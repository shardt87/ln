// oemcards renders the OEM equipment picture cards — one tight hidden-line
// close-up per package — from the caller-power CCGT plant GLB, using ln as the
// presentation renderer (vector paths, real occlusion, anti-aliased strokes).
//
// It reproduces the framing and part selection of the handoff's oemcards.py:
// same package keys, same camera az/el, same pad, same roof-drop and
// below-grade hide rules, same output names (oem_<KEY>.png) and the same
// oemcards.json metadata, so mkoemcards.py / mkoemxl.py rebuild the PDF and
// Excel against the new images unchanged.
//
// Usage:
//
//	oemcards -glb caller-power-ccgt-rev89-full-cable-families.glb -out outdir
//	oemcards -glb model.glb -out outdir -keys GT,HRSG,STG   # subset
//	oemcards -list                                          # list package keys
package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"math"
	"os"
	"path/filepath"
	"runtime"
	"sort"
	"strings"
	"sync"
	"time"

	"github.com/fogleman/gg"
	"github.com/fogleman/ln/ln"
)

const mToFt = 1 / 0.3048

type cardMeta struct {
	PNG     string  `json:"png"`
	SpanFt  float64 `json:"span_ft"`
	Visible int     `json:"visible"`
	Parts   int     `json:"parts"`
	W       int     `json:"W"`
	H       int     `json:"H"`
	Secs    int     `json:"secs"`
}

func main() {
	glbPath := flag.String("glb", "", "path to the plant GLB")
	outDir := flag.String("out", ".", "output directory")
	keysFlag := flag.String("keys", "", "comma-separated package keys (default: all)")
	width := flag.Int("w", 3600, "output width in pixels")
	height := flag.Int("h", 2550, "output height in pixels")
	feature := flag.Float64("angle", 30, "feature-edge dihedral threshold in degrees")
	lineWidth := flag.Float64("lw", 3, "stroke width in pixels")
	svg := flag.Bool("svg", true, "also write SVG next to each PNG")
	jobs := flag.Int("j", runtime.NumCPU(), "cards rendered in parallel")
	list := flag.Bool("list", false, "list package keys and exit")
	flag.Parse()

	if *list {
		for _, d := range pkgs {
			fmt.Printf("%-10s %v\n", d.Key, d.Prefixes)
		}
		return
	}
	if *glbPath == "" {
		fmt.Fprintln(os.Stderr, "usage: oemcards -glb model.glb -out dir [-keys GT,HRSG,...]")
		os.Exit(2)
	}

	g, err := LoadGLB(*glbPath)
	die(err)
	parts, err := g.Parts()
	die(err)
	fmt.Printf("loaded %s: %d parts\n", filepath.Base(*glbPath), len(parts))
	if err := os.MkdirAll(*outDir, 0755); err != nil {
		die(err)
	}

	selected := pkgs
	if *keysFlag != "" {
		byKey := map[string]pkgDef{}
		for _, d := range pkgs {
			byKey[d.Key] = d
		}
		selected = nil
		for _, k := range strings.Split(*keysFlag, ",") {
			k = strings.TrimSpace(k)
			d, ok := byKey[k]
			if !ok {
				die(fmt.Errorf("unknown package key %q (see -list)", k))
			}
			selected = append(selected, d)
		}
	}

	db := map[string]cardMeta{}
	jsPath := filepath.Join(*outDir, "oemcards.json")
	if raw, err := os.ReadFile(jsPath); err == nil {
		json.Unmarshal(raw, &db)
	}
	var mu sync.Mutex
	sem := make(chan struct{}, max(1, *jobs))
	var wg sync.WaitGroup
	for _, d := range selected {
		wg.Add(1)
		go func(d pkgDef) {
			defer wg.Done()
			sem <- struct{}{}
			defer func() { <-sem }()
			meta, err := shot(parts, d, *outDir, *width, *height, *feature, *lineWidth, *svg)
			if err != nil {
				fmt.Printf("  %-10s SKIPPED: %v\n", d.Key, err)
				return
			}
			mu.Lock()
			db[d.Key] = *meta
			writeJSON(jsPath, db)
			mu.Unlock()
			fmt.Printf("  %-10s %3ds  span %5.1f' drawn  pkg parts %3d  vis %4d\n",
				d.Key, meta.Secs, meta.SpanFt, meta.Parts, meta.Visible)
		}(d)
	}
	wg.Wait()
}

