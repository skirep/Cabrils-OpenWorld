# Surveyed buildings and terrain

**Edificis i elevacions © Institut Cartogràfic i Geològic de Catalunya (ICGC), CC BY 4.0. Adapted for this game.**

- Buildings: [Referencial Topogràfic Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Referencial-Topografic-Territorial), 2024, IFC 3D, working scale 1:5000.
- Six source sheets: 293118, 293119, 293120, 294118, 294119, 294120. Original URLs and SHA-256 hashes are recorded in `public/data/survey-manifest.json`.
- Terrain: [ICGC terrain elevation WCS](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Geoinformacio-en-linia-Geoserveis/WMS-i-WCS-Elevacions/WCS-del-Model-dElevacions-del-Terreny), MET5, bounded ArcGrid export at 10 m sampling. The exact request is recorded in the manifest. The source service supports the legacy name `met`, which resolves to MET5.
- License: [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/). No ICGC endorsement implied.

## What changed

The game loads **3,511 source building volumes** within the rectangular game region. The runtime replaces the earlier 2,716 OSM footprints and inferred heights. OSM roads, POIs and landcover remain a separate ODbL database. These are render overlays, not a merged geographic database.

IFC solids are triangulated, transformed from ETRS89 UTM 31N into the same local geographic projection as roads/orthophoto, quantized to centimetre storage precision and compressed. Quantization is a storage choice, **not a claim of centimetre survey accuracy**. Mesh vertices retain the source positions and elevations; the renderer does not invent extra storeys or pitched roofs. Courtyards and disjoint parts are retained in collision footprints. The renderer omits underground bottom faces. Roofs may receive the orthophoto with geographic UVs; facades use an illustrative plaster material. Meshes are batched by 180 m cells for culling.

Source IFCs include surveyed volumes with flat extrusions. They are **not** a photogrammetric street-level model. Roof slopes, windows, shutters, materials, trees, garden walls and other small details are not guaranteed to match reality. A 2024 snapshot cannot guarantee current buildings. Four IFC objects could not be triangulated, including a zero-height tank; their IDs are recorded rather than replaced with invented geometry.

The real elevation grid replaces the earlier synthetic sloping/sinusoidal terrain. Its vertical datum is aligned with the IFC source by subtracting a shared 165.99 m origin altitude. All vehicles, pedestrians, roads, collision cameras and terrain sample that grid. Roads are subdivided to conform to the measured hills. The DEM and IFC were captured/derived separately; local ground mismatches remain possible.

## Reproduce

Install `numpy pyproj shapely ifcopenshell`, download and extract the six IFC sheet ZIPs from the manifest (exclude the optional `noms-geografics` files), and save the manifest's terrain WCS response to an ArcGrid text file. The ICGC download application's documented proxy can deliver files when direct datacloud access is unavailable:

`https://proxy.icgc.cat/proxy/proxy_icgc.cgi?url=<original-source-URL>`

```sh
python scripts/import_survey.py --cache /path/to/ifc-files --dem /path/to/terrain.asc
npm test
npm run build
```

Source downloads are bounded exports. The game serves the prepared snapshots from its own GitHub Pages origin, with no ICGC calls during gameplay. The local RTL index available at preparation time did not list Cabrils; this implementation therefore uses the RTT source actually downloaded, not a claimed 1:1000 or Mobile Mapping reconstruction.
