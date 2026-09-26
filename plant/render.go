// Command render draws the SK-3X1 3x1 combined-cycle plant model as vector
// line art with ln.
//
// Usage (from the repository root):
//
//	go run ./plant                 # all views
//	go run ./plant -view B         # one view (keys from the model's view list)
//	go run ./plant -list           # list the views
//
// Views and their layer lists come from sk3x1_model.json, which follows the
// camera plan on sheet SK-3X1-11 (e.g. view B hides R1_ROOF and R1_WALL_E).
// Output is written as SVG and PNG to plant/renders/.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"strings"

	"github.com/fogleman/ln/ln"
)

type part struct {
	Kind  string       `json:"kind"`
	Layer string       `json:"layer"`
	Min   [3]float64   `json:"min"`
	Max   [3]float64   `json:"max"`
	A     [3]float64   `json:"a"`
	B     [3]float64   `json:"b"`
	R     float64      `json:"r"`
	R2    float64      `json:"r2"`
	V     [][3]float64 `json:"v"`
	Ridge string       `json:"ridge"`
	Color string       `json:"color"`
}

type route struct {
	Layer  string       `json:"layer"`
	Z      float64      `json:"z"`
	W      float64      `json:"w"`
	H      float64      `json:"h"`
	Points [][2]float64 `json:"points"`
}

type view struct {
	K    string     `json:"k"`
	N    string     `json:"n"`
	Show []string   `json:"show"`
	T    [3]float64 `json:"t"`
	C    [3]float64 `json:"c"`
}

type model struct {
	Parts  []part  `json:"parts"`
	Routes []route `json:"routes"`
	Views  []view  `json:"views"`
}

func vec(a [3]float64) ln.Vector { return ln.Vector{X: a[0], Y: a[1], Z: a[2]} }

// skipColor drops surface finishes that only add clutter to line art.
var skipColor = map[string]bool{"ground": true}

func build(m *model, v view, eye ln.Vector, clip float64) *ln.Scene {
	show := map[string]bool{}
	for _, l := range v.Show {
		show[l] = true
	}
	center := vec(v.T)
	near := func(lo, hi ln.Vector) bool {
		if clip <= 0 {
			return true
		}
		dx := math.Max(math.Max(lo.X-center.X, center.X-hi.X), 0)
		dy := math.Max(math.Max(lo.Y-center.Y, center.Y-hi.Y), 0)
		return math.Hypot(dx, dy) < clip
	}
	up := ln.Vector{Z: 1}
	scene := &ln.Scene{}
	for _, p := range m.Parts {
		if !show[p.Layer] || skipColor[p.Color] {
			continue
		}
		switch p.Kind {
		case "box":
			lo, hi := vec(p.Min), vec(p.Max)
			if !near(lo, hi) {
				continue
			}
			scene.Add(ln.NewCube(lo, hi))
		case "prism":
			lo, hi := vec(p.Min), vec(p.Max)
			if near(lo, hi) {
				scene.Add(prism(lo, hi, p.Ridge))
			}
		case "hex":
			var q [8]ln.Vector
			for i := range q {
				q[i] = vec(p.V[i])
			}
			if near(q[0].Min(q[6]), q[0].Max(q[6])) {
				scene.Add(hex(q))
			}
		case "rod":
			a, b := vec(p.A), vec(p.B)
			r := math.Max(p.R, p.R2)
			if !near(a.Min(b).SubScalar(r), a.Max(b).AddScalar(r)) {
				continue
			}
			if math.Abs(p.R-p.R2) < 1e-6 {
				scene.Add(ln.NewTransformedOutlineCylinder(eye, up, a, b, p.R))
			} else {
				scene.Add(frustum(a, b, p.R, p.R2))
			}
		}
	}
	for _, r := range m.Routes {
		if !show[r.Layer] || r.Z < 0 {
			continue
		}
		for i := 0; i+1 < len(r.Points); i++ {
			a, b := r.Points[i], r.Points[i+1]
			if a[0] != b[0] && a[1] != b[1] {
				continue // drawings are orthogonal; skip the odd diagonal
			}
			hw := r.W / 2
			lo := ln.Vector{X: math.Min(a[0], b[0]) - hw, Y: math.Min(a[1], b[1]) - hw, Z: r.Z - r.H/2}
			hi := ln.Vector{X: math.Max(a[0], b[0]) + hw, Y: math.Max(a[1], b[1]) + hw, Z: r.Z + r.H/2}
			if near(lo, hi) {
				scene.Add(ln.NewCube(lo, hi))
			}
		}
	}
	return scene
}

// outlineMesh is a triangle mesh (for hidden-line tests) that draws only
// the given feature edges instead of every triangle edge.
type outlineMesh struct {
	*ln.Mesh
	paths ln.Paths
}

func (m *outlineMesh) Paths() ln.Paths { return m.paths }

func quads(v []ln.Vector, faces [][4]int) []*ln.Triangle {
	var t []*ln.Triangle
	for _, f := range faces {
		t = append(t, ln.NewTriangle(v[f[0]], v[f[1]], v[f[2]]), ln.NewTriangle(v[f[0]], v[f[2]], v[f[3]]))
	}
	return t
}

// hex is a general 8-vertex loft: q[0..3] one end, q[4..7] the other.
func hex(q [8]ln.Vector) ln.Shape {
	v := q[:]
	t := quads(v, [][4]int{{0, 1, 2, 3}, {4, 7, 6, 5}, {0, 4, 5, 1}, {1, 5, 6, 2}, {2, 6, 7, 3}, {3, 7, 4, 0}})
	var p ln.Paths
	p = append(p, ln.Path{q[0], q[1], q[2], q[3], q[0]}, ln.Path{q[4], q[5], q[6], q[7], q[4]})
	for i := 0; i < 4; i++ {
		p = append(p, ln.Path{q[i], q[i+4]})
	}
	return &outlineMesh{ln.NewMesh(t), p}
}

