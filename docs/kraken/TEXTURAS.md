# Texturas del sistema Kraken

Las reglas de formato y estilo son las mismas de [../TEXTURAS.md](../TEXTURAS.md): equirectangulares 2:1, color en DXT1, altura en R16 y biomas en PNG sin compresión.
Todas existen ya como **provisionales**, en `GameData/MundosLejanos/PluginData/<Cuerpo>/`. Para sustituir una, guarda la versión final con el mismo nombre y ejecuta `python herramientas/validar_pack.py`.

**Pintad pensando en la luz rojiza.** En el juego todo se ve a través de `sunlightColor = 1, 0.55, 0.48` con intensidad 0.35, así que los blancos salen color salmón y los verdes y azules se apagan. Evitad los azules saturados: bajo esta enana no hay luz azul que reflejar. `docs/kraken/preview_kraken.png` simula esa luz.

**Vista lejana y terreno van por separado** en los tres mundos con atmósfera gruesa (Scarch, Tenebris y Salus):
- `_Color` es lo que se ve desde órbita, con neblina o nubes horneadas.
- `_Surface` es el terreno real, sin nubes, y lo usa `VertexColorMap`.

Estado: ⭐ prioridad para el arte final.

## Kraken (estrella)

| ⭐ | Archivo | Clave | Final | Contenido |
|---|---|---|---|---|
| ⭐ | `Kraken/Kraken_Bands.png` | `ScaledVersion › Material › sunspotTex` | 4096×2048, gris | **Aspecto de enana T**: zonas claras (blanco) y cinturones oscuros, con bordes turbulentos y unos 9 huecos ovales en las nubes. El shader lo tiñe entre `emitColor0` #4d0a1f y `emitColor1` #8c1a3d, con los cinturones hacia #140309 |
| | `Kraken/Kraken_Noise.png` | `noiseMap` | 1024×512 RGB | Turbulencia fina estirada en latitud; cada canal en una escala distinta |
| ⭐ | `Kraken/Kraken_DiskInner.png` | `Rings › Ring` (1º) | 2048×16 RGBA | Disco interior caliente: polvo anaranjado `#b8643a`, fino |
| ⭐ | `Kraken/Kraken_Disk.png` | `Rings › Ring` (2º) | 2048×16 RGBA | **Disco protoplanetario**: pardo rosado `#8c6a62`, opaco (alfa hasta 0.75), con cúmulos y dos huecos (x = 0.40, órbita de Ignea, y x = 0.72) |
| | `Kraken/Kraken_DarkBelt.png` | `Rings › Ring` (3º) | 2048×16 RGBA | Polvo del Cinturón Oscuro: `#20181c` con alfa ≤ 0.3, **apenas visible** |

En las tiras, **u = 0 es el borde exterior** y u = 1 el interior. Los discos no tienen luz propia: el color se ve tal cual.

## Krax — mundo de carbono (Moho)

| ⭐ | Archivo | Final | Contenido |
|---|---|---|---|
| ⭐ | `Krax_Color.png` (también la usa `VertexColorMap`) | 2048×1024 DXT1 | Grafito casi negro en 4 tonos (`#3a3a42` a `#141417`), con 4 cráteres jóvenes de rayos grises `#4a4a55`. **La Fundición** (20° N 60° O): 6 terrazas que alternan `#4a2a26` y `#3a201e`, y 4 zanjas `#5a3a30` en X |
| ⭐ | `Krax_Height.png` | 4096×2048 R16 | `h = −1800 + gris × 3600`. Escarpes lobulados (fallas de contracción de 650 m), 90 cráteres y la mina en terrazas de 1.5 km de profundidad |
| | `Krax_Normal.png`, `Krax_Biomes.png` | 2048×1024 | 5 biomas (Fundición ×2.0) |

## Scarch — sauna volcánica (Eve)

| ⭐ | Archivo | Final | Contenido |
|---|---|---|---|
| ⭐ | `Scarch_Color.png` | 4096×2048 DXT1 | **Neblina gris rojiza** en bandas (`#9b7a70`, `#8a6a62`, `#76585a`) al 65 %, con el terreno apenas visible debajo |
| ⭐ | `Scarch_Surface.png` | 4096×2048 DXT1 | Tierra gris rojiza (`#8a6a62`, `#76585a`, `#62484a`), lava oscura `#3a2c2c` con grietas `#c8502a`, **nieve orgánica** marrón (`#b8925e`, `#c9a46e`) en cumbres y polos, fondo marino de limo `#3a3430` y **rejillas industriales** (`#2e2a2c`, `#4a4446`) en los Campos de Extracción |
| ⭐ | `Scarch_Height.png` | 8192×4096 R16 | `h = −4000 + gris × 9000`. Un 40 % de mar, 12 volcanes en escudo con caldera y 3 campos de pozos nivelados de 52 km de radio |
| | `Scarch_Normal.png`, `Scarch_Biomes.png` | 2048×1024 | 6 biomas (Campos de Extracción ×2.0) |
| | `Scarch_Haze.png` *(v2)* | 4096×2048 DXT5 | Capa EVE de neblina y nieve: el ciclo visible |

## Tenebris — mundo oscuro (Laythe)

