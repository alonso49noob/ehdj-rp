# Mundos Lejanos — versión de prueba (10-10-2026)

Gracias por probarlo. Es un planet pack de Kopernicus con tres sistemas, dos planetas nuevos y dos planetas enanos en el de Kerbol:
- **Creus–Halum**: un binario errante capturado a 880 KAU de Kerbol. Halum tiene continentes de hielo flotante.
- **Kraken**: una enana marrón T2 a 0.2 años luz kerbales (~12 650 KAU).
- **Norh**: un planeta nuevo del sistema de Kerbol, troyano de Jool (lo sigue 60° por detrás).
- **Skolta**: un "Titán cálido" del sistema de Kerbol, entre Duna y Dres, con su luna Ceniza.
- **Elara**: una enana naranja K4 V a 0.3 años luz kerbales, con **Titanus** (12 masas jovianas, 21 g, anillos enormes y océano de agua supercrítica) y **Termos** (planeta enano activo con lagos casi hirviendo y dos lunas, Tyrna y Karmen).
- **Talia**: un planeta enano lleno de cráteres en el cinturón exterior, entre Dres y Jool.
- **Akira**: un mundo de hielo con atmósfera densa a 200 KAU de Kerbol.

Las texturas son **provisionales**: las pintará un artista más adelante.

## Instalación

1. Copia la carpeta `GameData/MundosLejanos` dentro de `Kerbal Space Program/GameData/`.
2. Imprescindibles: **Kopernicus** (probado con 1.12.1-247) y **ModuleManager**. KSP 1.12.x.
   - Recomendado: **CTTP** (Community Terrain Texture Pack), con el suelo de mejor calidad. Debe quedar en `GameData/CTTP/Textures/PluginData/` (por ejemplo, `rock.dds`).
   - Sin CTTP, el pack usa sus propias texturas de suelo, más simples. Si Kopernicus muestra "Missing Textures" con rutas `CTTP/...`, CTTP está a medias o en otra carpeta: bórralo o reinstálalo.
3. Opcionales, que el pack aprovecha si están instalados:

| Mod | Qué aporta |
|---|---|
| Parallax Continued + Parallax_StockScatterTextures | Rocas, cristales y las máquinas |
| Scatterer + StockScattererConfigs | Atmósferas y océanos |
| EVE (Blackrack) + StockVolumetricClouds | Nubes volumétricas |
| PlanetShine | Luz reflejada por los planetas |

Usa una **partida nueva**: el pack añade 34 cuerpos. La primera carga es lenta porque Kopernicus crea su caché. Se probó **sin OPM**.

## Ir rápido a cualquier sitio
Menú de depuración: `Alt+F12` → Cheats → **Set Orbit**. Pon una nave en órbita del cuerpo que quieras probar.

## Qué probar

- [ ] **Kraken** parece una enana T: bandas granate y pardo rojizo, sin corona y con luz tenue y rojiza (sin tonos violeta).
- [ ] Los **tres discos** de Kraken se ven desde el Tracking Station; el del Cinturón Oscuro casi no se ve.
- [ ] Los **polos** de Creus, Halum, Scarch, Tenebris y Vestigia ya no tienen cuñas de luz ni de sombra.
- [ ] **En vuelo**, los planetas del sistema Kraken quedan iluminados por Kraken (luz rojiza) y no por Kerbol (luz blanca).
- [ ] **Krax**: la Fundición (20° N, 60° O) tiene agujas metálicas de las máquinas (requiere Parallax).
- [ ] **Halum**: los continentes de hielo blanco azulado alrededor de las islas se ven desde órbita, se puede aterrizar en ellos y el frente de hielo está rodeado de témpanos flotando (requiere Parallax).
- [ ] **Elara** da luz naranja a Termos y Titanus (no la blanca de Kerbol); los anillos de Titanus se ven desde el Tracking Station.
- [ ] **Titanus**: las balsas minerales flotan sobre el mar (no hundidas ni en el aire) en los biomas Balsas Minerales y Jardines Químicos (requiere Parallax).
- [ ] **Scarch**: los Campos de Extracción tienen máquinas. Haz un experimento allí: los registros están **en inglés**.
- [ ] **Tenebris**: frío y oscuro, 0.2 atm de metano y 0.29 g. Océanos helados y agua líquida solo en el ecuador, con respiraderos de metano en la costa. La órbita baja empieza por encima de 527 km. En 18° S 140° E están los restos de una máquina.
- [ ] **Cuerpos menores con personalidad**:
  - Secunda: acantilado de 3.6 km, ¿cuánto dura la caída?
  - Prima: dos lóbulos unidos por un cuello.
  - Pastora: forma de nuez.
  - Atra: forma de puro.
  - Fuligo: el Ojo brillante.
  - Lumen: franjas de tigre en el polo sur.
  - Hollín: la baliza de las máquinas, con registro en inglés.
