# Cabrils material references and texture sources

The material palette is informed by public photographs of Cabrils, especially Carrer de Sant Salvador, the old village centre and Santa Creu. Reference photographs are **not included or used as textures** in this repository.

Visual references:

- Barcelona Catalunya Film Commission, Carrer de Sant Salvador: https://www.bcncatfilmcommission.com/es/location/calle-sant-salvador
- Ajuntament de Cabrils, Ruta patrimonial / Ruta urbana: https://www.cabrils.cat/municipi/turisme/rutes/ruta-patrimonial--ruta-urbana.html
- Santa Creu and village overview images found during the Cabrils reference search.

## Included photographic surfaces

All original photographic surface maps are from **Poly Haven**, CC0 1.0. License: https://polyhaven.com/license and https://creativecommons.org/publicdomain/zero/1.0/ . They may be redistributed and modified. The exact source URL and original download SHA-256 for each map are recorded in `public/textures/manifest.json`.

| Surface | Original asset | Application |
|---|---|---|
| Lime / plaster | https://polyhaven.com/a/plastered_wall | White, ivory and pale ochre facades |
| Aged terracotta | https://polyhaven.com/a/clay_roof_tiles_02 | Roofs, at approximately 2.5 m per repeat |
| Warm stone | https://polyhaven.com/a/rustic_stone_wall_02 | Building plinths |
| Worn asphalt | https://polyhaven.com/a/asphalt_02 | Vehicle roads |
| Stone paving | https://polyhaven.com/a/cobblestone_floor_03 | Pedestrian paths only |
| Soil and sparse vegetation | https://polyhaven.com/a/brown_mud_leaves_01 | Terrain and unpaved tracks |
| Concrete paving | https://polyhaven.com/a/concrete_pavement | Sidewalk strips |

There are seven material sets with photographic albedo and OpenGL normal maps. Maps are downsampled to 512 × 512 WebP for web/mobile use. Colour textures use sRGB; normal maps remain linear. Surface relief uses normal maps, without expensive displacement geometry.

Three 1024 × 1024 facade atlases combine the CC0 plaster photograph with original artwork for narrow openings, lime surrounds, wooden shutters, sills and iron grilles. That additional artwork is MIT. The facades cover 7 × 6.4 m per repeat, roughly two bays and two floors. These are reusable material interpretations, not photographs or exact replicas of individual Cabrils houses. Real surface materials have **not** been surveyed building by building, and assignments are artistic approximations.

Assets are included in the repository and served from the game's own GitHub Pages origin. There is no runtime dependency on a texture website.

## Reproducing the web assets

Download the seven source albedo and OpenGL normal maps at 1K from the original asset pages. Name them `<asset>_diff.jpg` and `<asset>_normal.jpg`, using the asset IDs from `manifest.json`.

```sh
python3 -m pip install Pillow
python3 scripts/prepare_textures.py /path/to/downloaded-maps
```

This resizes and compresses the maps, builds facade atlases and writes the provenance manifest. Keep these credits and the manifest with redistributed copies, even though attribution is not mandatory for CC0 assets.
