// Line extraction: instead of drawing every triangle edge (which buries a
// tessellated cylinder under its own wireframe), a part is drawn as
//   - boundary edges (used by exactly one triangle),
//   - feature edges (dihedral angle above a threshold),
//   - silhouette edges for the current view (front-facing meets back-facing),
//
// and the ln scene does the hidden-line removal against the full keep set.
package main

import (
	"math"

	"github.com/fogleman/ln/ln"
)

// weld quantum in metres — merges float32 vertices that should be identical.
const weldQ = 1e-4

type edgeFaces struct {
	a, b int // vertex ids
	n    [][3]float64
}

type partEdges struct {
	verts []ln.Vector
	edges []edgeFaces
}

func buildPartEdges(p *Part) *partEdges {
	qkey := func(v [3]float64) [3]int64 {
		return [3]int64{
			int64(math.Round(v[0] / weldQ)),
			int64(math.Round(v[1] / weldQ)),
			int64(math.Round(v[2] / weldQ)),
		}
	}
	vid := make(map[[3]int64]int)
	var verts []ln.Vector
	remap := make([]int, len(p.V))
	for i, v := range p.V {
		k := qkey(v)
		id, ok := vid[k]
		if !ok {
			id = len(verts)
			vid[k] = id
			verts = append(verts, ln.Vector{X: v[0], Y: v[1], Z: v[2]})
		}
		remap[i] = id
	}
	type ekey struct{ a, b int }
	em := make(map[ekey]*edgeFaces)
	addEdge := func(a, b int, n [3]float64) {
		if a == b {
			return
		}
		if a > b {
			a, b = b, a
		}
		k := ekey{a, b}
		e, ok := em[k]
		if !ok {
			e = &edgeFaces{a: a, b: b}
			em[k] = e
		}
		e.n = append(e.n, n)
	}
	for _, t := range p.I {
		i0, i1, i2 := remap[t[0]], remap[t[1]], remap[t[2]]
		if i0 == i1 || i1 == i2 || i0 == i2 {
			continue
		}
		v0, v1, v2 := verts[i0], verts[i1], verts[i2]
		n := v1.Sub(v0).Cross(v2.Sub(v0))
		l := n.Length()
		if l < 1e-12 {
			continue
		}
		n = n.DivScalar(l)
		nn := [3]float64{n.X, n.Y, n.Z}
		addEdge(i0, i1, nn)
		addEdge(i1, i2, nn)
		addEdge(i2, i0, nn)
	}
	pe := &partEdges{verts: verts}
	for _, e := range em {
		pe.edges = append(pe.edges, *e)
	}
	return pe
}

// paths returns the drawable edges for a view direction (unit vector toward
// the camera), split into two weights the way a technical drawing inks them:
// heavy for object outlines (boundary and view silhouette), light for interior
// feature edges (sharp dihedrals). cosFeature = cos(feature angle threshold).
func (pe *partEdges) paths(view ln.Vector, cosFeature float64) (heavy, light ln.Paths) {
	for _, e := range pe.edges {
		outline, feature := false, false
		switch len(e.n) {
		case 1:
			outline = true // boundary
		default:
			for i := 1; i < len(e.n) && !outline; i++ {
				n0, ni := e.n[0], e.n[i]
				f0 := n0[0]*view.X + n0[1]*view.Y + n0[2]*view.Z
				fi := ni[0]*view.X + ni[1]*view.Y + ni[2]*view.Z
				if (f0 >= 0) != (fi >= 0) {
					outline = true // silhouette for this view
					break
				}
				dot := n0[0]*ni[0] + n0[1]*ni[1] + n0[2]*ni[2]
				if dot < cosFeature {
					feature = true // sharp dihedral
				}
			}
		}
		seg := ln.Path{pe.verts[e.a], pe.verts[e.b]}
		if outline {
			heavy = append(heavy, seg)
		} else if feature {
			light = append(light, seg)
		}
	}
	return heavy, light
}

// edgeShape wraps a part's triangle mesh (for occlusion ray tests) but emits
// only the extracted line-art edges as paths.
type edgeShape struct {
	mesh  *ln.Mesh
	heavy ln.Paths
	light ln.Paths
}

func newEdgeShape(p *Part, pe *partEdges, view ln.Vector, cosFeature float64) *edgeShape {
	triangles := make([]*ln.Triangle, 0, len(p.I))
	for _, t := range p.I {
		v0, v1, v2 := p.V[t[0]], p.V[t[1]], p.V[t[2]]
		triangles = append(triangles, ln.NewTriangle(
			ln.Vector{X: v0[0], Y: v0[1], Z: v0[2]},
			ln.Vector{X: v1[0], Y: v1[1], Z: v1[2]},
			ln.Vector{X: v2[0], Y: v2[1], Z: v2[2]},
		))
	}
	heavy, light := pe.paths(view, cosFeature)
	return &edgeShape{mesh: ln.NewMesh(triangles), heavy: heavy, light: light}
}

func (s *edgeShape) Compile()                             { s.mesh.Compile() }
func (s *edgeShape) BoundingBox() ln.Box                  { return s.mesh.BoundingBox() }
func (s *edgeShape) Contains(v ln.Vector, f float64) bool { return false }
func (s *edgeShape) Intersect(r ln.Ray) ln.Hit            { return s.mesh.Intersect(r) }
func (s *edgeShape) Paths() ln.Paths                      { return append(append(ln.Paths{}, s.heavy...), s.light...) }
