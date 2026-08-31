package main

import "github.com/fogleman/ln/ln"

// Renders the mesh produced by blender/power_plant.py. Generate it first:
//
//	python3 blender/power_plant.py --detail 0.35 --no-steam \
//	    --obj examples/power_plant.obj
func main() {
	scene := ln.Scene{}
	mesh, err := ln.LoadOBJ("examples/power_plant.obj")
	if err != nil {
		panic(err)
	}
	scene.Add(mesh)
	eye := ln.Vector{120, -140, 70}
	center := ln.Vector{-8, -12, 22}
	up := ln.Vector{0, 0, 1}
	width := 1024.0
	height := 640.0
	paths := scene.Render(eye, center, up, width, height, 40, 0.1, 1000, 0.01)
	paths.WriteToPNG("out.png", width, height)
	paths.Print()
}
