# Cabrils · Open World

Un minijoc de món obert amb **Three.js**, ambientat a Cabrils (Maresme, Barcelona). Explora a peu, condueix un cotxe i completa una ruta de sis repartiments. Inspiració en la llibertat d'exploració de GTA, amb codi i gràfics originals.

## Jugar al navegador

**https://skirep.github.io/Cabrils-OpenWorld/**

El joc es publica amb GitHub Actions després de cada canvi a `main`, sempre que les proves i la compilació passin.

## Jugar en local

Requisits: Node.js 22+ i un navegador modern amb WebGL 2 i DecompressionStream (Chrome, Edge, Firefox o Safari actuals).

```sh
npm ci
npm start
```

Obre l'adreça que imprimeix Vite (normalment http://localhost:5173). El primer inici construeix el món; pot trigar uns segons, sobretot en mòbils. Les dades del mapa estan incloses: no es consulta OSM durant la partida. La tipografia de Google Fonts és opcional i té alternatives locals.

```sh
npm test
npm run build
```

`dist/` és un web estàtic amb rutes relatives, preparat per a qualsevol hosting estàtic. El workflow `Verify game` executa proves, compila i desa un artefacte web a GitHub Actions. El workflow `Publish GitHub Pages` compila i publica el joc a GitHub Pages. El repositori és públic.

## Què inclou

- 1.131 trams de carretera/carrer/camí, 2.716 contorns d'edificis, 112 àrees i 48 punts d'interès d'un mapa real d'OpenStreetMap.
- Un sector aproximat de 3,5 × 3,1 km al voltant de Cabrils, amb límits jugables i part de l'entorn veí.
- Conducció amb acceleració, marxa enrere, frenada i col·lisions amb edificis.
- Personatge en tercera persona; pujar al cotxe blau i baixar-ne amb espai lliure.
- Trànsit ambiental, vianants i un cotxe policial que intenta acostar-se quan acumules incidències per velocitat o col·lisions.
- Minimap amb noms de carrer, mapa ampliat i punts de destinació seleccionables.
- Sis entregues: Biblioteca de Cabrils, Mas de Baix, Axol, Xeflis, zona Sorli i Font de la Plaça. Les destinacions se situen al carrer més proper.
- Contrarellotge, bonificació per entrega i rècord local al navegador.
- Llum càlida, ombres suaus, atmosfera i textures fotogràfiques CC0: estuc blanc/crema, teula envellida, pedra, asfalt, paviment de formigó i terra. Materials amb mapes de normals, persianes i reixes inspirats en referències de Cabrils.
- Controls tàctils, pausa, recuperació del vehicle, tres càmeres, qualitat gràfica i so de motor opcional.

## Controls

| Acció | Tecla |
|---|---|
| Accelerar / caminar | W o ↑ |
| Marxa enrere / caminar enrere | S o ↓ |
| Girar | A/D o ←/→ |
| Entrar / sortir del cotxe blau | E (a menys de 5 m; atura't per baixar) |
| Fre de mà / córrer | Espai |
| Ampliar el mapa | M |
| Canviar càmera | C |
| Recuperar al punt inicial | R |
| Pausa | Esc |

En mòbil apareixen botons tàctils grans. Toca el mapa per marcar un punt blau. El marcador verd indica l'entrega activa; atura el cotxe dins dels 10 metres per completar-la. Els punts donen orientació directa: no són un navegador amb càlcul de rutes.

## Fidelitat i límits

**Els carrers i les petjades d'edificis són reals. Les façanes, les cobertes i la vegetació són recreacions procedimentals. El relleu és una superfície aproximada, no un model d'elevació topogràfic.** Les alçades sense dades s'infereixen. El joc no és una reconstrucció fotogramètrica ni té la qualitat d'una producció GTA comercial.

El trànsit segueix segments d'OSM i pot girar a l'extrem d'un tram; no disposa d'un sistema complet de semàfors ni d'encaminament urbà. Els vianants són ambientals. La policia és una mecànica senzilla de persecució, sense navegació complexa. La geometria OSM pot tenir errors o solapaments; R permet recuperar-se.

Validació: proves automàtiques de dades geogràfiques, projecció sobre carrers, col·lisions, límits, punt d'inici i destinacions; compilació de producció. La verificació visual del món 3D i les proves de jugabilitat en navegador queden pendents perquè el navegador de proves no pot crear un context WebGL. Els fitxers de la web i el mapa publicats s’han verificat per HTTP.

## Actualitzar el mapa

```sh
python3 scripts/import_map.py
npm test
npm run build
```

L'importador consulta l'API d'OSM per una àrea acotada, projecta les coordenades i desa una instantània comprimida. Evita executar-lo repetidament sense necessitat. El joc no inventa una quadrícula de carrers quan falla la descàrrega.

## Arquitectura

- `src/main.js`: escena, bucle, entrada, conducció, missions, càmera i interfície.
- `src/world.js`: construcció de geometria i materials, edificis OSM, vegetació i models.
- `src/geo.js`: projeccions, superfície aproximada, col·lisions amb índex espacial i moviment.
- `public/data/cabrils.json.gz`: instantània geogràfica ODbL inclosa.
- `scripts/import_map.py`: importador reproduïble, només biblioteca estàndard Python.
- `tests/geo.test.js`: comprovacions del mapa i de l'espai jugable.

Codi original MIT. Dades geogràfiques © OpenStreetMap contributors, ODbL 1.0. Consulta [DATA-LICENSE.md](DATA-LICENSE.md).

## Textures i referències de Cabrils

S’han consultat fotografies del carrer de Sant Salvador i referències patrimonials del municipi. Les fotografies només orienten la paleta; no s’han copiat al joc. Les textures fotogràfiques reutilitzables són de Poly Haven (CC0), incloses localment i optimitzades a WebP. Consulta [TEXTURE-CREDITS.md](TEXTURE-CREDITS.md) i `public/textures/manifest.json` per als materials, llicències i procedència. La selecció de material per casa és aproximada.
