# oemcards — OEM equipment picture-card renderer

Renders the OEM equipment close-ups for the caller-power CCGT plant model as
hidden-line vector art, using `ln` as the presentation renderer. This replaces
the in-container CPU rasteriser from the handoff (`oemcards.py` / `render.py`):
same framing, same part selection, same outputs — but real vector linework
with anti-aliased strokes and an SVG next to every PNG.

## Usage

```sh
go run ./cmd/oemcards -glb caller-power-ccgt-rev89-full-cable-families.glb -out outputs
```

Renders all 47 package close-ups as `oem_<KEY>.png` (3600x2550) plus
`oem_<KEY>.svg`, and writes `oemcards.json` metadata compatible with the
handoff's `mkoemcards.py` (PDF picture cards) and `mkoemxl.py` (Excel) — run
those against the output directory unchanged to rebuild the deliverables.

Options:

- `-keys GT,HRSG,STG` — render a subset (see `-list` for all keys)
- `-w`, `-h` — raster size (default 3600x2550)
- `-angle` — feature-edge dihedral threshold in degrees (default 30)
- `-lw` — stroke width in pixels (default 3)
- `-svg=false` — skip the SVG output
- `-j` — cards rendered in parallel (default: number of CPUs)

## What it carries over from the handoff

- **`PKG` map** (`pkg.go`): package key → name prefixes that ARE the package,
  camera azimuth/elevation, pad in drawn feet, drop-roof flag. Ported verbatim
  from `oemcards.py`.
- **Hide rules**: hall roof/shell prefixes for interior packages; below-grade
  parts (`EXCAV-*`, `ZONE-*`, anything with max y < 0.05 ft except
  `site-base`).
- **Ground context**: `site-base`, roads, aprons and `*-pad` parts are kept
  regardless of the crop box.
- **Framing**: the crop box is the padded target bounds (floor pulled to at
  least −1 ft), fitted with a 4% margin, orthographic, matching
  `render.py project()` (same camera basis: az 0 looks from +z, +Y up).
- **Metadata**: `oemcards.json` with `png`, `span_ft` (drawn feet; true feet =
  drawn × 2.40), `visible`, `parts`, `W`, `H`, `secs` per key.

## How the linework is drawn

Every kept part becomes an occluder (its full triangle mesh goes into the ln
BVH), but only three kinds of edges are inked:

- boundary edges (used by one triangle),
- feature edges (dihedral angle above `-angle`),
- silhouette edges for the card's view (front-facing meets back-facing).

So a tessellated cylinder reads as its outline, not its wireframe, and hidden
lines are removed by real ray tests against everything in frame.

## Testing without the plant model

`testdata/mktestglb.py` (pure Python stdlib) writes a small GLB in the same
schema — named parts, identity transforms, metres, y-up — with enough geometry
to exercise the prefixes, roof drop, below-grade hides, ground context and
occlusion:

```sh
python3 cmd/oemcards/testdata/mktestglb.py /tmp/test.glb
go run ./cmd/oemcards -glb /tmp/test.glb -out /tmp/cards -keys GT,GEN,HRSG
```
