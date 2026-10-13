# Sistema Elara: Elara, Titanus y Termos

Elara es una enana naranja con un sistema casi vacío: Titanus, un gigante de 12 masas jovianas, migró hacia dentro y se tragó o expulsó casi todo. Solo Termos (con sus lunas Tyrna y Karmen) sobrevivió, en la órbita interior. Termos se trasladó aquí desde el cinturón entre Skolta y Dres (ver [../termos/DISENO.md](../termos/DISENO.md)).

## Cuerpos y órbitas

| Cuerpo | Órbita | Radio | g | Plantilla | Notas |
|---|---|---|---|---|---|
| **Elara** | Kerbol, a = 0.3 años luz kerbales (~19 000 KAU), e = 0, i = 9° | 183 120 km | 2.50 | Sun | K4 V. SOI fijada a 2 000 KAU |
| **Termos** | Elara, a = 3 KAU, e = 0.025, i = 6.5° | 212.9 km | 0.2702 | Laythe | Año de 6.2 años de Kerbin. SOI de 75 Mm (Tyrna y Karmen caben de sobra) |
| **Titanus** | Elara, a = 6.5 KAU, e = 0.03, i = 1.5° | 7 200 km | 21 | Laythe | Año de 19.8 años de Kerbin. SOI de 15.6 Gm |

## Elara

Escalada respecto a Kerbol como una K4 V real respecto al Sol: **0.70 masas y 0.70 radios** (mu = 8.21e17).

- **Luz:** L = 0.70² · (4 600 / 5 772)⁴ = 0.20 L_Kerbol. Kopernicus mide `luminosity` en W/m² a 1 KAU (Kerbol = 1360): **268.8**. Termos recibe 30 W/m² (el 2 % que Kerbin) y Titanus, 6 W/m². En los dos el calor viene de dentro.
- **SOI a mano:** con una masa del 70 % de la de Kerbol, la fórmula de Laplace daría una SOI de 0.26 años luz, que llegaría a tocar la de Kraken. Se fija a 2 000 KAU (`sphereOfInfluence`), muy por encima de lo que necesita el sistema (Titanus está a 6.5 KAU).
- **Posición:** a 0.3 años luz kerbales, en el lado del cielo opuesto a Kraken (anomalía media 4.3 frente a 1.0). La separación mínima entre las órbitas de Kraken y Elara (8.6e13 m) supera la suma de sus SOI (4.8e13 m).
- **Aspecto:** shader de estrella de Kerbol en naranja (`emitColor0/1`, manchas pardas). Destello de Scatterer y luz de PlanetShine naranjas.

## Titanus

La petición: 1.2 radios de Jool, 12 veces la masa de Jool, 218 atm y 700 K en la superficie, océano de agua supercrítica, balsas de minerales flotantes, vida exótica plausible y una gravedad de 10 a 30 g.

### Gravedad: 21 g

Las cifras de radio y masa no dan la gravedad pedida en unidades de KSP: Jool es unas tres veces menos denso que Júpiter, y 12 masas de Jool en 1.2 radios de Jool dan solo **6.7 g**. Se interpretó Titanus como un "Júpiter de 12 masas jovianas y 1.2 radios jovianos", que es lo que describe la ficha (casi una enana marrón), y se conservó su gravedad real, igual que se hizo con Termos y las demás fichas:

g = 24.79 m/s² · 12 / 1.2² = 207 m/s² = **21 g**

En unidades de KSP eso son **~38 masas de Jool** (mu = 1.068e16) y el **1.3 % de la masa de Elara**, la misma proporción que 12 M_J junto a una K4 V real. Si se prefiere exactamente 12 masas de Jool, basta con poner `gee=6.67` en `sistema.py` y en `Titanus.cfg`.

Consecuencias de juego: velocidad orbital en la superficie de 38.5 km/s y de escape de 54 km/s. Llegar a órbita desde el mar exige más de 40 km/s de delta-v. Ningún kerbal aguanta de pie.

### Atmósfera y océano

- **Aire:** 78 % H₂, 12 % He, 10 % H₂O (M = 3.85 g/mol), γ = 1.38. 218 atm y 700 K al nivel del mar; adiabática húmeda (κ = 0.2) hasta 160 K en la cima de las nubes. Con 21 g la atmósfera se aplasta: techo a ~70 km (`generar_atmosferas.py`). Densidad al nivel del mar: 14.6 kg/m³.
- **Océano:** el punto crítico del agua es 647 K y 218 atm, así que a 700 K el "mar" es **agua supercrítica**: ni líquido ni vapor. Su densidad en la superficie ronda 0.15 g/cm³ y crece rápido con la profundidad (con 21 g, cada 100 m suman ~30 atm). En el juego, `density = 0.2`: la mayoría de las naves se hunden.
- **Fondo:** todo el manto está bajo el mar, de **−179 km** (fosas) a **−18 km** (dorsales): 20 veces más hondo que en la primera versión. El relieve se calcula en la escala original y se multiplica por `TITANUS_PROF = 20` al guardar la altura (`offset = −180 000`, `deformity = 172 000`; 2.6 m por nivel de gris en 16 bits). Los umbrales de biomas siguen en la escala original.