| ⭐ | Archivo | Final | Contenido |
|---|---|---|---|
| ⭐ | `Tenebris_Color.png` | 4096×2048 DXT1 | Terreno oscuro más un 30 % de nubes grises (`#706c6a`, `#9c9894`) |
| ⭐ | `Tenebris_Surface.png` | 4096×2048 DXT1 | **Sin vegetación**: llanuras de basalto (`#2a2724` a `#181716`), tierras altas `#2c2c32` y `#3a3a42`, playas oscuras `#3a3632`, fondo marino `#0e1114`, casquetes `#c8c8c8`. La **colonia** (12° N 35° E) es una meseta gris `#5a5a60` con luces `#ffd890`; el **cráter de la máquina** (18° S 140° E), `#2a1a18` con óxido `#5a3020` |
| ⭐ | `Tenebris_Height.png` | 8192×4096 R16 | `h = −4000 + gris × 8000`. Un 35 % de tierra. **La meseta de la colonia, a +320 m, debe quedar plana** porque la plataforma de Kerbal Konstructs va encima |
| | `Tenebris_Normal.png`, `Tenebris_Biomes.png` | 2048×1024 | 6 biomas (Restos de la Máquina ×2.5) |
| | `Tenebris_Clouds.png` *(v2)* | 4096×2048 DXT5 | Capa de nubes EVE |

## Salus — océano hipersalino (Laythe)

| ⭐ | Archivo | Final | Contenido |
|---|---|---|---|
| ⭐ | `Salus_Color.png` | 4096×2048 DXT1 | Océano gris verdoso (`#244648` a `#13292a`), aguas someras `#8aa49a`, islas de sal `#d8d0c0`, hielo salobre polar `#e0e2de` y un 25 % de nubes |
| ⭐ | `Salus_Surface.png` | 4096×2048 DXT1 | Lo mismo sin nubes ni hielo: lecho marino, plataformas someras e islas (sal `#d8d0c0`, roca `#4a4440` en las laderas) |
| ⭐ | `Salus_Height.png` | 8192×4096 R16 | `h = −2500 + gris × 3600`; **nivel del mar en gris 0.694**. Exactamente un 3 % de tierra: arcos de islas en los bordes de 4 cuencas de impacto |
| | `Salus_Normal.png`, `Salus_Biomes.png` | 2048×1024 | 5 biomas |

## Lunas, Ignea y Cinturón Oscuro

Todas a 1024×512, con color, normal, altura y biomas (Depresiones, Llanuras, Crestas). Los dos últimos salen de la altura.

| Cuerpo | Altura (`offset` / `deformity`) | Aspecto |
|---|---|---|
| **Vestigia** (luna de Salus) | −1200 / 3600 | Basalto vitrificado gris (`#807a74`, `#6a6460`, `#57524e`) con cráteres |
| **Nox** (luna de Salus) | −3000 / 6000 | Casi negra (`#141416` a `#09090a`), forma irregular |
| **Lumen** (luna de Tenebris) | −2000 / 5000 | Hielo sucio de polvo (`#9c9894`, `#86827e`, `#6e6a68`); solo el casquete sur es nieve limpia `#cfccc8` |
| **Ignea** (2048×1024) | −500 / 1200 | Costra negra (`#4a2a20` a `#2a1a16`), **grietas incandescentes** `#f0b040`, mar de magma `#e0602a` con piel `#8a3018`. El brillo debe ir pintado |
| **Fuligo** | −2500 / 6000 | `#1a1a1d` a `#0e0e10`, con cráteres frescos `#3a3a40` (lo único visible) |
| **Caligo** | −2500 / 6000 | `#19171a` a `#0c0b0d` |
| **Atra** | −3000 / 7000 | `#161618` a `#0a0a0b` |
| Azabache · Brea · Tizne · Escoria · Hollín | −3000/6000 … −1200/2400 | Negros con matices: azulado, pardo, neutro, escoria parda, el más oscuro |

## Texturas de EVE (las genera `generar_visuales.py`)

| Archivo | Uso |
|---|---|
| `<Cuerpo>_EVECoverage.png` | Cobertura en gris (canal R) para las nubes volumétricas V5 |
| `<Cuerpo>_EVEClouds.png` | Capa 2D RGBA (color de nube + alfa = cobertura) |
| `<Cuerpo>_ScaledEVE.png` | Vista lejana sin nubes de Halum, Tenebris y Salus. Solo se usa con EVE instalado |

Si el artista pinta las nubes por separado, estas tres salen de su capa de nubes y la vista lejana normal (`_Color`) queda como "terreno + nubes".

## Modelos 3D (no son texturas, pero hacen falta)

Las máquinas usan provisionalmente las agujas y racimos de Moho de Parallax. Para tener máquinas propias hacen falta:

| Modelo | Uso | Formato |
|---|---|---|
| Torre extractora, refinería y módulo (3 LOD cada uno) | Scatters de Krax y Scarch | `.mu` exportado con PartTools de Unity, más su textura y normal |
| Máquina derribada (1 modelo grande) | Restos de Tenebris | Ídem |
| Plataforma de la colonia | Kerbal Konstructs | Puede reutilizar un modelo de KSCExtended |
