# Akira: implementación en KSP

Se basa en la ficha del equipo (Discord): "Akira es un mundo transneidoniano compuesto de hielos de metano y nitrógeno. […] diámetro excepcionalmente grande de 900 km, pero al parecer no afecta a objetos como Plock y Ervo debido a su considerable lejanía. Se ubica a 200 KAU de Kerbol y es excepcionalmente activo. Su atmósfera es sorprendentemente densa y estable."

![Akira](preview_akira.png)

## Valores de la ficha

| | Ficha | En el pack |
|---|---|---|
| Tamaño | 900 km de diámetro, "excepcionalmente grande" | **R = 450 km, sin dividir.** A diferencia de las fichas de Termos y Talia, esta ya está a escala de KSP: lo compara con Plock (378 km en OPM), y a ÷10 mediría 90 km, nada excepcional |
| Gravedad | No la da | **0.2 g** (1.96 m/s²): un mundo de hielo, menos denso que Eeloo (0.17 g con 210 km) |
| Distancia | 200 KAU | a = 2.72 Tm, e = 0.12, i = 17°. Año de ~2 830 años de Kerbin. Muy por fuera de Eeloo (6.6 KAU) y de los planetas de OPM |
| Composición | Hielos de metano y nitrógeno | Llanuras de hielo de N₂ con CH₄ y CO, crestas de CH₄ y, debajo, una corteza de hielo de agua |
| Actividad | Excepcionalmente activo | 4 criovolcanes con escarcha fresca y un glaciar de N₂ en convección |
| Atmósfera | Sorprendentemente densa y estable | **1.2 atm**: 92 % N₂, 5 % CH₄, 3 % CO (M = 27.4 g/mol). 62 K (−211 °C) en el ecuador y ~56 K en los polos. Techo a 165 km |
| Plock y Ervo | No los afecta | A 200 KAU no hay nada cerca. Plock es de OPM; "Ervo" no está en este pack ni en OPM |

**La física de la atmósfera.** A 62 K, el hielo de nitrógeno solo sostiene unos 0.09 bar: una atmósfera de 1.2 atm debería congelarse sobre la superficie. La ficha la llama "sorprendente", así que se dejó como un misterio del lore: la mantienen los criovolcanes, que expulsan nitrógeno sin parar. Los textos de ciencia lo comentan.

Con 0.2 g, la atmósfera es muy alta: se cortó en 1·10⁻⁵ atm (165 km, 0.37 radios), en vez del 1·10⁻⁶ del resto de los cuerpos. La estratosfera está más caliente (80 K) por el metano, como en Plutón.

## Mapa y biomas

| Bioma | Color del mapa | × ciencia | Dónde |
|---|---|---|---|
| Llanuras de Nitrógeno | `#e0e8ff` | 1.0 | Hielo rosado de N₂ con algo de CH₄, la mayor parte de la superficie |
| Glaciar de Celdas | `#80c0ff` | 1.5 | Cuenca en forma de lágrima en 25° N, 160° E, rellena de N₂ que convecciona en celdas de varios km (como Sputnik Planitia) |
| Crestas de Metano | `#c0a0ff` | 1.3 | Tierras altas: cuchillas de hielo de CH₄ |
| Tierras de Tolinas | `#804020` | 1.2 | Franja ecuatorial rojiza y antigua, la única con cráteres |
| Criovolcanes | `#ff40c0` | 1.7 | 4 montes anchos con cráter central y escarcha fresca alrededor |
| Casquetes Polares | `#ffffff` | 1.1 | Más allá de ~66° |
| Montañas de Hielo | `#606080` | 1.4 | Bloques de hielo de agua que flotan en el borde del glaciar, como icebergs |

**Vista desde el espacio.** El terreno se ve bajo un velo azul (36 %), como la bruma de Plutón: hielo rosado y blanco, la lágrima clara del glaciar y la franja rojiza de tolinas.

## Visuales opcionales

- **Scatterer:** cielo azul oscuro.
- **PlanetShine:** albedo 0.65.
- **Parallax:** bloques de hielo, cuchillas de metano y rocas de tolinas.
- **Sin EVE.** La ficha no habla de nubes.

## Archivos

| Archivo | Qué es |
|---|---|
| `Configs/Akira/Akira.cfg` | Cuerpo, órbita, atmósfera (bloque generado) y PQS |
| `Configs/Akira/Ciencia.cfg` | Textos de ciencia |
| `PluginData/Akira/Akira_{Color,Surface,Height,Normal,Biomes}.png` | Mapas provisionales |

## Pendiente

- **Probarlo en el juego.** Hay que ver sobre todo cómo se ve con tan poca luz (Kerbol llega 40 000 veces más débil que a Kerbin) y si los 165 km de atmósfera molestan al orbitar.
- **Viajar hasta él.** A 200 KAU, una transferencia de Hohmann desde Kerbin tarda unos 500 años de Kerbin: hace falta un mod de propulsión avanzada o de viaje rápido, como para Creus–Halum.