### Balsas minerales y vida

El agua supercrítica es un disolvente muy agresivo: se come la roca del manto, sobre todo en las crestas de las **Dorsales de Disolución**. Al subir y enfriarse, la sílice y las sales de magnesio precipitan como una **espuma llena de hidrógeno** de ~0.12 g/cm³, más ligera que el agua supercrítica, y flotan. Las corrientes juntan esa espuma en balsas del tamaño de montañas, sobre todo encima de las dorsales.

En los poros de algunas balsas (bioma **Jardines Químicos**) crecen redes de compuestos de silicio y azufre que catalizan su propia formación con el hidrógeno y los minerales disueltos: crecen, se parten y cada trozo sigue creciendo. A 700 K no puede haber química de proteínas ni de ADN; lo más plausible es algo así, química autocatalítica en superficies minerales. Los textos de ciencia no lo llaman vida: dejan la pregunta abierta.

**Scatters de Parallax con modelos propios** (`generar_modelos.py` → `Modelos/Titanus/*.mu`, 6 formaciones × 3 LOD). Los modelos `.mu` se escriben con `herramientas/mu.py`, que reproduce la estructura mínima de los modelos de Parallax_StockScatterTextures (una sola malla: vértices, UV, normales, tangentes y triángulos; Parallax pone el material). El origen de cada modelo es la línea de flotación: Parallax los coloca **a nivel del mar** (`placementAltitude = 0`) sobre cualquier fondo de −180 a −8 km, así que flotan.

| Formación | Tamaño (escala 1) | Geología |
|---|---|---|
| `continente_a`, `continente_b` | ~3.3 km, de −340 a +590 m | Meseta en terrazas de estratos (escalones de 45 m), siete mesetas testigo de paredes verticales, crestas de minerales cristalizados, acantilado con muesca de oleaje a ras de agua y agujas sueltas |
| `montana` | ~1.6 km, hasta +680 m | Pico con cárcavas radiales y estratos de 22 m, rodeado de órganos de columnas hexagonales (por contracción, como las de basalto) |
| `agujas` | ~350 m, hasta +490 m | Racimo de cristales de sílice hexagonales, inclinados y con punta piramidal, sobre una base de espuma |
| `chimeneas` | ~350 m, hasta +240 m | Tubos huecos de precipitación química con la boca acampanada (como los jardines químicos o las fumarolas negras) |
| `balsa` | ~250 m, hasta +20 m | Balsa pequeña de espuma, para rellenar entre las grandes |

Con 21 g nada alto se sostiene sin una raíz ancha: los continentes y la montaña son achaparrados y macizos; las agujas y los tubos son finos porque son cristales y paredes huecas.

| Scatter | Modelo | Biomas | Tinte |
|---|---|---|---|
| ContinentesA / B | `continente_a` / `_b` | Balsas Minerales (A también en Jardines) | ocre y óxido |
| Montanas | `montana` | Balsas Minerales, Dorsales | óxido oscuro |
| AgujasSilice | `agujas` | Balsas, Dorsales, Jardines | sílice pálida |
| ChimeneasMinerales | `chimeneas` | Dorsales, Balsas | gris pardo |
| ChimeneasVivas / Naranja | `chimeneas` | Jardines Químicos | verde y naranja (las redes químicas) |
| BalsasEspuma | `balsa` | Balsas, Jardines y algo de Mar Supercrítico | crema |
| Espuma | iceberg pequeño de Kerbin | Balsas, Dorsales | crema |

Material: el shader biplanar de los icebergs de Kerbin con una textura propia (`PluginData/Titanus/Titanus_Roca.png`: estratos ondulados, vetas de sales y costras de sulfuros; `construir.py` la pasa a DDS) y la normal de los icebergs; roca mate (`_SpecularIntensity = 0.25`). `collisionLevel = 4`: se puede aterrizar en ellas.

> **Por probar en el juego.** Parallax reparte los scatters sobre los quads del terreno. Con el fondo a 18–179 km, no está comprobado que los quads del fondo lleguen al nivel de detalle en el que Parallax los procesa. Si las formaciones no aparecen, hay dos salidas: subir el fondo bajo los biomas de balsas (por ejemplo, dorsales a −2 km) o reducir la profundidad.

### Biomas