// prism is an A-frame (gable) solid with its ridge along X or Y.
func prism(lo, hi ln.Vector, ridge string) ln.Shape {
	var a, b, c, d, e, f ln.Vector
	if ridge == "x" {
		ym := (lo.Y + hi.Y) / 2
		a, b, c = ln.Vector{X: lo.X, Y: lo.Y, Z: lo.Z}, ln.Vector{X: lo.X, Y: hi.Y, Z: lo.Z}, ln.Vector{X: lo.X, Y: ym, Z: hi.Z}
		d, e, f = ln.Vector{X: hi.X, Y: lo.Y, Z: lo.Z}, ln.Vector{X: hi.X, Y: hi.Y, Z: lo.Z}, ln.Vector{X: hi.X, Y: ym, Z: hi.Z}
	} else {
		xm := (lo.X + hi.X) / 2
		a, b, c = ln.Vector{X: lo.X, Y: lo.Y, Z: lo.Z}, ln.Vector{X: hi.X, Y: lo.Y, Z: lo.Z}, ln.Vector{X: xm, Y: lo.Y, Z: hi.Z}
		d, e, f = ln.Vector{X: lo.X, Y: hi.Y, Z: lo.Z}, ln.Vector{X: hi.X, Y: hi.Y, Z: lo.Z}, ln.Vector{X: xm, Y: hi.Y, Z: hi.Z}
	}
	t := []*ln.Triangle{
		ln.NewTriangle(a, b, c), ln.NewTriangle(d, f, e),
		ln.NewTriangle(a, c, f), ln.NewTriangle(a, f, d),
		ln.NewTriangle(b, e, f), ln.NewTriangle(b, f, c),
		ln.NewTriangle(a, d, e), ln.NewTriangle(a, e, b),
	}
	return &outlineMesh{ln.NewMesh(t), ln.Paths{{a, b, c, a}, {d, e, f, d}, {a, d}, {b, e}, {c, f}}}
}

// frustum is a cone section from a (radius r1) to b (radius r2), drawn as
// its two end circles and four generator lines.
func frustum(a, b ln.Vector, r1, r2 float64) ln.Shape {
	const n = 24
	ax := b.Sub(a).Normalize()
	ref := ln.Vector{X: 1}
	if math.Abs(ax.X) > 0.9 {
		ref = ln.Vector{Y: 1}
	}
	u := ax.Cross(ref).Normalize()
	w := ax.Cross(u)
	ring := func(c ln.Vector, r float64) []ln.Vector {
		v := make([]ln.Vector, n)
		for i := range v {
			t := 2 * math.Pi * float64(i) / n
			v[i] = c.Add(u.MulScalar(r * math.Cos(t))).Add(w.MulScalar(r * math.Sin(t)))
		}
		return v
	}
	p0, p1 := ring(a, r1), ring(b, r2)
	var tris []*ln.Triangle
	for i := 0; i < n; i++ {
		j := (i + 1) % n
		tris = append(tris, ln.NewTriangle(p0[i], p0[j], p1[j]), ln.NewTriangle(p0[i], p1[j], p1[i]),
			ln.NewTriangle(a, p0[j], p0[i]), ln.NewTriangle(b, p1[i], p1[j]))
	}
	c0, c1 := append(ln.Path{}, p0...), append(ln.Path{}, p1...)
	c0, c1 = append(c0, p0[0]), append(c1, p1[0])
	paths := ln.Paths{c0, c1}
	for i := 0; i < n; i += n / 4 {
		paths = append(paths, ln.Path{p0[i], p1[i]})
	}
	return &outlineMesh{ln.NewMesh(tris), paths}
}

func main() {
	dir := flag.String("dir", "plant", "directory holding sk3x1_model.json")
	only := flag.String("view", "", "render one view by key (see -list)")
	list := flag.Bool("list", false, "list the views and exit")
	size := flag.Float64("size", 2400, "output width in pixels (height is 2/3)")
	flag.Parse()

	data, err := os.ReadFile(filepath.Join(*dir, "sk3x1_model.json"))
	if err != nil {
		fmt.Fprintln(os.Stderr, "read model:", err)
		os.Exit(1)
	}
	var m model
	if err := json.Unmarshal(data, &m); err != nil {
		fmt.Fprintln(os.Stderr, "parse model:", err)
		os.Exit(1)
	}
	if *list {
		for _, v := range m.Views {
			fmt.Printf("%-4s %s\n", v.K, v.N)
		}
		return
	}
	out := filepath.Join(*dir, "renders")
	if err := os.MkdirAll(out, 0o755); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	width, height := *size, *size*2/3
	for _, v := range m.Views {
		if (*only != "" && !strings.EqualFold(*only, v.K)) || (*only == "" && v.K == "ALL") {
			continue
		}
		eye, center := vec(v.C), vec(v.T)
		dist := eye.Sub(center).Length()
		fovy := 34.0
		// geometry clip radius keeps close-ups fast; overviews draw everything
		clip := 0.0
		if dist < 900 {
			clip = dist * 1.6
		}
		scene := build(&m, v, eye, clip)
		paths := scene.Render(eye, center, ln.Vector{Z: 1}, width, height, fovy, 1, 20000, 0.25)
		name := "sk3x1_view_" + strings.ToLower(v.K)
		base := filepath.Join(out, name)
		if err := paths.WriteToSVG(base+".svg", width, height); err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
		paths.WriteToPNG(base+".png", width, height)
		fmt.Printf("%-4s %-26s %6d paths -> %s.{svg,png}\n", v.K, v.N, len(paths), base)
	}
}