- [ ] **Salus**: arcos de islas. Sus lunas son Vestigia y Nox (casi negra).
- [ ] **Cinturón Oscuro** (Fuligo, Caligo, Atra y asteroides): casi invisibles.
- [ ] **Halum**: amerizar en el océano de neón (7 atm). Volver a órbita es difícil, a propósito.
- [ ] **Cometa Heraldo**: tiene coma verdosa, cola de iones azul (siempre opuesta a Kerbol) y cola de polvo curvada. Se ve desde el mapa (Tracking Station o vista de mapa) y crece al acercarse a Kerbol. Lo dibuja el plugin `MundosLejanos.dll`.
- [ ] **Terreno a ras de suelo** (con Parallax): texturas de suelo detalladas, colinas y cambios de color en todos los cuerpos rocosos; en Skolta, rocas, bloques, agujas volcánicas, cristales de sal y vetas de cobre según el bioma.
- [ ] **Cuerpos menores** (Ceniza, Vestigia, Nox, Lumen, cinturón oscuro, asteroides): cráteres de todos los tamaños, con bordes claros y rayos en los más jóvenes.
- [ ] **Norh** (troyano de Jool, 60° por detrás):
  - comprueba con el tiempo acelerado que sigue a Jool sin acercarse ni alejarse;
  - los anillos de hielo se ven inclinados y no giran con el planeta;
  - el cielo es ocre y el mar ecuatorial es líquido;
  - aterrizar con paracaídas es fácil; despegar de nuevo es muy difícil (12 bar);
  - el Gran Volcán (8° N, 50° O) mide 9 km: ¿se puede escalar?
- [ ] **Skolta** (entre Duna y Dres, órbita inclinada 19°):
  - desde el espacio es una bola naranja, como Titán;
  - el mar de amoníaco es incoloro: crema en la orilla y casi negro mar adentro. Desde el espacio se ve oscuro frente a la tierra clara y brilla con el reflejo de Kerbol. Las naves flotan peor que en agua;
  - busca las bahías azules junto a los volcanes y los yacimientos de cobre (azul y violeta);
  - en Ceniza, el Monte Solitario (12° N, 75° E).
- [ ] **Termos** (entre Skolta y Dres; 0.27 g y 5 atm):
  - desde el espacio, nublado y gris azulado, con lagos turquesa que brillan al reflejar a Kerbol;
  - amerizar en un lago a 140 °C: ¿flotan bien las naves? (el agua caliente es algo menos densa);
  - los pozos ácidos de colores en los trópicos y las terrazas blancas de las orillas;
  - despegar con 5 atm pero solo 0.27 g: ¿cuánto Δv hace falta?
- [ ] **Tyrna** (fisuras con metales) y **Karmen** (cara de fractura plana y brillante), las lunas de Termos.
- [ ] **Talia** (entre Dres y Jool): cráteres por todas partes, la Gran Cuenca (22° S, 110° E) y los afloramientos metálicos.
- [ ] **Akira** (200 KAU; usa Set Orbit): cielo azul oscuro, hielo rosado, el Glaciar de Celdas (25° N, 160° E) y los criovolcanes. ¿Se ve algo con tan poca luz?
- [ ] **Aspecto de plástico** (arreglado en esta versión): compara cualquier planeta del pack con Duna y Kerbin en el mapa. Ya no debería haber un reflejo blanco enorme en tierra ni bordes en relieve como de plástico; solo brillan los mares.
- [ ] Con Scatterer y EVE: las nubes no se duplican (Halum, Salus y Termos cambian a texturas sin nubes).

## Problemas conocidos
- **Tracking Station**: a veces ilumina el sistema Kraken con la luz de Kerbol. Es el selector de estrella de Kopernicus, que elige la estrella más cercana a la cámara. En vuelo debería ir bien; confírmalo, por favor.
- La plataforma de lanzamiento de la colonia de Tenebris aún no está colocada.
- Las máquinas usan modelos provisionales de Parallax: las agujas metálicas de Moho.

## Cómo informar
Envía:
- `Kerbal Space Program/KSP.log`;
- la carpeta `Kerbal Space Program/Logs/Kopernicus/`;
- capturas de lo que veas raro, con el nombre del cuerpo.
