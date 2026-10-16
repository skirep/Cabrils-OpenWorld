# Geographic data

`public/data/cabrils.json.gz` contains a derived OpenStreetMap database, freely available under the Open Database License (ODbL) 1.0:

- © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright)
- [ODbL 1.0 text](https://opendatacommons.org/licenses/odbl/1-0/)
- Source: https://www.openstreetmap.org/api/0.6/map?bbox=2.349,41.515,2.391,41.543
- Downloaded: 16 October 2026 (exact timestamp embedded in the snapshot).
- Changes: projected longitude/latitude to local approximate metres; retained roads, building outlines, selected landcover and named POIs; inferred missing building heights; compressed with gzip. No aerial imagery or proprietary map tiles included.

Reproduce the data with `python3 scripts/import_map.py`. To read the database: `gzip -dc public/data/cabrils.json.gz > cabrils.json`.

The snapshot is a rectangular area around Cabrils, approximately 3.5 × 3.1 km, including some neighbouring streets. It does not claim to reproduce the entire municipal boundary. Gameplay bounds are smaller than the downloaded rectangle. OpenStreetMap features may be incomplete or out of date.

A bounded ICGC Ortofoto Territorial snapshot is now included separately in `public/aerial/` under CC BY 4.0. It is independent of the ODbL OSM geometry database. See [AERIAL-CREDITS.md](AERIAL-CREDITS.md) for its license, attribution, export resolution, modifications and provenance.
