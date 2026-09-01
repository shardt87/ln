// Hand-rolled GLB (binary glTF 2.0) reader, ported from the handoff's glb.py.
// Reads only what the OEM cards need: the scene graph flattened to named parts
// with world-space triangles. Honours byteStride (interleaved buffers exist in
// the rev89 bake). All transforms in that bake are identity, but TRS/matrix
// nodes are applied anyway so the loader is not bake-specific.
package main

import (
	"encoding/binary"
	"encoding/json"
	"fmt"
	"math"
	"os"
)

const (
	glbMagic   = 0x46546C67
	chunkJSON  = 0x4E4F534A
	chunkBIN   = 0x004E4942
	compByte   = 5120
	compUByte  = 5121
	compShort  = 5122
	compUShort = 5123
	compUInt   = 5125
	compFloat  = 5126
)

var compSize = map[int]int{
	compByte: 1, compUByte: 1, compShort: 2, compUShort: 2, compUInt: 4, compFloat: 4,
}

var typeComps = map[string]int{
	"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16,
}

type gltfAccessor struct {
	BufferView    *int   `json:"bufferView"`
	ByteOffset    int    `json:"byteOffset"`
	ComponentType int    `json:"componentType"`
	Count         int    `json:"count"`
	Type          string `json:"type"`
}

type gltfBufferView struct {
	ByteOffset int `json:"byteOffset"`
	ByteLength int `json:"byteLength"`
	ByteStride int `json:"byteStride"`
}

type gltfPrimitive struct {
	Attributes map[string]int `json:"attributes"`
	Indices    *int           `json:"indices"`
	Material   *int           `json:"material"`
}

type gltfMesh struct {
	Primitives []gltfPrimitive `json:"primitives"`
}

type gltfNode struct {
	Name        string    `json:"name"`
	Mesh        *int      `json:"mesh"`
	Children    []int     `json:"children"`
	Matrix      []float64 `json:"matrix"`
	Rotation    []float64 `json:"rotation"`
	Scale       []float64 `json:"scale"`
	Translation []float64 `json:"translation"`
}

type gltfScene struct {
	Nodes []int `json:"nodes"`
}

type gltfDoc struct {
	Accessors   []gltfAccessor   `json:"accessors"`
	BufferViews []gltfBufferView `json:"bufferViews"`
	Meshes      []gltfMesh       `json:"meshes"`
	Nodes       []gltfNode       `json:"nodes"`
	Scene       int              `json:"scene"`
	Scenes      []gltfScene      `json:"scenes"`
}

// Part is one mesh primitive of one node: a named bag of world-space triangles.
type Part struct {
	Name string
	V    [][3]float64 // world metres
	I    [][3]int
	Min  [3]float64
	Max  [3]float64
}

type GLB struct {
	doc *gltfDoc
	bin []byte
}

func LoadGLB(path string) (*GLB, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}
	if len(data) < 12 || binary.LittleEndian.Uint32(data) != glbMagic {
		return nil, fmt.Errorf("%s: not a GLB", path)
	}
	length := int(binary.LittleEndian.Uint32(data[8:]))
	if length > len(data) {
		length = len(data)
	}
	g := &GLB{}
	for off := 12; off+8 <= length; {
		clen := int(binary.LittleEndian.Uint32(data[off:]))
		ctype := binary.LittleEndian.Uint32(data[off+4:])
		off += 8
		if off+clen > len(data) {
			return nil, fmt.Errorf("%s: truncated chunk", path)
		}
		payload := data[off : off+clen]
		switch ctype {
		case chunkJSON:
			g.doc = &gltfDoc{}
			if err := json.Unmarshal(payload, g.doc); err != nil {
				return nil, err
			}
		case chunkBIN:
			g.bin = payload
		}
		off += clen
	}
	if g.doc == nil {
		return nil, fmt.Errorf("%s: no JSON chunk", path)
	}
	return g, nil
}

// accessorFloats returns accessor i as a flat []float64 (count*ncomp values),
// converting integer component types to their numeric value.
func (g *GLB) accessorFloats(i int) ([]float64, int, error) {
	a := g.doc.Accessors[i]
	nc := typeComps[a.Type]
	esz := compSize[a.ComponentType] * nc
	out := make([]float64, a.Count*nc)
	if a.BufferView == nil {
		return out, nc, nil
	}
	bv := g.doc.BufferViews[*a.BufferView]
	base := bv.ByteOffset + a.ByteOffset
	stride := bv.ByteStride
	if stride == 0 {
		stride = esz
	}
	for k := 0; k < a.Count; k++ {
		rec := g.bin[base+k*stride:]
		for c := 0; c < nc; c++ {
			b := rec[c*compSize[a.ComponentType]:]
			switch a.ComponentType {
			case compFloat:
				out[k*nc+c] = float64(math.Float32frombits(binary.LittleEndian.Uint32(b)))
			case compUInt:
				out[k*nc+c] = float64(binary.LittleEndian.Uint32(b))
			case compUShort:
				out[k*nc+c] = float64(binary.LittleEndian.Uint16(b))
			case compShort:
				out[k*nc+c] = float64(int16(binary.LittleEndian.Uint16(b)))
			case compUByte:
				out[k*nc+c] = float64(b[0])
			case compByte:
				out[k*nc+c] = float64(int8(b[0]))
			}
		}
	}
	return out, nc, nil
}

