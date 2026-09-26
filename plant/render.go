// Command render draws the SK-3X1 3x1 combined-cycle plant model as vector
// line art with ln.
//
// Usage (from the repository root):
//
//	go run ./plant                       # all views, base plant
//	go run ./plant -view powerblock -opt # one view, include optional systems
//
// The model is read from plant/sk3x1_model.json (see build_model.py).
// Output is written as SVG and PNG to plant/renders/.
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/fogleman/ln/ln"
)

type object struct {
	Kind   string     `json:"kind"`
	Layer  string     `json:"layer"`
	Name   string     `json:"name"`
	Min    [3]float64 `json:"min"`
	Max    [3]float64 `json:"max"`
	Center [2]float64 `json:"center"`
	R      float64    `json:"r"`
	Z0     float64    `json:"z0"`
	Z1     float64    `json:"z1"`
	Axis   string     `json:"axis"`
	Color  string     `json:"color"`
}

type route struct {
	Type   string       `json:"type"`
	Layer  string       `json:"layer"`
	Z      float64      `json:"z"`
	W      float64      `json:"w"`
	H      float64      `json:"h"`
	Points [][2]float64 `json:"points"`
}

type model struct {
	Objects []object `json:"objects"`
	Routes  []route  `json:"routes"`
}

type view struct {
	eye, center ln.Vector
	fovy        float64
	// clip limits drawn geometry to a plan window (x0, y0, x1, y1) to keep
	// close-up renders fast; zero means no clip.
	clip [4]float64
}

var views = map[string]view{
	"overview":   {ln.Vector{-420, -780, 1150}, ln.Vector{1180, 760, 20}, 32, [4]float64{}},
	"powerblock": {ln.Vector{430, 70, 330}, ln.Vector{820, 560, 40}, 45, [4]float64{380, 280, 1480, 880}},
	"acc":        {ln.Vector{1720, 1130, 360}, ln.Vector{1250, 600, 50}, 40, [4]float64{980, 280, 1500, 900}},
	"ccs":        {ln.Vector{120, 380, 820}, ln.Vector{900, 1250, 110}, 42, [4]float64{400, 780, 1500, 1920}},
}

var skip = regexp.MustCompile(`rack bent|fan stack|radiator|Compound|lane$`)

func inClip(c [4]float64, x0, y0, x1, y1 float64) bool {
	if c == [4]float64{} {
		return true
	}
	return x1 >= c[0] && x0 <= c[2] && y1 >= c[1] && y0 <= c[3]
}

func build(m *model, v view, withOpt bool) *ln.Scene {
	scene := &ln.Scene{}
	up := ln.Vector{0, 0, 1}
	layerOK := func(l string) bool {
		if l == "SITE" {
			return true
		}
		return withOpt || !strings.HasPrefix(l, "OPT_")
	}
	for _, o := range m.Objects {
		if !layerOK(o.Layer) || skip.MatchString(o.Name) {
			continue
		}
		switch o.Kind {
		case "box", "prism":
			if !inClip(v.clip, o.Min[0], o.Min[1], o.Max[0], o.Max[1]) {
				continue
			}
			lo, hi := ln.Vector{o.Min[0], o.Min[1], o.Min[2]}, ln.Vector{o.Max[0], o.Max[1], o.Max[2]}
			if hi.Z-lo.Z < 0.2 {
				hi.Z = lo.Z + 0.2
			}
			if o.Kind == "prism" {
				scene.Add(prism(lo, hi))
			} else {
				scene.Add(ln.NewCube(lo, hi))
			}
		case "cyl":
			c := o.Center
			if !inClip(v.clip, c[0]-o.R, c[1]-o.R, c[0]+o.R, c[1]+o.R) {
				continue
			}
			scene.Add(ln.NewTransformedOutlineCylinder(v.eye, up,
				ln.Vector{c[0], c[1], o.Z0}, ln.Vector{c[0], c[1], o.Z1}, o.R))
		case "hcyl":
			if !inClip(v.clip, o.Min[0], o.Min[1], o.Max[0], o.Max[1]) {
				continue
			}
			zc := (o.Min[2] + o.Max[2]) / 2
			var a, b ln.Vector
			if o.Axis == "x" {
				yc := (o.Min[1] + o.Max[1]) / 2
				a, b = ln.Vector{o.Min[0], yc, zc}, ln.Vector{o.Max[0], yc, zc}
			} else {
				xc := (o.Min[0] + o.Max[0]) / 2
				a, b = ln.Vector{xc, o.Min[1], zc}, ln.Vector{xc, o.Max[1], zc}
			}
			scene.Add(ln.NewTransformedOutlineCylinder(v.eye, up, a, b, o.R))
		}
	}
	// routes above grade become thin boxes along each segment
	for _, r := range m.Routes {
		if !layerOK(r.Layer) || r.Z < 0 {
			continue
		}
		for i := 0; i+1 < len(r.Points); i++ {
			a, b := r.Points[i], r.Points[i+1]
			hw := r.W / 2
			x0, x1 := math.Min(a[0], b[0])-hw, math.Max(a[0], b[0])+hw
			y0, y1 := math.Min(a[1], b[1])-hw, math.Max(a[1], b[1])+hw
			if (x1-x0 > r.W+0.5 && y1-y0 > r.W+0.5) ||
				!inClip(v.clip, x0, y0, x1, y1) {
				continue // diagonal segment: skip (drawings are orthogonal)
			}
			scene.Add(ln.NewCube(ln.Vector{x0, y0, r.Z - r.H/2}, ln.Vector{x1, y1, r.Z + r.H/2}))
		}
	}
	return scene
}

