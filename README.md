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

- 3.511 volums d’edificis oficials de l’ICGC (IFC 3D, 2024), amb coordenades i alçades de la font.
- 1.131 trams de carretera/carrer/camí, 112 àrees i 48 punts d’interès d’OpenStreetMap.
- Model d’elevacions real ICGC MET5, mostrejat a 10 m; carrers subdividits per seguir el relleu.
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

En mòbil apareixen dos bolets analògics independents: l’esquerre mou el personatge respecte de la càmera o gira/accelera el cotxe; el dret orienta la càmera. Es poden fer servir alhora. Els bolets es reinicien en deixar anar, cancel·lar el toc, pausar o redimensionar.

Amb un gamepad físic de mapping estàndard: bolet esquerre per moure/girar, dret per càmera, RT/LT per accelerar/frenar o marxa enrere, Y per pujar/baixar, A per córrer, B per fre de mà, X per canviar càmera, View per mapa, RB per iniciar ruta, LB per recuperar i Menu per pausa. A o Menu inicien el joc des de la portada. Inclou zona morta contra la deriva. No s’ha validat encara amb un comandament físic connectat.

 Toca el mapa per marcar un punt blau. El marcador verd indica l'entrega activa; atura el cotxe dins dels 10 metres per completar-la. Els punts donen orientació directa: no són un navegador amb càlcul de rutes.

## Fidelitat i límits

**Els edificis es representen amb les malles de la cartografia oficial ICGC RTT 2024, sense inferir-ne l’alçada. El relleu prové del model d’elevacions real.** La font és topogràfica a escala 1:5000: no és fotogrametria de façanes, i inclou extrusions amb coberta plana. Els materials de façana són recreats. L’ortofoto continua sent una capa de terreny, cobertes i minimapa. No es promet una còpia exacta de cada casa actual. Consulta [SURVEY-CREDITS.md](SURVEY-CREDITS.md).

El trànsit segueix segments d'OSM i pot girar a l'extrem d'un tram; no disposa d'un sistema complet de semàfors ni d'encaminament urbà. Els vianants són ambientals. La policia és una mecànica senzilla de persecució, sense navegació complexa. La cartografia pot tenir errors o desajustos entre fonts; R permet recuperar-se.

Validació: proves automàtiques de dades geogràfiques, projecció sobre carrers, col·lisions, límits, punt d'inici i destinacions; compilació de producció. Les 15 proves automàtiques passen. També s’ha construït l’escena completa de 3.511 edificis i alternat els materials sense errors. La verificació visual 3D i les proves de jugabilitat en navegador queden pendents perquè el navegador disponible no pot crear un context WebGL. Els bolets simultanis es proven amb esdeveniments de dos dits; falta validar amb maquinari físic. Els fitxers de la web i el mapa publicats s’han verificat per HTTP.

## Actualitzar el mapa

```sh
python3 scripts/import_map.py
npm test
npm run build
```

L'importador consulta l'API d'OSM per una àrea acotada, projecta les coordenades i desa una instantània comprimida. Evita executar-lo repetidament sense necessitat. El joc no inventa una quadrícula de carrers quan falla la descàrrega.

## Arquitectura

- `src/main.js`: escena, bucle, entrada, conducció, missions, càmera i interfície.
- `src/world.js`: construcció de geometria i materials, malles d’edificis ICGC, vegetació i models.
- `src/geo.js`: projeccions, elevacions reals, col·lisions amb índex espacial i moviment.
- `src/controls.js`: dos bolets tàctils i Gamepad API estàndard.
- `src/survey.js` i `src/terrain.js`: càrrega de malles oficials i interpolació d’altituds.
- `scripts/import_survey.py`: conversió reproduïble IFC + ArcGrid.
- `public/data/survey-buildings.json.gz` i `terrain.json.gz`: dades oficials preparades.
- `public/data/cabrils.json.gz`: instantània geogràfica ODbL inclosa.
- `scripts/import_map.py`: importador reproduïble, només biblioteca estàndard Python.
- `tests/geo.test.js`: comprovacions del mapa i de l'espai jugable.

Codi original MIT. Dades geogràfiques © OpenStreetMap contributors, ODbL 1.0. Consulta [DATA-LICENSE.md](DATA-LICENSE.md).

## Textures i referències de Cabrils

S’han consultat fotografies del carrer de Sant Salvador i referències patrimonials del municipi. Les fotografies només orienten la paleta; no s’han copiat al joc. Les textures fotogràfiques reutilitzables són de Poly Haven (CC0), incloses localment i optimitzades a WebP. Consulta [TEXTURE-CREDITS.md](TEXTURE-CREDITS.md) i `public/textures/manifest.json` per als materials, llicències i procedència. Les façanes de la versió topogràfica fan servir estuc neutre; les finestres i persianes de l’atles anterior no s’apliquen com si fossin dades reals de cada casa.

## Ortofoto real de Cabrils

El mode **AERI: ON**, activat per defecte, mostra una fotografia aèria real de Cabrils al terreny, les cobertes i el minimapa. El botó **AERI** alterna entre aquesta imatge i els materials anteriors. Inclou una instantània ICGC de 4096 × 4096 píxels, allotjada al mateix web. El pes addicional de la imatge és aproximadament 5,6 MB. La imatge de vista zenital no proporciona façanes fotorealistes ni el relleu real; hi pot haver desajustos entre l’ortofoto i la topografia 3D de dates diferents.

Ortofoto © ICGC, CC BY 4.0, adaptada. Consulta [AERIAL-CREDITS.md](AERIAL-CREDITS.md) i `public/aerial/manifest.json`. L’any exacte del vol a Cabrils no s’ha verificat. Les proves inclouen projecció, orientació nord/sud i UV de la imatge, a més de les de col·lisions i geometria.
