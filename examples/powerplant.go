// powerplant renders a massing model of a combined-cycle power plant site
// as hidden-line vector art. Shapes are tagged with a layer so the drawing
// can be styled per layer (site, plant, power path); numbered anchor points
// are projected with the same camera so labels line up with the drawing.
//
// Output (stdout):
//
//	L <layer>          start of a layer
//	x,y;x,y;...        one visible polyline per line (screen units)
//	A <label> x y      projected anchor point
package main

import (
	"fmt"
	"os"
	"sort"

	"github.com/fogleman/ln/ln"
)

const (
	width  = 2000.0
	height = 1250.0
)

var (
	center = ln.Vector{X: 58, Y: 44, Z: 6}
	eye    = center.Add(ln.Vector{X: -175, Y: -150, Z: 165})
	up     = ln.Vector{X: 0, Y: 0, Z: 1}
)

type plant struct {
	scene  ln.Scene
	layers map[string][]ln.Shape
}

func (p *plant) add(layer string, s ln.Shape) {
	p.scene.Add(s)
	p.layers[layer] = append(p.layers[layer], s)
}

func (p *plant) box(layer string, x0, y0, z0, x1, y1, z1 float64) {
	p.add(layer, ln.NewCube(ln.Vector{X: x0, Y: y0, Z: z0}, ln.Vector{X: x1, Y: y1, Z: z1}))
}

// vcyl is a vertical cylinder drawn as a silhouette (outline) or hatched.
func (p *plant) vcyl(layer string, x, y, r, z0, z1 float64, outline bool) {
	v0, v1 := ln.Vector{X: x, Y: y, Z: z0}, ln.Vector{X: x, Y: y, Z: z1}
	if outline {
		p.add(layer, ln.NewTransformedOutlineCylinder(eye, up, v0, v1, r))
		return
	}
	c := ln.NewCylinder(r, z0, z1)
	p.add(layer, ln.NewTransformedShape(c, ln.Translate(ln.Vector{X: x, Y: y})))
}

// hcyl is a hatched horizontal cylinder of length l centred on c, with its
// axis along x (alongX) or y.
func (p *plant) hcyl(layer string, c ln.Vector, l, r float64, alongX bool) {
	axis := ln.Vector{X: 1}
	if alongX {
		axis = ln.Vector{Y: 1}
	}
	m := ln.Rotate(axis, ln.Radians(90)).Translate(c)
	p.add(layer, ln.NewTransformedShape(ln.NewCylinder(r, -l/2, l/2), m))
}

// reel is a cable reel lying on its flanges: two thin discs and a drum.
func (p *plant) reel(layer string, x, y, r, w float64, alongX bool) {
	c := ln.Vector{X: x, Y: y, Z: r}
	off := ln.Vector{Y: w/2 - 0.1}
	if alongX {
		off = ln.Vector{X: w/2 - 0.1}
	}
	p.hcyl(layer, c.Sub(off), 0.2, r, alongX)
	p.hcyl(layer, c.Add(off), 0.2, r, alongX)
	p.hcyl(layer, c, w-0.4, r*0.72, alongX)
}

