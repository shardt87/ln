package main

// Line-art model of a combined cycle power plant (CCPP) site.
//
// The arrangement follows the generic layout found in public plot plans,
// single-line diagrams and EIA/permit drawings of CCGT projects: a gas
// receiving & metering station (pipeline or LNG regas send-out), a 1x1
// single-shaft-style block (GT + HRSG + ST + air cooled condenser), a
// post-combustion carbon capture (CCS) train on the HRSG flue gas, a
// modular reciprocating engine (RICE) hall for peaking / black start, and
// the generator step-up transformers wired by overhead conductors to the
// HV switchyard and the outgoing transmission line.
//
// All dimensions are in meters and are representative, not taken from any
// specific project.

import (
	"math"

	"github.com/fogleman/ln/ln"
)

var (
	eye    = ln.Vector{-170, -230, 150}
	center = ln.Vector{70, 35, 5}
	up     = ln.Vector{0, 0, 1}
)

// Lines is a shape made only of paths. It never occludes anything, which
// makes it suitable for cables, conductors and lattice steel.
type Lines struct {
	ln.EmptyShape
	P ln.Paths
}

func (l *Lines) Paths() ln.Paths {
	return l.P
}

func (l *Lines) BoundingBox() ln.Box {
	return l.P.BoundingBox()
}

type Plant struct {
	scene ln.Scene
	lines ln.Paths
}

func v(x, y, z float64) ln.Vector {
	return ln.Vector{x, y, z}
}

func (p *Plant) Box(x0, y0, z0, x1, y1, z1 float64) {
	p.scene.Add(ln.NewCube(v(x0, y0, z0), v(x1, y1, z1)))
}

func (p *Plant) Pipe(a, b ln.Vector, r float64) {
	p.scene.Add(ln.NewTransformedOutlineCylinder(eye, up, a, b, r))
}

func (p *Plant) Tank(x, y, r, h float64) {
	p.Pipe(v(x, y, 0), v(x, y, h), r)
}

func (p *Plant) Line(points ...ln.Vector) {
	p.lines = append(p.lines, ln.Path(points))
}

func (p *Plant) Circle(c ln.Vector, r float64) {
	var path ln.Path
	for i := 0; i <= 36; i++ {
		a := ln.Radians(float64(i * 10))
		path = append(path, c.Add(v(math.Cos(a)*r, math.Sin(a)*r, 0)))
	}
	p.lines = append(p.lines, path)
}

// Cable draws a conductor between two attachment points with a parabolic
// sag approximating a catenary.
func (p *Plant) Cable(a, b ln.Vector, sag float64) {
	var path ln.Path
	n := 24
	for i := 0; i <= n; i++ {
		t := float64(i) / float64(n)
		q := a.Add(b.Sub(a).MulScalar(t))
		q.Z -= sag * 4 * t * (1 - t)
		path = append(path, q)
	}
	p.lines = append(p.lines, path)
}

// Tray draws an elevated cable tray (two side rails with rungs) along a
// polyline route.
func (p *Plant) Tray(w float64, route ...ln.Vector) {
	for i := 1; i < len(route); i++ {
		a, b := route[i-1], route[i]
		d := b.Sub(a)
		n := v(-d.Y, d.X, 0).Normalize().MulScalar(w / 2)
		p.Line(a.Add(n), b.Add(n))
		p.Line(a.Sub(n), b.Sub(n))
		steps := int(d.Length() / 3)
		for j := 0; j <= steps; j++ {
			c := a.Add(d.MulScalar(float64(j) / float64(steps)))
			p.Line(c.Add(n), c.Sub(n))
		}
	}
}