// shot renders one package close-up, mirroring oemcards.py shot().
func shot(parts []*Part, d pkgDef, outDir string, W, H int, featureDeg, lw float64, svg bool) (*cardMeta, error) {
	start := time.Now()

	var tgt []*Part
	for _, p := range parts {
		if hasAnyPrefix(p.Name, d.Prefixes) {
			tgt = append(tgt, p)
		}
	}
	if len(tgt) == 0 {
		return nil, fmt.Errorf("no parts for %v", d.Prefixes)
	}

	// Crop box: target bounds padded by pad ft, floor pulled to at least -1 ft.
	pad := d.PadFt / mToFt
	lo := [3]float64{math.Inf(1), math.Inf(1), math.Inf(1)}
	hi := [3]float64{math.Inf(-1), math.Inf(-1), math.Inf(-1)}
	for _, p := range tgt {
		for a := 0; a < 3; a++ {
			lo[a] = math.Min(lo[a], p.Min[a]-pad)
			hi[a] = math.Max(hi[a], p.Max[a]+pad)
		}
	}
	lo[1] = math.Min(lo[1], -1.0/mToFt)

	// Keep set: parts whose centroid falls in the crop box, plus ground
	// context, minus below-grade parts and (for interior packages) the hall
	// roof/shell.
	var keep []*Part
	for _, p := range parts {
		if isUnderground(p) || (d.DropRoof && isRoof(p.Name)) {
			continue
		}
		c := [3]float64{
			(p.Min[0] + p.Max[0]) / 2,
			(p.Min[1] + p.Max[1]) / 2,
			(p.Min[2] + p.Max[2]) / 2,
		}
		inside := true
		for a := 0; a < 3; a++ {
			if c[a] < lo[a] || c[a] > hi[a] {
				inside = false
				break
			}
		}
		if inside || isGroundContext(p.Name) {
			keep = append(keep, p)
		}
	}

	// Camera basis from az/el, matching render.py project(): the eye direction
	// is (sin az * cos el, sin el, cos az * cos el) with +Y up.
	az, el := d.Az*math.Pi/180, d.El*math.Pi/180
	eyeDir := ln.Vector{
		X: math.Sin(az) * math.Cos(el),
		Y: math.Sin(el),
		Z: math.Cos(az) * math.Cos(el),
	}.Normalize()
	up := ln.Vector{Y: 1}

	// Frame: fit the 8 corners of the crop box with a 4% margin, centred
	// (pad=0.04, vo=0.5 in render.py terms).
	center := ln.Vector{X: (lo[0] + hi[0]) / 2, Y: (lo[1] + hi[1]) / 2, Z: (lo[2] + hi[2]) / 2}
	right := up.Cross(eyeDir).Normalize()
	camUp := eyeDir.Cross(right)
	uMin, uMax := math.Inf(1), math.Inf(-1)
	vMin, vMax := math.Inf(1), math.Inf(-1)
	for _, x := range []float64{lo[0], hi[0]} {
		for _, y := range []float64{lo[1], hi[1]} {
			for _, z := range []float64{lo[2], hi[2]} {
				p := ln.Vector{X: x, Y: y, Z: z}.Sub(center)
				u, v := p.Dot(right), p.Dot(camUp)
				uMin, uMax = math.Min(uMin, u), math.Max(uMax, u)
				vMin, vMax = math.Min(vMin, v), math.Max(vMax, v)
			}
		}
	}
	const margin = 0.04
	su := float64(W) * (1 - 2*margin) / (uMax - uMin)
	sv := float64(H) * (1 - 2*margin) / (vMax - vMin)
	s := math.Min(su, sv) // pixels per metre
	halfW, halfH := float64(W)/s/2, float64(H)/s/2
	cu, cv := (uMin+uMax)/2, (vMin+vMax)/2

	// Scene radius for eye distance and near/far planes.
	radius := 0.0
	for _, p := range keep {
		for a := 0; a < 3; a++ {
			radius = math.Max(radius, math.Abs(p.Min[a]-vecAt(center, a)))
			radius = math.Max(radius, math.Abs(p.Max[a]-vecAt(center, a)))
		}
	}
	radius = math.Max(radius*math.Sqrt(3), 1)
	eye := center.Add(eyeDir.MulScalar(radius * 4))

	scene := ln.Scene{}
	cosFeature := math.Cos(featureDeg * math.Pi / 180)
	shapes := make([]*edgeShape, len(keep))
	var bwg sync.WaitGroup
	for i, p := range keep {
		bwg.Add(1)
		go func(i int, p *Part) {
			defer bwg.Done()
			shapes[i] = newEdgeShape(p, buildPartEdges(p), eyeDir, cosFeature)
		}(i, p)
	}
	bwg.Wait()
	for _, sh := range shapes {
		scene.Add(sh)
	}
	scene.Compile()

	view := ln.LookAt(eye, center, up)
	matrix := view.Orthographic(cu-halfW, cu+halfW, cv-halfH, cv+halfH,
		radius, radius*8)

	// Per-shape render (Scene.RenderWithMatrix, unrolled) so visible parts can
	// be counted the way the raster renderer counted its id-buffer.
	step := (float64(W) / s) / 2000 // chop for occlusion sampling: frame width / 2000
	filter := &ln.ClipFilter{Matrix: matrix, Eye: eye, Scene: &scene}
	screen := ln.Translate(ln.Vector{X: 1, Y: 1}).Scale(ln.Vector{X: float64(W) / 2, Y: float64(H) / 2})
	var paths ln.Paths
	visible := 0
	for _, sh := range shapes {
		pp := sh.Paths()
		if len(pp) == 0 {
			continue
		}
		pp = pp.Chop(step).Filter(filter)
		if len(pp) == 0 {
			continue
		}
		visible++
		paths = append(paths, pp.Simplify(1e-6).Transform(screen)...)
	}

	pngPath := filepath.Join(outDir, "oem_"+d.Key+".png")
	if err := writePNG(pngPath, paths, W, H, lw); err != nil {
		return nil, err
	}
	if svg {
		if err := paths.WriteToSVG(strings.TrimSuffix(pngPath, ".png")+".svg",
			float64(W), float64(H)); err != nil {
			return nil, err
		}
	}
	abs, err := filepath.Abs(pngPath)
	if err != nil {
		abs = pngPath
	}
	return &cardMeta{
		PNG:     abs,
		SpanFt:  math.Round(float64(W)/s*mToFt*10) / 10,
		Visible: visible,
		Parts:   len(tgt),
		W:       W,
		H:       H,
		Secs:    int(math.Round(time.Since(start).Seconds())),
	}, nil
}