func build() *plant {
	p := &plant{layers: map[string][]ln.Shape{}}

	// site slab and paved areas
	p.box("site", 0, 0, -1.2, 120, 92, 0)
	p.box("site", 4, 38, 0, 24, 60, 0.15)   // BESS pad
	p.box("site", 6, 20, 0, 28, 38, 0.15)   // reel yard
	p.box("site", 22, 2, 0, 38, 14, 0.15)   // admin compound
	p.box("site", 2, 62, 0, 26, 90, 0.15)   // switchyard
	p.box("site", 98, 6, 0, 118, 38, 0.15)  // modular generation
	p.box("site", 96, 38, 0, 114, 54, 0.15) // gas yard

	// ---- power path: generation, heat recovery, collection, export ----
	// turbine hall
	p.box("power", 34, 38, 0, 84, 56, 14)
	p.box("power", 36, 45, 14, 82, 49, 16.5) // roof monitor
	for x := 38.0; x <= 80; x += 7 {
		p.box("power", x, 37.4, 11, x+3, 38, 12.5) // wall louvres
	}
	// HRSG trains with inlet ducts and stacks
	for i := 0; i < 3; i++ {
		x0 := 57 + float64(i)*11.5
		p.box("power", x0, 16, 0, x0+8, 32, 19)
		p.box("power", x0+1, 18, 19, x0+7, 21, 21.5) // steam drum housing
		p.box("power", x0+2, 32, 5, x0+6, 38, 11)    // exhaust duct from GT
		p.vcyl("power", x0+4, 12.5, 2.3, 0, 27, true)
		p.vcyl("power", x0+4, 12.5, 2.8, 25, 27.5, true) // stack collar
	}
	// electrical e-house on piers
	for _, x := range []float64{44.5, 49, 53.5} {
		p.box("power", x, 16.5, 0, x+1, 17.5, 1.8)
		p.box("power", x, 21.5, 0, x+1, 22.5, 1.8)
	}
	p.box("power", 44, 16, 1.8, 55, 23, 6.5)
	// step-up transformers with radiators
	for _, y := range []float64{40, 45.5, 51} {
		p.box("power", 26, y, 0, 31, y+4, 4.5)
		p.box("power", 25.2, y+0.6, 0.6, 26, y+3.4, 4)
		p.vcyl("power", 28.5, y+2, 0.35, 4.5, 6.5, true) // bushing
	}
	// switchyard gantries and breakers
	for _, y := range []float64{66, 74, 82} {
		p.box("power", 5, y, 0, 5.6, y+0.6, 11)
		p.box("power", 22, y, 0, 22.6, y+0.6, 11)
		p.box("power", 5, y, 11, 22.6, y+0.6, 11.8)
		for _, x := range []float64{9, 13.5, 18} {
			p.box("power", x-1, y+2, 0, x+1, y+4, 3.5)
			p.vcyl("power", x, y+3, 0.4, 3.5, 6.5, true)
		}
	}
	// transmission tower (stepped lattice massing)
	tx, ty := 13.5, 89.0
	steps := []struct{ h, z0, z1 float64 }{{2.2, 0, 9}, {1.6, 9, 17}, {1.0, 17, 23}, {0.6, 23, 28}}
	for _, s := range steps {
		p.box("power", tx-s.h, ty-s.h/2, s.z0, tx+s.h, ty+s.h/2, s.z1)
	}
	p.box("power", tx-7, ty-0.3, 19, tx+7, ty+0.3, 19.8)
	p.box("power", tx-5, ty-0.3, 25, tx+5, ty+0.3, 25.8)
	// battery energy storage: two rows of containers
	for r := 0; r < 3; r++ {
		for c := 0; c < 3; c++ {
			x, y := 6.0+float64(c)*5.8, 41.0+float64(r)*6
			p.box("power", x, y, 0, x+5, y+2.6, 2.9)
		}
	}

	// ---- plant: cooling, water, fuel, carbon capture, support ----
	// air-cooled condenser on columns, fans on deck
	for x := 16.0; x <= 58; x += 7 {
		for _, y := range []float64{70, 83} {
			p.box("plant", x, y, 0, x+0.8, y+0.8, 9)
		}
	}
	p.box("plant", 15, 69, 9, 60, 85, 10.5)
	p.box("plant", 17, 72, 10.5, 58, 76, 14) // A-frame bundles (massing)
	p.box("plant", 17, 78, 10.5, 58, 82, 14)
	for x := 20.0; x <= 56; x += 6 {
		p.vcyl("plant", x, 77, 1.4, 10.5, 12, false)
	}
	// steam duct from turbine hall to ACC
	p.box("plant", 30, 56, 11, 33, 69, 14)
	// cooling cells / chillers
	p.box("plant", 28, 86, 0, 62, 91, 2.5)
	for x := 31.0; x <= 60; x += 5.5 {
		p.vcyl("plant", x, 88.5, 2.1, 2.5, 5.5, false)
	}
	// water treatment basins and clarifier
	for i := 0; i < 3; i++ {
		x0 := 64 + float64(i)*7
		p.box("plant", x0, 66, 0, x0+6, 78, 1.8)
	}
	p.box("plant", 86, 74, 0, 104, 90, 1.2) // retention basin
	p.vcyl("plant", 68, 85, 3.5, 0, 2.2, false)
	p.box("plant", 76, 82, 0, 84, 90, 4.5) // pump house
	// carbon-capture island
	p.vcyl("plant", 100, 64, 3.2, 0, 31, true)
	p.vcyl("plant", 100, 64, 3.8, 28, 31, true)
	p.vcyl("plant", 108, 70, 4.2, 0, 16, false)
	p.add("plant", ln.NewSphere(ln.Vector{X: 110, Y: 58, Z: 4.5}, 4.5))
	// pipe rack linking the islands
	for x := 34.0; x <= 104; x += 7 {
		p.box("plant", x, 58.5, 0, x+0.6, 59.1, 8)
		p.box("plant", x, 61.5, 0, x+0.6, 62.1, 8)
	}
	p.box("plant", 34, 58.5, 8, 104.6, 62.1, 8.8)
	// gas metering and conditioning trains
	p.box("plant", 98, 40, 0, 106, 46, 4)
	for _, y := range []float64{48, 50.5} {
		p.hcyl("plant", ln.Vector{X: 104.5, Y: y, Z: 1.4}, 15, 0.6, true)
	}
	p.vcyl("plant", 109, 43, 1.2, 0, 5, true)
	// modular engine-generators and black-start sets
	for i := 0; i < 3; i++ {
		y0 := 20 + float64(i)*5.5
		p.box("plant", 104, y0, 0, 116, y0+4, 4.5)
		p.vcyl("plant", 114, y0+2, 0.5, 4.5, 9, true)
	}
	for _, x := range []float64{100, 106.5} {
		p.box("plant", x, 9, 0, x+5, 14, 3.5)
	}
	// cable reel yard: reels lying on their axes, conductor sets
	for i := 0; i < 4; i++ {
		p.reel("plant", 10+float64(i)*4.4, 24, 2, 1.6, true)
	}
	for i := 0; i < 3; i++ {
		p.reel("plant", 23.5, 28.5+float64(i)*3, 1.4, 1.3, false)
	}
	p.box("plant", 9, 30, 0, 18, 33, 2.4) // staged module
	// admin / control building
	p.box("plant", 25, 5, 0, 36, 11.5, 5)
	p.box("plant", 28, 7, 5, 31, 9.5, 6.5)
	// field cable trays on supports between e-house and turbine hall
	for x := 40.0; x <= 56; x += 4 {
		p.box("plant", x, 30, 0, x+0.4, 30.4, 4)
	}
	p.box("plant", 40, 29.6, 4, 56.4, 30.8, 4.5)
	p.box("plant", 55, 23, 4, 56.2, 30.8, 4.5)
	// grounding-grid demonstration: bars flush with grade
	for i := 0; i <= 4; i++ {
		f := float64(i) * 2
		p.box("plant", 40+f, 1, 0, 40.2+f, 9, 0.05)
		p.box("plant", 40, 1+f, 0, 48.2, 1.2+f, 0.05)
	}
	return p
}

