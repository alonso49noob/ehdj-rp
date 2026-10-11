# Termos, Tyrna, Karmen y Talia: implementación en KSP

Se basan en las fichas del equipo (Discord, 28-07): **Termos**, **Talia** y **Tyrna**. Karmen sale de la ficha de Tyrna.
Aquí se recogen los valores que se usaron en el juego y las decisiones que las fichas dejaban abiertas.

![Termos](preview_termos.png)

## Escala: ÷10, conservando la gravedad

Las fichas dan tamaños reales: Termos mide 4 258 km, más que Kerbin (1 200 km) y tres veces Skolta. En KSP los tamaños se dividen entre 10, como Kerbin respecto a la Tierra, y se **conserva la gravedad de la ficha**, que es lo que se nota al jugar:

| | Ficha | En el pack | Parecido a |
|---|---|---|---|
| Termos | 4 258 km, 2.45 masas lunares, 2.65 m/s² | R = 212.9 km, 0.2702 g (2.65 m/s²) | Algo mayor que el Mun |
| Talia | 2 928 km, 0.89 masas lunares, 1.31 m/s² | R = 146.4 km, 0.1336 g (1.31 m/s²) | Dres |
| Tyrna | 1 172 km, 0.02 masas lunares, 0.66 m/s² | R = 58.6 km, 0.0673 g (0.66 m/s²) | Minmus |
| Karmen | "del tamaño de un asteroide" | R = 4 km, 0.003 g | Un asteroide grande |

Para usar otra escala, se cambia en `sistema.py` (radio) y en `sistema.ATMOS["Termos"]["scale"]`.

> **Las fichas de Talia y Tyrna no cuadran del todo.** Con 0.89 masas lunares y 2 928 km, Talia tendría 2.0 m/s², no 1.31. Con 0.02 masas lunares y 1 172 km, Tyrna tendría 0.29 m/s² (densidad de hielo, 1.7 g/cm³), no 0.66. Se tomó la gravedad de la ficha. La de Termos sí cuadra.

## Órbitas

| Cuerpo | Órbita | Por qué |
|---|---|---|
| Termos | a = 33.5 Gm (2.46 KAU), e = 0.025, i = 6.5° | En el hueco entre Skolta (apoapsis 32.5 Gm) y Dres (periapsis 34.9 Gm). Su año dura 3.9 años de Kerbin |
| Talia | a = 53 Gm (3.9 KAU), e = 0.07, i = 9° | Cinturón exterior, más allá de Dres (apoapsis 46.8 Gm) y lejos de Jool |
| Tyrna | a = 3 400 km de Termos, e = 0.015, i = 1.2° | Algo excéntrica: las mareas la calientan, de ahí el criovulcanismo. Periodo de 31.6 h, síncrona |
| Karmen | a = 21 000 km de Termos, e = 0.18, i = 27° | "Mucho más allá de Tyrna", en una órbita de luna capturada. La SOI de Termos mide 53.6 Mm |

En las fichas, Termos y Talia comparten el cinturón "entre Klann y Tempel" (Termos tiene el 60 % de la masa, Talia el 35 % y los asteroides y el polvo, el 5 %). En el pack, Termos está en el cinturón entre Skolta y Dres y Talia en el cinturón exterior, como se pidió. Los textos dicen que Termos reúne el 60 % de la masa de su cinturón y que Talia es el mayor cuerpo del exterior.

## Termos

| | Ficha | En el pack |
|---|---|---|
| Atmósfera | 5 atm, sobre todo N₂, CO₂, vapor de agua y NH₃ | **55 % N₂, 22 % CO₂, 18 % H₂O, 5 % NH₃** (M = 29.2 g/mol). Sin oxígeno: `oxygen = false` |
| Temperatura | Lagos cerca del punto de ebullición | **122 °C en el ecuador y ~95 °C en los polos**. A 5 atm el agua hierve a 152 °C; los lagos tropicales rondan los 140 °C |
| Altura de la atmósfera | — | Se integra el Termos real (radio × 10, misma g) y las alturas se dividen entre 10, como el radio: **techo a 51 km**. Sin comprimir serían ~510 km, más que el propio radio |
| Densidad del aire | — | 4.5 kg/m³ en la superficie |
| Lagos | Inmensos lagos de agua | 22 % de la superficie, en cuencas separadas. `Ocean { density = 0.93 }` (agua a 140 °C) |
| Volcanes | Actividad volcánica en los trópicos | 36 volcanes en escudo entre ±26°; un tercio tiene lava en la caldera |
| Pozos ácidos | En los trópicos | 8 depresiones salinas de colores, como Dallol (Etiopía): sal, azufre, verde ácido y óxido |
| Rotación | — | 18 h |

### Mapa y biomas

| Bioma | Color del mapa | × ciencia | Dónde |
|---|---|---|---|
| Lagos Termales | `#2060b0` | 1.0 | Bajo el nivel del agua (22 %) |
| Orillas de Sílice | `#f0f0d0` | 1.3 | Primeros 220 m sobre el agua: terrazas blancas de sínter con bandas ocres de hierro |
| Llanuras Basálticas | `#606060` | 1.0 | El resto de la tierra baja |
| Tierras Altas | `#b08050` | 1.1 | Interior de los macizos: toba volcánica alterada |
| Montañas | `#a0a0a0` | 1.3 | Por encima de 3 000 m |
| Campos Volcánicos | `#ff6000` | 1.4 | Conos, coladas y calderas tropicales |
| Pozos Ácidos | `#c0ff00` | 1.7 | Las 8 depresiones de colores |
| Llanuras de Arcilla | `#608060` | 1.1 | Más allá de ~50° de latitud: arcillas verdosas que deja la lluvia |