type mat4 [16]float64 // row-major

func matIdentity() mat4 {
	return mat4{1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1}
}

func (a mat4) mul(b mat4) mat4 {
	var m mat4
	for r := 0; r < 4; r++ {
		for c := 0; c < 4; c++ {
			s := 0.0
			for k := 0; k < 4; k++ {
				s += a[r*4+k] * b[k*4+c]
			}
			m[r*4+c] = s
		}
	}
	return m
}

func (a mat4) isIdentity() bool {
	id := matIdentity()
	for i := range a {
		if math.Abs(a[i]-id[i]) > 1e-12 {
			return false
		}
	}
	return true
}

func nodeMatrix(n *gltfNode) mat4 {
	if len(n.Matrix) == 16 {
		// glTF stores column-major; transpose into row-major.
		var m mat4
		for r := 0; r < 4; r++ {
			for c := 0; c < 4; c++ {
				m[r*4+c] = n.Matrix[c*4+r]
			}
		}
		return m
	}
	m := matIdentity()
	if len(n.Scale) == 3 {
		s := mat4{n.Scale[0], 0, 0, 0, 0, n.Scale[1], 0, 0, 0, 0, n.Scale[2], 0, 0, 0, 0, 1}
		m = s.mul(m)
	}
	if len(n.Rotation) == 4 {
		x, y, z, w := n.Rotation[0], n.Rotation[1], n.Rotation[2], n.Rotation[3]
		r := mat4{
			1 - 2*(y*y+z*z), 2 * (x*y - z*w), 2 * (x*z + y*w), 0,
			2 * (x*y + z*w), 1 - 2*(x*x+z*z), 2 * (y*z - x*w), 0,
			2 * (x*z - y*w), 2 * (y*z + x*w), 1 - 2*(x*x+y*y), 0,
			0, 0, 0, 1,
		}
		m = r.mul(m)
	}
	if len(n.Translation) == 3 {
		t := matIdentity()
		t[3], t[7], t[11] = n.Translation[0], n.Translation[1], n.Translation[2]
		m = t.mul(m)
	}
	return m
}

// Parts flattens the scene graph to named parts with world-space triangles.
func (g *GLB) Parts() ([]*Part, error) {
	var out []*Part
	doc := g.doc
	var walk func(ni int, parent mat4) error
	walk = func(ni int, parent mat4) error {
		node := &doc.Nodes[ni]
		m := parent.mul(nodeMatrix(node))
		name := node.Name
		if name == "" {
			name = fmt.Sprintf("node%d", ni)
		}
		if node.Mesh != nil {
			for _, prim := range doc.Meshes[*node.Mesh].Primitives {
				pi, ok := prim.Attributes["POSITION"]
				if !ok {
					continue
				}
				pos, nc, err := g.accessorFloats(pi)
				if err != nil {
					return err
				}
				if nc != 3 {
					continue
				}
				nv := len(pos) / 3
				p := &Part{Name: name, V: make([][3]float64, nv)}
				ident := m.isIdentity()
				for k := 0; k < nv; k++ {
					x, y, z := pos[k*3], pos[k*3+1], pos[k*3+2]
					if !ident {
						x2 := m[0]*x + m[1]*y + m[2]*z + m[3]
						y2 := m[4]*x + m[5]*y + m[6]*z + m[7]
						z2 := m[8]*x + m[9]*y + m[10]*z + m[11]
						x, y, z = x2, y2, z2
					}
					p.V[k] = [3]float64{x, y, z}
				}
				if prim.Indices != nil {
					idx, _, err := g.accessorFloats(*prim.Indices)
					if err != nil {
						return err
					}
					p.I = make([][3]int, 0, len(idx)/3)
					for k := 0; k+2 < len(idx); k += 3 {
						p.I = append(p.I, [3]int{int(idx[k]), int(idx[k+1]), int(idx[k+2])})
					}
				} else {
					p.I = make([][3]int, 0, nv/3)
					for k := 0; k+2 < nv; k += 3 {
						p.I = append(p.I, [3]int{k, k + 1, k + 2})
					}
				}
				p.computeBounds()
				out = append(out, p)
			}
		}
		for _, c := range node.Children {
			if err := walk(c, m); err != nil {
				return err
			}
		}
		return nil
	}
	si := doc.Scene
	if si >= len(doc.Scenes) {
		si = 0
	}
	for _, ni := range doc.Scenes[si].Nodes {
		if err := walk(ni, matIdentity()); err != nil {
			return nil, err
		}
	}
	return out, nil
}

func (p *Part) computeBounds() {
	for a := 0; a < 3; a++ {
		p.Min[a], p.Max[a] = math.Inf(1), math.Inf(-1)
	}
	for _, v := range p.V {
		for a := 0; a < 3; a++ {
			p.Min[a] = math.Min(p.Min[a], v[a])
			p.Max[a] = math.Max(p.Max[a], v[a])
		}
	}
}