// Gantry is a switchyard dead-end structure: two lattice columns and a
// beam. It returns the conductor attachment points for three phases.
func (p *Plant) Gantry(x, y0, y1, h float64) []ln.Vector {
	for _, y := range []float64{y0, y1} {
		p.Lattice(v(x, y, 0), h, 1.2)
	}
	p.Line(v(x, y0, h), v(x, y1, h))
	p.Line(v(x, y0, h-1.5), v(x, y1, h-1.5))
	for i := 0; i <= 8; i++ {
		y := y0 + (y1-y0)*float64(i)/8
		p.Line(v(x, y, h), v(x, y, h-1.5))
	}
	var points []ln.Vector
	for i := 1; i <= 3; i++ {
		y := y0 + (y1-y0)*float64(i)/4
		p.Line(v(x, y, h-1.5), v(x, y, h-3.5)) // insulator string
		points = append(points, v(x, y, h-3.5))
	}
	return points
}

// Lattice draws a square lattice column with X bracing.
func (p *Plant) Lattice(base ln.Vector, h, w float64) {
	c := []ln.Vector{v(-w, -w, 0), v(w, -w, 0), v(w, w, 0), v(-w, w, 0)}
	for _, o := range c {
		p.Line(base.Add(o), base.Add(o).Add(v(0, 0, h)))
	}
	for z := 0.0; z < h; z += 2 * w {
		z1 := math.Min(z+2*w, h)
		for i := range c {
			a, b := c[i], c[(i+1)%4]
			p.Line(base.Add(a).Add(v(0, 0, z)), base.Add(b).Add(v(0, 0, z1)))
			p.Line(base.Add(b).Add(v(0, 0, z)), base.Add(a).Add(v(0, 0, z1)))
		}
	}
}

// Tower is a transmission lattice tower with three cross arms. It returns
// the conductor attachment points.
func (p *Plant) Tower(x, y, h float64) []ln.Vector {
	w0, w1 := 4.0, 1.0
	var legs []ln.Path
	for _, s := range []ln.Vector{v(-1, -1, 0), v(1, -1, 0), v(1, 1, 0), v(-1, 1, 0)} {
		a := v(x+s.X*w0, y+s.Y*w0, 0)
		b := v(x+s.X*w1, y+s.Y*w1, h)
		legs = append(legs, ln.Path{a, b})
		p.Line(a, b)
	}
	n := 10
	for i := 0; i < n; i++ {
		t0, t1 := float64(i)/float64(n), float64(i+1)/float64(n)
		for j := range legs {
			a, b := legs[j], legs[(j+1)%4]
			pa0 := a[0].Add(a[1].Sub(a[0]).MulScalar(t0))
			pa1 := a[0].Add(a[1].Sub(a[0]).MulScalar(t1))
			pb0 := b[0].Add(b[1].Sub(b[0]).MulScalar(t0))
			pb1 := b[0].Add(b[1].Sub(b[0]).MulScalar(t1))
			p.Line(pa0, pb1)
			p.Line(pb0, pa1)
		}
	}
	var points []ln.Vector
	for i, z := range []float64{h - 10, h - 5, h} {
		arm := 6.0 - float64(i)
		p.Line(v(x, y-arm, z), v(x, y+arm, z))
		p.Line(v(x, y-arm, z), v(x, y-1, z-2))
		p.Line(v(x, y+arm, z), v(x, y+1, z-2))
		side := arm
		if i%2 == 1 {
			side = -arm
		}
		p.Line(v(x, y+side, z), v(x, y+side, z-2.5))
		points = append(points, v(x, y+side, z-2.5))
	}
	return points
}

