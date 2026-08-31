# Headless Blender rendering for glTF/GLB models

`render_glb.py` produces beauty renders of a 3D model file (`.glb`, `.gltf`,
`.obj`, `.stl`, `.fbx`, `.ply`) from the command line, with no Blender UI and no
manual scene setup. It builds the whole shot automatically:

- **Auto-framed camera** — the camera is fit to the scene bounding box with
  `camera_fit_coords`, so any model is fully in frame at any aspect ratio.
  Azimuth, elevation, FOV and framing margin are all CLI flags.
- **Physically based lighting** — a Nishita sky dome plus a matching sun lamp,
  with optional fill and rim area lights scaled to the model size.
- **Cycles path tracing** — adaptive sampling, OpenImageDenoise denoising,
  and AgX tone mapping (EEVEE is available as a fast fallback via `--engine`).
- **Multi-view stills and turntables** — render several azimuths in one run
  (`--views 45,135,225`) or a full orbit PNG sequence (`--turntable 120`).

The scene/light/camera building blocks are adapted from well-known open-source
Blender CLI rendering repositories, primarily
[yuki-koyama/blender-cli-rendering](https://github.com/yuki-koyama/blender-cli-rendering)
and [njanakiev/blender-scripting](https://github.com/njanakiev/blender-scripting).

## Requirements

Either a regular Blender install (4.2+), or the pip-installed `bpy` module
(requires the matching Python version, e.g. Python 3.11 for bpy 4.x/5.x):

```sh
pip install bpy
```

## Usage

With Blender:

```sh
blender -b -P scripts/blender/render_glb.py -- \
    --input model.glb --output out/render.png
```

With the `bpy` module:

```sh
python scripts/blender/render_glb.py --input model.glb --output out/render.png
```

Common options:

| Flag | Default | Meaning |
| --- | --- | --- |
| `--width` / `--height` | 1920 / 1080 | output resolution |
| `--samples` | 128 | Cycles max samples (adaptive) |
| `--engine` | `cycles` | `cycles` or `eevee` |
| `--views` | `45` | comma-separated camera azimuths (degrees) |
| `--elevation` | 30 | camera elevation (degrees) |
| `--fov` | 35 | horizontal field of view (degrees) |
| `--margin` | 1.06 | framing margin, >1 zooms out |
| `--sun-elevation` / `--sun-azimuth` | 42 / 160 | sun position (degrees) |
| `--sun-strength` | 3.0 | sun lamp energy |
| `--sky-strength` | 1.0 | sky dome brightness |
| `--exposure` | 0.4 | film exposure |
| `--transparent` | off | transparent background PNG |
| `--no-fill` | off | disable fill/rim lights (sun + sky only) |
| `--turntable N` | 0 | render an N-frame orbit instead of stills |

Example — three views of a site model with a slightly dimmer sun:

```sh
python scripts/blender/render_glb.py \
    --input site.glb --output out/site.png \
    --views 45,135,225 --exposure -0.3 --sun-strength 2.5
```