var anchors = map[string]ln.Vector{
	"1": {X: 64, Y: 47, Z: 16.5}, "2": {X: 42, Y: 47, Z: 16.5}, "3": {X: 72.5, Y: 24, Z: 21.5},
	"4": {X: 80, Y: 52, Z: 14}, "5": {X: 49.5, Y: 19.5, Z: 6.5}, "6": {X: 26, Y: 80, Z: 14},
	"7": {X: 42, Y: 88.5, Z: 5.5}, "8": {X: 74, Y: 72, Z: 1.8}, "9": {X: 102, Y: 43, Z: 4},
	"10": {X: 110, Y: 28, Z: 4.5}, "11": {X: 103, Y: 11.5, Z: 3.5}, "12": {X: 14, Y: 50, Z: 2.9},
	"13": {X: 13.5, Y: 74, Z: 11.8}, "14": {X: 16, Y: 24, Z: 4}, "15": {X: 30.5, Y: 8, Z: 6.5},
	"16": {X: 100, Y: 64, Z: 31}, "17": {X: 44, Y: 5, Z: 0}, "18": {X: 48, Y: 30, Z: 4.5},
}

func main() {
	p := build()
	p.scene.Compile()
	matrix := ln.LookAt(eye, center, up).Perspective(27, width/height, 1, 2000)
	screen := ln.Translate(ln.Vector{X: 1, Y: 1}).Scale(ln.Vector{X: width / 2, Y: height / 2, Z: 0})

	out := os.Stdout
	names := make([]string, 0, len(p.layers))
	for name := range p.layers {
		names = append(names, name)
	}
	sort.Strings(names)
	for _, name := range names {
		var paths ln.Paths
		for _, s := range p.layers[name] {
			paths = append(paths, s.Paths()...)
		}
		paths = paths.Chop(0.05)
		paths = paths.Filter(&ln.ClipFilter{Matrix: matrix, Eye: eye, Scene: &p.scene})
		paths = paths.Simplify(1e-6).Transform(screen)
		fmt.Fprintf(out, "L %s\n", name)
		for _, path := range paths {
			if len(path) > 1 {
				fmt.Fprintln(out, path.String())
			}
		}
	}
	for k, v := range anchors {
		s := screen.MulPosition(matrix.MulPositionW(v))
		fmt.Fprintf(out, "A %s %.2f %.2f\n", k, s.X, s.Y)
	}
}