// GasStation is the gas receiving, filtering, metering and pressure
// regulating station (custody transfer). Fed from an LNG tank and
// vaporizers or a pipeline tie-in.
func (p *Plant) GasStation() ln.Vector {
	// LNG full containment tank with roof, and ambient air vaporizers
	p.Tank(-60, 10, 16, 24)
	p.Circle(v(-60, 10, 27), 10)
	for a := 0; a < 360; a += 30 {
		c, s := math.Cos(ln.Radians(float64(a))), math.Sin(ln.Radians(float64(a)))
		p.Line(v(-60+16*c, 10+16*s, 24), v(-60+10*c, 10+10*s, 27))
	}
	for i := 0; i < 4; i++ {
		x := -38.0 + float64(i)*4
		p.Box(x, -8, 0, x+2.5, -2, 12)
	}
	// skid base and shelter
	p.Box(-25, -6, 0, 5, 14, 0.4)
	p.Box(-25, 10, 0.4, -15, 14, 4)
	// filter separators
	for i := 0; i < 2; i++ {
		x := -21.0 + float64(i)*4
		p.Pipe(v(x, 0, 0.4), v(x, 0, 6), 0.9)
	}
	// ultrasonic / turbine meter runs (2 x 100% + spare)
	for i := 0; i < 3; i++ {
		y := -3.0 + float64(i)*3
		p.Pipe(v(-12, y, 1.5), v(-2, y, 1.5), 0.35)
		p.Box(-8, y-0.6, 1, -6.5, y+0.6, 2.2) // meter body
	}
	p.Pipe(v(-12, -4, 1.5), v(-12, 4, 1.5), 0.5) // inlet header
	p.Pipe(v(-2, -4, 1.5), v(-2, 4, 1.5), 0.5)   // outlet header
	// gas heater and pressure regulators
	p.Pipe(v(0, 7, 1.5), v(4, 7, 1.5), 1.0)
	p.Box(0, 0, 0.4, 3, 3, 2.5)
	// pipe from LNG area into station
	p.Pipe(v(-44, 10, 4), v(-25, 10, 4), 0.4)
	p.Pipe(v(-25, 0, 1.5), v(-21, 0, 1.5), 0.4)
	return v(4, 7, 1.5)
}

// PowerBlock is the GT + HRSG + ST + ACC train. It returns the GT and ST
// generator terminal points used for the isolated phase bus to the GSUs.
func (p *Plant) PowerBlock(gas ln.Vector) (ln.Vector, ln.Vector) {
	// fuel gas line on the pipe rack to the GT
	p.Pipe(gas, v(20, 7, 1.5), 0.4)
	p.Pipe(v(20, 7, 1.5), v(20, 7, 7), 0.4)
	p.Pipe(v(20, 7, 7), v(48, 7, 7), 0.4)
	// pipe rack steel
	for x := 20.0; x <= 48; x += 7 {
		p.Line(v(x, 5.5, 0), v(x, 5.5, 8))
		p.Line(v(x, 8.5, 0), v(x, 8.5, 8))
		p.Line(v(x, 5.5, 8), v(x, 8.5, 8))
	}
	p.Line(v(20, 5.5, 8), v(48, 5.5, 8))
	p.Line(v(20, 8.5, 8), v(48, 8.5, 8))

	// gas turbine: inlet filter house, inlet duct, enclosure, generator
	p.Box(30, -10, 10, 42, 14, 24)
	p.Box(36, -2, 0, 42, 6, 10)
	p.Box(42, -3, 0, 70, 7, 9)
	p.Box(46, -2.5, 9, 66, 6.5, 11) // roof vent package
	p.Box(70, -2, 0, 76, 6, 6)      // exhaust diffuser
	p.Box(52, 10, 0, 64, 18, 6)     // GT generator (offset, cold end drive)
	// HRSG: transition duct, casing, steel, drum, stack
	p.Box(76, -4, 0, 82, 10, 18)
	p.Box(82, -5, 0, 112, 11, 28)
	p.Pipe(v(86, -1, 30), v(108, -1, 30), 1.2) // HP drum
	for x := 84.0; x <= 110; x += 6.5 {
		p.Line(v(x, -5, 28), v(x, -5, 30))
		p.Line(v(x, 11, 28), v(x, 11, 30))
	}
	p.Tank(117, 3, 3.5, 55)
	p.Box(112, 0, 22, 117, 6, 27)

	// steam turbine hall and ST generator
	p.Box(52, 28, 0, 92, 46, 22)
	p.Box(60, 32, 6, 72, 40, 10)
	// steam lines HRSG -> ST
	p.Pipe(v(96, 11, 24), v(96, 30, 24), 0.6)
	p.Pipe(v(96, 30, 24), v(92, 30, 24), 0.6)
	// air cooled condenser on columns with fan rings
	for x := 100.0; x <= 140; x += 10 {
		for y := 28.0; y <= 58; y += 10 {
			p.Pipe(v(x, y, 0), v(x, y, 18), 0.4)
		}
	}
	p.Box(98, 26, 18, 142, 60, 20)
	for x := 104.0; x <= 136; x += 8 {
		for y := 32.0; y <= 54; y += 11 {
			p.Circle(v(x, y, 20.05), 3.2)
		}
	}
	// A-frame tube bundles above fan deck
	for x := 98.0; x <= 142; x += 11 {
		p.Line(v(x, 26, 20), v(x, 43, 30), v(x, 60, 20))
	}
	p.Line(v(98, 43, 30), v(142, 43, 30))
	p.Pipe(v(92, 40, 18), v(98, 40, 26), 1.5) // exhaust steam duct

	return v(58, 18, 4), v(60, 46, 6)
}