func writePNG(path string, paths ln.Paths, w, h int, lw float64) error {
	dc := gg.NewContext(w, h)
	dc.InvertY()
	dc.SetRGB(1, 1, 1)
	dc.Clear()
	dc.SetRGB(0.08, 0.09, 0.10)
	dc.SetLineWidth(lw)
	dc.SetLineCapRound()
	dc.SetLineJoinRound()
	for _, p := range paths {
		for _, v := range p {
			dc.LineTo(v.X, v.Y)
		}
		dc.NewSubPath()
	}
	dc.Stroke()
	return dc.SavePNG(path)
}

func writeJSON(path string, db map[string]cardMeta) {
	keys := make([]string, 0, len(db))
	for k := range db {
		keys = append(keys, k)
	}
	sort.Strings(keys)
	ordered := make(map[string]cardMeta, len(db))
	for _, k := range keys {
		ordered[k] = db[k]
	}
	raw, _ := json.MarshalIndent(ordered, "", " ")
	os.WriteFile(path, raw, 0644)
}

func die(err error) {
	if err != nil {
		fmt.Fprintln(os.Stderr, "oemcards:", err)
		os.Exit(1)
	}
}

func vecAt(v ln.Vector, a int) float64 {
	switch a {
	case 0:
		return v.X
	case 1:
		return v.Y
	}
	return v.Z
}