| Bioma | Color | Valor | Dónde |
|---|---|---|---|
| Fosas del Manto | `#2a1f4f` | 1.4 | El 10 % más hondo del fondo |
| Mar Supercrítico | `#4f6fa8` | 1.0 | El resto del océano |
| Dorsales de Disolución | `#c87a3a` | 1.3 | Fondo por encima de −3 200 m, sin balsas |
| Balsas Minerales | `#d8c690` | 1.5 | Franjas de convergencia de las corrientes (16 % del planeta) |
| Jardines Químicos | `#58c878` | 2.0 | Parte de las balsas por debajo de 50° de latitud (3.7 %) |

### Anillos

Un solo anillo de Kopernicus de **1.6 a 80 radios** (11 500–576 000 km, como J1407b), con la textura `Titanus_Ring.png` de 4 096 px: denso y pardo por dentro (roca), pálido y helado por fuera, con cinco huecos en 3.1, 7.5, 13, 21 y 34 radios (resonancias con las lunas que se tragó) y anillos finos. Desde Termos ocupa unos 1.4°: más que tres lunas llenas.

### Aspecto desde el espacio

218 atm de hidrógeno con nubes de agua: no se ve el océano. Sobre el dibujo de bandas de la primera versión (que se conserva como base, con un 15 % de peso) se aplica una gradación amenazante: zonas crema enfermizas, cinturones de óxido y sangre seca y un negro amoratado, con filamentos de turbulencia entre las bandas.

- **El Ojo** (22° S, 70° E): un ciclón oscuro de ~6 000 × 2 400 km, más ancho que Kerbin, con tres brazos en espiral logarítmica, el centro casi negro y la pared encendida de azufre.
- Nueve tormentas oscuras menores y los óvalos claros de antes.
- Limbo rojo sangre que se apaga en negro (`Gradient` y `rimBlend`), anillos más oscuros y rojizos.
- **Scatterer:** cielo rojo herrumbre, muy brumoso (`mie` 0.05).

### Nubes volumétricas (EVE, V5)

Dos capas separadas por un hueco, para dar escala y profundidad: se ve la cubierta baja entre las torres.

| Capa | Altura | Cobertura | Densidad |
|---|---|---|---|
| `Titanus-nubes` | 9–24 km | `Titanus_Clouds.png`: las zonas claras de las bandas | ×3 la del resto del pack |
| `Titanus-tormentas` | 26–44 km | `Titanus_Tormentas.png`: bordes de los cinturones (cizalla), tormentas y brazos de El Ojo | ×1.5 |

La vista lejana no se cambia con EVE (`swap = False`): las bandas horneadas hacen de capa profunda bajo las volumétricas.

## Destello de Elara (Scatterer)

Texturas propias, en PNG (`PluginData/Elara/Destello/`, `construir.py` no las comprime: DXT1 rompería los degradados), generadas por `generar_visuales.destello_texturas()`:

- **Núcleo:** disco saturado blanco que vira a naranja, resplandor 1/r² y corona ciliar (las «pestañas» finas de la lente).
- **Estallido:** 6 picos de difracción (diafragma hexagonal) con bandas irisadas, 6 secundarios y 260 rayos finos de longitud y color variables.
- **Raya anamórfica:** horizontal, cálida en el centro y cian en los extremos.
- **Halo:** anillo de 22° con dispersión (rojo fuera, azul dentro) y otro más tenue.
- **14 fantasmas** a lo largo de la línea estrella–centro de pantalla: hexágonos del diafragma con borde brillante y franja cromática, anillos irisados y discos ámbar, de distintos tamaños y a ambos lados de la estrella.

Las curvas de escala e intensidad van por distancia a la estrella y son planas en un margen amplio, así que Termos y Titanus quedan dentro tanto si Scatterer mide en radios de la estrella como en Gm.

## Archivos

| Archivo | Contenido |
|---|---|
| `Configs/Elara/Elara.cfg` | La estrella |
| `Configs/Elara/Titanus.cfg` | Cuerpo, órbita, anillos, atmósfera (bloque generado), PQS y océano |
| `Configs/Elara/Ciencia.cfg` | Textos de ciencia de Elara y Titanus |
| `Configs/Termos/*` | Termos y sus lunas (ahora con `referenceBody = Elara`) |
| `herramientas/sistema.py` | Órbitas, masas, luz (`LUMINOSITY`), anillos (`TITANUS_RING`) y atmósfera |
| `herramientas/generar_texturas.py` | `titanus()`: altura, color, biomas, nubes (`Clouds`, `Tormentas`) y anillo |
| `herramientas/generar_modelos.py`, `herramientas/mu.py` | Modelos procedurales de los scatters y escritor/lector de `.mu` |
| `Modelos/Titanus/*.mu`, `PluginData/Titanus/Titanus_Roca.png` | Los 18 modelos (6 × 3 LOD) y su textura |
| `PluginData/Elara/Destello/*.png` | Texturas del destello de Elara |