// CarbonCapture is a post-combustion amine CCS train: flue gas from the
// HRSG stack breeching via booster fan to direct contact cooler, absorber,
// stripper/reboiler, and CO2 compression & dehydration.
func (p *Plant) CarbonCapture() {
	p.Box(117, 3, 30, 150, 9, 36)               // flue duct
	p.Box(145, -8, 0, 155, 0, 8)                // booster fan
	p.Tank(150, 3, 5, 34)                       // direct contact cooler
	p.Box(150, 6, 34, 166, 10, 37)              // duct DCC -> absorber
	p.Tank(170, 6, 8, 62)                       // absorber
	p.Tank(170, 6, 2.5, 72)                     // absorber vent / water wash stack
	p.Tank(190, 20, 4, 44)                      // stripper
	p.Tank(198, 20, 2.5, 12)                    // reboiler
	p.Box(180, 32, 0, 210, 46, 12)              // CO2 compressor building
	p.Box(210, 34, 0, 218, 44, 8)               // dehydration unit
	p.Pipe(v(170, 6, 50), v(190, 20, 40), 0.5)  // rich amine
	p.Pipe(v(190, 20, 6), v(170, 6, 6), 0.5)    // lean amine
	p.Pipe(v(190, 20, 44), v(195, 39, 12), 0.4) // CO2 overhead
	p.Pipe(v(218, 39, 4), v(240, 39, 4), 0.4)   // CO2 export to pipeline
	p.Box(240, 37, 0, 244, 41, 3)               // CO2 fiscal meter skid
	// steam extraction from ST to reboiler
	p.Pipe(v(92, 44, 16), v(160, 64, 16), 0.5)
	p.Pipe(v(160, 64, 16), v(198, 20, 12), 0.5)
}

// RICE is a modular reciprocating engine hall: containerized gensets with
// exhaust stacks, roof radiators, and their own step-up transformers.
// Returns the attachment point of the RICE MV/HV transformer.
func (p *Plant) RICE() ln.Vector {
	for i := 0; i < 8; i++ {
		y := 70.0 + float64(i)*4.2
		p.Box(-10, y, 0, 2.2, y+2.9, 2.9)   // 40ft genset container
		p.Box(-8, y+0.3, 2.9, -1, y+2.6, 4) // radiator
		p.Pipe(v(1, y+1.45, 2.9), v(1, y+1.45, 9), 0.35)
	}
	// LV/MV collector cable tray along the containers to the transformer
	p.Tray(1.0, v(4, 70, 3), v(4, 104, 3), v(12, 104, 3))
	// collector switchgear e-house and RICE step-up transformer
	p.Box(6, 96, 0, 18, 102, 4)
	p.Box(14, 105, 0, 20, 110, 5)
	for i := 0; i < 3; i++ {
		y := 106.0 + float64(i)*1.5
		p.Pipe(v(18, y, 5), v(18, y, 8), 0.2)
	}
	return v(18, 108, 8)
}