Sin oxígeno libre no hay óxido rojo: el hierro forma minerales grises y verdosos.

**Vista desde el espacio.** El terreno se ve bajo un velo azulado de 5 atm (26 %), con nubes de vapor en un ~35 % del cielo: más en el ecuador, por los volcanes, y en los polos, más frescos y lluviosos. Los lagos son de un turquesa lechoso (`#4f9aa6`) y brillan cuando reflejan a Kerbol.

## Tyrna

Luna helada con criovulcanismo y la superficie cubierta de metales (ficha). En el pack, la causa es la siguiente:
- su órbita algo excéntrica deja que las mareas de Termos la calienten;
- por **6 fisuras** sube salmuera del interior que, al congelarse, deja vetas de sulfuros de hierro, níquel y cobre;
- los impactos del cinturón sembraron granos metálicos por todo el hielo.

Bioma especial: **Fisuras Criovolcánicas** (× 1.6).

## Karmen

La ficha la llama "otra luna de **Tempel**", pero sitúa su órbita "mucho más allá de Tyrna", que es luna de Termos. Se interpretó como una errata: Karmen es la segunda luna de Termos. Para darle un rasgo, es un **fragmento del núcleo metálico** de un cuerpo que se rompió (un asteroide tipo M, como Psyche) con una **Cara de Fractura** plana y pulida hacia 0° 90° E. Brilla más que el resto de las lunas (`specColor` 0.24).

## Talia

| | Ficha | En el pack |
|---|---|---|
| Atmósfera | Casi inexistente | Sin atmósfera |
| Superficie | Accidentada, llena de cráteres, sin actividad geológica: registro de la historia temprana | Superficie saturada de cráteres (más de 300), 4 cuencas de impacto y la **Gran Cuenca**: un anillo triple de 220 km en 22° S, 110° E |
| Metales | Objetivo de la minería | 12 afloramientos de hierro y níquel en los bordes de las cuencas, donde los impactos dejaron el manto a la vista (× 1.7) |
| Rotación | — | 7.3 h |

Biomas: Llanuras Craterizadas (1.0), Tierras Altas (1.1), Cuencas de Impacto (1.2), Gran Cuenca (1.5), Cráteres Jóvenes (1.3) y Afloramientos Metálicos (1.7).

## Decisiones abiertas: qué se eligió

| Decisión | Elegido | Dónde se cambia |
|---|---|---|
| Escala | ÷10 con la gravedad de la ficha | `sistema.py` |
| Posición de Talia | Cinturón exterior, entre Dres y Jool | `sistema.py`, `Talia.cfg` |
| Karmen | Segunda luna de Termos (la ficha decía Tempel) | `sistema.py` |
| Composición del aire de Termos | 55/22/18/5 % (en el orden de la ficha) | `sistema.ATMOS["Termos"]` y luego `generar_atmosferas.py` |
| Temperatura de Termos | 122 °C en el ecuador, lagos a ~140 °C | ídem |
| Disco de polvo del cinturón | **No se dibujó**: sería un anillo en el Sol stock. Se puede añadir como los discos de Kraken | — |

## Visuales opcionales

- **Scatterer:** cielo azul pálido, casi blanco por el vapor. Los lagos son de agua lechosa y turquesa (poca transparencia, n = 1.33) con espuma mineral en las orillas. Tyrna proyecta eclipses.
- **EVE:** nubes de vapor entre 2.5 y 7 km (`Termos_Clouds`). Con EVE, la vista lejana pasa a la textura sin nubes.
- **PlanetShine:** albedos de Termos 0.50, Tyrna 0.60, Karmen 0.15 y Talia 0.12.
- **Parallax:** en Termos, losas de basalto, costras de sílice y de azufre, y toba; en Talia, regolito, bloques de eyecta y metal nativo; en Tyrna, cristales de hielo y vetas metálicas.

## Archivos

| Archivo | Qué es |
|---|---|
| `Configs/Termos/Termos.cfg` | Cuerpo, órbita, atmósfera (bloque generado), PQS y lagos |
| `Configs/Termos/Lunas.cfg` | Tyrna y Karmen (generado por `generar_cuerpos_menores.py`) |
| `Configs/Termos/Ciencia.cfg` | Textos de ciencia de Termos, Tyrna y Karmen |
| `Configs/Talia/Talia.cfg`, `Configs/Talia/Ciencia.cfg` | Talia y sus textos |
| `PluginData/Termos/Termos_{Color,Surface,Height,Normal,Biomes,Clouds}.png` | Mapas provisionales |
| `PluginData/{Tyrna,Karmen,Talia}/…` | Mapas provisionales |

Vistas previas: `preview_termos.png`, `preview_tyrna.png`, `preview_karmen.png` y `preview_talia.png`. Las láminas para el artista están en `docs/referencias_artista/`.

## Pendiente

- **Probarlo en el juego**, sobre todo:
  - que las naves floten en los lagos (densidad 0.93);
  - el despegue con 5 atm y 0.27 g;
  - que Termos se vea nublado y los lagos turquesa.
