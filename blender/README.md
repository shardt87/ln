# Blender power plant generator

`power_plant.py` builds a coal-fired power plant procedurally: two natural-draft
cooling towers, a turbine hall, a boiler house, tapered chimneys with warning
bands, storage tanks and the pipe runs between them. Nothing is modelled by
hand, so the layout is just numbers in `build_scene()`.

Everything is created from mesh data directly (a `box` helper and one
surface-of-revolution helper), with no edit-mode operators, so it runs the same
in the GUI and in a headless/background session.

## Running it

With a Blender install:

	blender -b -P blender/power_plant.py -- --blend plant.blend

Or with the [`bpy`](https://pypi.org/project/bpy/) module, no Blender needed:

	pip install bpy
	python3 blender/power_plant.py --render plant.png

Options:

| flag | effect |
| --- | --- |
| `--obj PATH` | export the scene as OBJ |
| `--blend PATH` | save a .blend file |
| `--render PATH` | render a still with Cycles |
| `--samples N` | render samples (default 48) |
| `--resolution W H` | render size (default 1280x720) |
| `--detail F` | scale every segment count; `0.35` gives a low-poly mesh |
| `--no-steam` | omit the steam plumes |

The camera frames whatever the scene bounding box turns out to be, so moving
buildings around does not mean re-aiming it.

## Feeding it to `ln`

The OBJ export drops straight into this repo's renderer. Low `--detail` values
are what you want here — `ln` draws every triangle edge, so a dense mesh comes
out solid black:

	python3 blender/power_plant.py --detail 0.35 --no-steam --obj examples/power_plant.obj
	go run examples/powerplant.go