// Transformer draws a GSU transformer with radiator banks and HV bushings
// and returns the bushing tops.
func (p *Plant) Transformer(x, y float64) []ln.Vector {
	p.Box(x, y, 0, x+8, y+5, 6)
	p.Box(x-1.5, y+0.5, 0.5, x, y+4.5, 5.5)
	p.Box(x+8, y+0.5, 0.5, x+9.5, y+4.5, 5.5)
	p.Box(x+1, y+1, 6, x+3, y+4, 7.5) // conservator
	var points []ln.Vector
	for i := 0; i < 3; i++ {
		b := v(x+4+float64(i-1)*2, y+4.5, 6)
		t := b.Add(v(0, 1, 4))
		p.Pipe(b, t, 0.25)
		points = append(points, t)
	}
	return points
}

func main() {
	p := Plant{}

	gas := p.GasStation()
	gtGen, stGen := p.PowerBlock(gas)
	p.CarbonCapture()
	ricePoint := p.RICE()

	// generator step-up transformers and isolated phase bus duct
	gtGSU := p.Transformer(50, 60)
	stGSU := p.Transformer(70, 60)
	p.Box(gtGen.X-1, gtGen.Y, 3, gtGen.X+1, 60, 4.5)
	p.Box(stGen.X-1, stGen.Y, 3, stGen.X+1, 60, 4.5)
	// medium voltage cable trays to auxiliary transformers / MCC e-house
	p.Box(34, 50, 0, 46, 56, 4)
	p.Tray(0.8, v(40, 50, 5), v(40, 20, 5), v(46, 20, 5))
	p.Tray(0.8, v(46, 53, 5), v(140, 53, 5), v(140, 64, 5), v(180, 64, 5), v(180, 40, 5))
	p.Tray(0.8, v(40, 50, 5), v(-4, 50, 5), v(-4, 14, 5))

	// switchyard: gantries, busbars, disconnect/breaker bays
	ys := []float64{125, 150}
	var bays [][]ln.Vector
	for _, x := range []float64{20, 40, 60, 80} {
		pts := p.Gantry(x, ys[0], ys[1], 16)
		bays = append(bays, pts)
		for _, q := range pts {
			// breaker and disconnector on pedestals below each phase
			p.Pipe(v(q.X, q.Y, 0), v(q.X, q.Y, 4), 0.3)
			p.Box(q.X-0.6, q.Y-0.6, 4, q.X+0.6, q.Y+0.6, 6)
			p.Line(v(q.X, q.Y, 6), q)
		}
	}
	// strung busbars between gantries
	for i := 1; i < len(bays); i++ {
		for j := range bays[i] {
			p.Cable(bays[i-1][j], bays[i][j], 0.6)
		}
	}
	// overhead conductors from GSUs and RICE transformer into bays
	for j := 0; j < 3; j++ {
		p.Cable(gtGSU[j], bays[2][j], 1.5)
		p.Cable(stGSU[j], bays[3][j], 1.5)
		p.Cable(ricePoint.Add(v(0, float64(j-1)*1.5, 0)), bays[0][j], 1.0)
	}
	// outgoing transmission line
	prev := bays[3]
	for k, x := range []float64{130, 200, 270} {
		pts := p.Tower(x, 137.5+float64(k)*15, 34)
		for j := 0; j < 3; j++ {
			p.Cable(prev[j], pts[j], 2.5+float64(k))
		}
		prev = pts
	}
	// earth/shield wire
	p.Line(v(20, 125, 16), v(80, 125, 16))
	p.Line(v(20, 150, 16), v(80, 150, 16))

	// site boundary fence
	p.Line(v(-85, -20, 0), v(250, -20, 0), v(250, 165, 0), v(-85, 165, 0), v(-85, -20, 0))

	p.scene.Add(&Lines{P: p.lines})

	width := 3000.0
	height := 1900.0
	fovy := 32.0
	paths := p.scene.Render(eye, center, up, width, height, fovy, 1, 2000, 0.25)
	paths.WriteToPNG("out.png", width, height)
	paths.WriteToSVG("out.svg", width, height)
}
