SW-3X1 3x1 combined-cycle plant, Rev 14 plus the modular expansion layer (design change).
Units: feet in the model; the Blender/GLB/USDZ files are in metres (Blender units), X east, north = -Z in GLB (Y-up).

SW-3X1_plant.glb        glTF 2.0: most 3D viewers, web, PowerPoint (Insert > 3D Models), Windows 3D Viewer
SW-3X1_plant.usdz       iPhone / iPad: tap to open in AR Quick Look
SW-3X1_plant.blend      Blender 4.2+: pro materials, sun/sky, all cameras (P1-P11 plates, E1-E8 epic)
SW-3X1_coastal_A.glb / .usdz / .blend   coastal variant (sheet 15, placed north of the plant): the plant plus the onshore LNG import terminal,
                        1,740 ft jetty, berth, 294 m LNG carrier, tugs and a trimmed sea plane
sw3x1_model.obj + .mtl  SketchUp, Rhino, Revit, 3ds Max: one group per item, layer in the group name (feet, Z up)

Downloads:
  SW-3X1_plant_only.zip   plant only (inland, sheets 01-14): README, SW-3X1_plant.glb, SW-3X1_plant.blend
  SW-3X1_coastal_A.zip    coastal variant (sheet 15): the plant PLUS the LNG import terminal, jetty, berth and
                          carrier: README, SW-3X1_coastal_A.glb, SW-3X1_coastal_A.blend
  SW-3X1_plant_datacenter.zip  add-on: the plant PLUS the ~150 MW BTM data centre beside the modular yard
  SW-3X1_3D_model.zip     everything above plus USDZ and OBJ / MTL
Object names: "<tag or name> [<item id>]", at most 63 characters (a Blender limit). Long names are shortened
with "..." but the item id is always complete; the full name, layer, tag, area, sheet, info and wiring of every
object are in its custom properties (glTF node "extras", Blender Object Properties > Custom Properties).
The OBJ group names carry the full name.

Conceptual illustration. Not engineered. Not for construction.
Stephan Hardt | Power Generation Solutions

Oct 18, 2026: the GLB / USDZ here are current (the Oct 17-18 work: slate HRSGs, black-copper hall, ST detail,
interior electrical, wall sign and flag) and carry every printed decal and screen as an image (USDZ included).
Each file is under GitHub's 100 MiB limit (GLB 94.8-101.1 MB, USDZ 88.9-93.4 MB): the export drops the end caps of
thin rods (cable, conduit, rail: they sit inside the next segment or a gland) and of straight rod joints, and faces
buried under the ground, and merges the decal quads; renders of old and new files match (blender/export_slim.py). The .blend files are complete and untrimmed.
