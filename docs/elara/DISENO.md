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
- **Fondo:** todo el manto está bajo el mar, de −8 950 m (fosas) a −900 m (dorsales). Detalle_PQS añade colinas de hasta 400 m, así que el techo se dejó en −900 m para que nada asome.

### Balsas minerales y vida

El agua supercrítica es un disolvente muy agresivo: se come la roca del manto, sobre todo en las crestas de las **Dorsales de Disolución**. Al subir y enfriarse, la sílice y las sales de magnesio precipitan como una **espuma llena de hidrógeno** de ~0.12 g/cm³, más ligera que el agua supercrítica, y flotan. Las corrientes juntan esa espuma en balsas del tamaño de montañas, sobre todo encima de las dorsales.

En los poros de algunas balsas (bioma **Jardines Químicos**) crecen redes de compuestos de silicio y azufre que catalizan su propia formación con el hidrógeno y los minerales disueltos: crecen, se parten y cada trozo sigue creciendo. A 700 K no puede haber química de proteínas ni de ADN; lo más plausible es algo así, química autocatalítica en superficies minerales. Los textos de ciencia no lo llaman vida: dejan la pregunta abierta.

**Scatters de Parallax** (`generar_scatters.py`): los icebergs del mar frío de Kerbin (`GiantBerg`, `Icebergs`, `SmallIcebergs`, `TinyIcebergs`) con el hielo teñido de pardo y ocre. Parallax los coloca **a nivel del mar** (`placementAltitude`) sobre cualquier fondo de altitud negativa, así que flotan aunque el fondo esté a 9 km. En los Jardines Químicos se añaden versiones verdes y naranjas. Con `collisionLevel = 4` se puede aterrizar en ellas.

> No se hizo un modelo propio: los scatters de Parallax son modelos `.mu`, y para crearlos hace falta Blender con el complemento io_object_mu o Unity con PartTools, que no están instalados.

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

218 atm de hidrógeno con nubes de agua: no se ve el océano. La textura lejana son bandas crema y pardas con óvalos de tormenta claros, como un Júpiter más cálido. Scatterer: cielo pardo anaranjado y muy brumoso.

## Archivos

| Archivo | Contenido |
|---|---|
| `Configs/Elara/Elara.cfg` | La estrella |
| `Configs/Elara/Titanus.cfg` | Cuerpo, órbita, anillos, atmósfera (bloque generado), PQS y océano |
| `Configs/Elara/Ciencia.cfg` | Textos de ciencia de Elara y Titanus |
| `Configs/Termos/*` | Termos y sus lunas (ahora con `referenceBody = Elara`) |
| `herramientas/sistema.py` | Órbitas, masas, luz (`LUMINOSITY`), anillos (`TITANUS_RING`) y atmósfera |
| `herramientas/generar_texturas.py` | `titanus()`: altura, color, biomas, nubes y anillo |
