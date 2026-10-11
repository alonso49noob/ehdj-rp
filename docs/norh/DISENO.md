# Norh: diseño

Un planeta rocoso helado del sistema de Kerbol, **troyano de Jool**: comparte su órbita y lo sigue 60° por detrás (punto L5). Tiene atmósfera de alta presión, una banda de agua líquida en el ecuador, polos helados, muchos volcanes y anillos de hielo.

![Norh](preview_norh_anillos.png)

## Datos

| | Valor | Origen |
|---|---|---|
| Diámetro | 1 207 km (R = 603.5 km) | Concepto |
| Masa | 0.94 masas de Kerbin (μ = 3.32e12 m³/s²) | Concepto (ver la nota sobre la masa) |
| Gravedad | 0.93 g | μ / R² |
| Órbita | La de Jool (68.8 Gm, 5.06 KAU), con e = 0.065 e i = 2.3° (Jool: 0.05 y 1.304°) | Troyano L5: anomalía media 60° menor que la de Jool |
| Separación de Jool | Oscila entre 54° y 67° (unos 60–76 Gm) por la diferencia de excentricidad, como la libración de un troyano real | Muy lejos de la SOI de Jool (2.5 Gm) |
| Año | El de Jool: 11.4 años de Kerbin | Mismo semieje = mismo periodo: lo sigue siempre |
| Día | 8 h | |
| SOI | 415 000 km | |
| Atmósfera | 12 bar: 45 % N₂, 23 % H₂, 32 % NH₃ | Concepto |
| Masa molar | 18.5 g/mol | 0.45·28.01 + 0.23·2.016 + 0.32·17.03 |
| Temperatura | −40 °C en el ecuador, ~−75 °C en los polos | Concepto; curva de latitud en el .cfg |
| Techo de la atmósfera | 138 km | `generar_atmosferas.py` |
| Densidad del aire en superficie | 11.5 kg/m³ (Eve: 6.2) | |
| Anillos | 1.45–2.05 R (875–1 237 km del centro), inclinados 20° | Medidos en el dibujo del concepto |

**Sobre la masa.** El concepto dice "0.94 % la masa de Kerbin". Tomé **0.94 veces** la masa de Kerbin. Con un 0.94 % la gravedad sería de 0.009 g, como un asteroide. Así no se podría retener una atmósfera de 12 bar, y Kopernicus no podría generarla: la atmósfera saldría más grande que la SOI.

## Por qué funciona

- **Órbita troyana.** En KSP no hay puntos de Lagrange (cada cuerpo solo siente a uno), pero da igual: con el mismo semieje que Jool, Norh tiene su mismo periodo y mantiene los 60° de distancia para siempre. La excentricidad y la inclinación algo distintas separan las dos órbitas en el mapa y hacen que la distancia oscile un poco, como la libración de un troyano real.
- **Calor.** En la órbita de Jool (5.06 KAU), Kerbol da 1/26 de la luz que recibe Kerbin, así que la temperatura de equilibrio rondaría −160 °C. A 12 bar, las moléculas de H₂ y N₂ chocan sin parar y absorben el infrarrojo (absorción inducida por colisiones). Ese invernadero sube el ecuador a −40 °C. Es el mecanismo que se propone para los planetas con mucho hidrógeno lejos de su estrella.
- **Mar líquido a −40 °C.** El mar es agua con un ~25 % de amoníaco, que no se congela hasta −55 °C. Entre ±20° de latitud sigue líquido. Más allá, el frío lo congela: polos de hielo de agua y amoníaco.
- **Nubes de amoníaco.** Con un 32 % de NH₃ a 12 bar, el aire está saturado. Hay nubes de cristales de amoníaco, lluvia sobre el mar y escarcha en la tundra. La neblina fotoquímica del amoníaco da el tono ocre del dibujo.
- **Sin cráteres.** La atmósfera densa quema los meteoritos pequeños antes de que lleguen al suelo. Los volcanes cubren con lava los impactos grandes.
- **Volcanes.** Los volcanes son la fuente del amoníaco y del agua. Hay unos 70 volcanes en escudo, algunos activos. El mayor, el **Gran Volcán** (8° N, 50° O), es una isla de ~90 km de radio que sube del fondo del mar a +8 900 m.
- **Anillos inclinados.** Son jóvenes: los restos de una luna que las mareas destrozaron. Con el tiempo se asentarán sobre el ecuador; por ahora siguen inclinados 20°, como en el dibujo. `lockRotation = true` evita que giren con el planeta. Están por encima de la atmósfera, que llega a 138 km.

## Jugabilidad

- **Aterrizar es fácil.** Con 11.5 kg/m³ de aire, los paracaídas frenan casi solos, y un avión sustenta muchísimo.
- **Despegar es muy difícil.** Es casi el doble de denso que Eve, aunque la gravedad es menor (0.93 g frente a 1.7). Hacen falta motores de alto empuje a nivel del mar.
- **Sin oxígeno** (`oxygen = false`): los motores de reacción no funcionan.
- **El mar ecuatorial** se puede amerizar. El Gran Volcán es la meta de escalada del sistema.

## Biomas

| Bioma | Color | × ciencia | Dónde |
|---|---|---|---|
| Mar Ecuatorial | `#2a6a80` | 1.0 | Banda líquida, ±20° |
| Costas Heladas | `#c8b48c` | 1.1 | Borde del mar y de las islas |
| Llanuras de Lava | `#7a3c20` | 1.0 | Roca volcánica de latitudes medias |
| Volcanes | `#ff5a20` | 1.3 | Conos y coladas |
| Tundra de Amoníaco | `#a8a8c0` | 1.1 | Escarcha de NH₃ más allá de ~27° |
| Casquetes Polares | `#f0f0f0` | 1.2 | Más allá de ~62° |
| Gran Volcán | `#ffd040` | 1.6 | 8° N, 50° O |

Hay textos de ciencia propios (`Configs/Norh/Ciencia.cfg`) para el Gran Volcán, los volcanes, los casquetes, las costas y la tundra.

## Archivos

| Archivo | Qué es |
|---|---|
| `Configs/Norh/Norh.cfg` | Cuerpo, órbita, atmósfera (bloque generado), PQS, océano y anillos |
| `Configs/Norh/Ciencia.cfg` | Textos de ciencia |
| `PluginData/Norh/Norh_Color.png` | Vista lejana: neblina ocre al 70 % más terreno al 30 % |
| `PluginData/Norh/Norh_Surface.png` | Terreno real (VertexColorMap) |
| `PluginData/Norh/Norh_Height.png` | h = −2500 + gris × 12000 m |
| `PluginData/Norh/Norh_Normal.png` | DXT5nm (X en alfa, Y en verde, rojo = 255) |
| `PluginData/Norh/Norh_Biomes.png` | Biomas (colores exactos de la tabla) |
| `PluginData/Norh/Norh_Ring.png` | Tira RGBA: u = 0 es el borde exterior; el alfa es la densidad |

También tiene:
- configs de Scatterer (cielo ocre, mar verdoso) y EVE (nubes de amoníaco color tostado);
- PlanetShine (albedo 0.40);
- scatters de Parallax (rocas volcánicas, losas de lava y bloques de hielo polar);
- respaldo de texturas para cuando falta CTTP.

La lámina para el artista es `docs/referencias_artista/20_Norh.png`.