// prism builds an A-frame (gable) solid with its ridge along Y.
func prism(lo, hi ln.Vector) ln.Shape {
	xm := (lo.X + hi.X) / 2
	a := ln.Vector{lo.X, lo.Y, lo.Z}
	b := ln.Vector{hi.X, lo.Y, lo.Z}
	c := ln.Vector{xm, lo.Y, hi.Z}
	d := ln.Vector{lo.X, hi.Y, lo.Z}
	e := ln.Vector{hi.X, hi.Y, lo.Z}
	f := ln.Vector{xm, hi.Y, hi.Z}
	t := []*ln.Triangle{
		ln.NewTriangle(a, b, c), ln.NewTriangle(d, f, e),
		ln.NewTriangle(a, c, f), ln.NewTriangle(a, f, d),
		ln.NewTriangle(b, e, f), ln.NewTriangle(b, f, c),
		ln.NewTriangle(a, d, e), ln.NewTriangle(a, e, b),
	}
	return &outlineMesh{ln.NewMesh(t), []ln.Path{{a, b, c, a}, {d, e, f, d}, {a, d}, {b, e}, {c, f}}}
}

// outlineMesh draws only the silhouette edges of a mesh instead of every
// triangle edge.
type outlineMesh struct {
	*ln.Mesh
	paths ln.Paths
}

func (m *outlineMesh) Paths() ln.Paths { return m.paths }

func main() {
	dir := flag.String("dir", "plant", "directory holding sk3x1_model.json")
	only := flag.String("view", "", "render one view: overview, powerblock, acc, ccs")
	withOpt := flag.Bool("opt", false, "include optional / adjacent-market systems")
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
	out := filepath.Join(*dir, "renders")
	os.MkdirAll(out, 0o755)

	names := []string{"overview", "powerblock", "acc", "ccs"}
	if *only != "" {
		names = []string{*only}
	}
	width, height := *size, *size*2/3
	for _, n := range names {
		v, ok := views[n]
		if !ok {
			fmt.Fprintln(os.Stderr, "unknown view:", n)
			os.Exit(2)
		}
		opt := *withOpt || n == "ccs"
		scene := build(&m, v, opt)
		paths := scene.Render(v.eye, v.center, ln.Vector{0, 0, 1}, width, height, v.fovy, 1, 20000, 0.5)
		base := filepath.Join(out, "sk3x1_"+n)
		if opt && n != "ccs" {
			base += "_opt"
		}
		paths.WriteToSVG(base+".svg", width, height)
		paths.WriteToPNG(base+".png", width, height)
		fmt.Printf("%-11s %6d paths -> %s.{svg,png}\n", n, len(paths), base)
	}
}
