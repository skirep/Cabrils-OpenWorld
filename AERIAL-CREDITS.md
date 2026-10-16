# ICGC aerial imagery

## Source and attribution

**Ortofoto © Institut Cartogràfic i Geològic de Catalunya (ICGC), CC BY 4.0. Adapted for this game.**

- Product: [Ortofoto Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Imatge/Ortofoto-Territorial).
- Service documentation: [WMS Ortofoto Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Geoinformacio-en-linia-Geoserveis/WMS-Ortoimatges/WMS-Ortofoto-Territorial).
- License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/).
- Provider: Institut Cartogràfic i Geològic de Catalunya, https://www.icgc.cat .
- Visible attribution and license links are retained in the game footer, including mobile layouts.

The included image is an aerial orthophoto, not a Google Maps screenshot and not a satellite photograph. It comes from a bounded export of `ortofoto_color_vigent`, the latest definitive RGB orthophoto layer exposed by the service at download time. The exact flight date for Cabrils has **not** been verified; do not infer it from the retrieval timestamp.

## Included snapshot and modifications

`public/aerial/cabrils-ortho.webp` is a 4096 × 4096 image covering longitude 2.349–2.391 and latitude 41.515–41.543. This covers Cabrils and part of the surrounding area, not the exact municipal boundary. At Cabrils latitude its in-game sampling is approximately 0.86 m/pixel east-west and 0.76 m/pixel north-south. This is the exported image sampling, not a claim about the native orthophoto resolution.

`public/aerial/manifest.json` records the complete WMS request, bounding box, coordinate reference system, retrieval timestamp, license, SHA-256 and modifications. The WMS export was converted from JPEG to WebP. It is mapped to the game's approximate terrain surface and roof footprints using the same local longitude/latitude projection as the OpenStreetMap data. Images are served locally from GitHub Pages, with no third-party tile requests during gameplay.

The default AERI mode applies the photograph to the terrain, roof surfaces within the image bounds and minimap. Roads and buildings remain 3D geometry. Material mode restores the earlier surfaces. The photograph already contains roof, vegetation and lighting detail; it is not a true orthophoto-derived 3D model. Baked shadows, differing capture dates, building parallax, approximate terrain and differences between OSM outlines and the orthophoto can cause mismatches. Facades are still approximations, since an overhead photograph cannot reconstruct street-level facades.

## Reproduce

```sh
python3 -m pip install Pillow
python3 scripts/import_aerial.py
npm test
npm run build
```

The importer makes one bounded WMS request and records provenance. Do not run it repeatedly without a need to refresh the imagery. Refreshing the `vigent` layer may return a newer image. This use does not imply ICGC endorsement.
