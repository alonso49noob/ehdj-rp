# Texturas del sistema Creus–Halum

El pack ya trae **30 texturas provisionales** generadas por código (`herramientas/generar_texturas.py`).
Los `.cfg` funcionan con ellas. Para sustituir una por la versión final:

1. Guarda el archivo final **con el mismo nombre y en la misma carpeta** (`GameData/MundosLejanos/PluginData/<Cuerpo>/`).
2. Si cambias la extensión a `.dds`, actualiza la ruta en el `.cfg` y ejecuta `python herramientas/validar_pack.py`, que avisa de cualquier ruta rota o bioma descuadrado.

Todas las texturas de planeta son **equirectangulares 2:1** (longitud −180°…180° en horizontal, norte arriba).
Pintadlas sobre una esfera o con ruido 3D (Blender, Gaea, World Machine). Pintar en plano deja costura en ±180° y pellizcos en los polos.

## Guía de estilo (sacada de la imagen de referencia)

Colores planos, posterizados, sin degradados realistas:

| Cuerpo | Paleta (muestreada de `docs/referencia.png`) |
|---|---|
| Creus | `#f6f9f9` (57 %), `#eaefef` (23 %), `#d7e0e0` (15 %), `#cdd6d6` (5 %). Polos más grises y anillo `#404040` |
| Halum | Base `#aac6e2`, vetas de nubes `#edf2f7`, tono intermedio `#cbdcee` y halo azul claro |
| Ocrea | Paleta propia, no viene de la imagen: lecho violeta `#6a6488` / `#5e5878` / `#4a4462`, escarcha de H₂ `#e9e6f2` con borde `#cfcbe0`, glaciares de neón `#bfe3ea` con líneas de flujo `#a6d3dc`, polos `#f6f4fb`, fumarolas `#2f2a44` con pozo `#1f1b30` |

**Orientación:** la Gran Tormenta Blanca de Creus está a **28° S** (en la textura, a u ≈ 0.61 en horizontal). Si en el juego aparece en el hemisferio norte, la textura está volteada.
Muchos packs voltean los DDS en vertical al exportar; comprobadlo con este marcador.

## Formatos

| Tipo de textura | Formato final | Por qué |
|---|---|---|
| Color (vista lejana y `VertexColorMap`) | DDS **DXT1** (BC1); DXT5 si lleva alfa | Rápido y ligero en RAM |
| Normal | DDS **DXT5nm**, o PNG RGBA con la misma disposición: **X (este) en el ALFA, Y (norte) en el verde, rojo = 255** | Los shaders de KSP leen X del alfa. Un PNG RGB normal sale con X = +1: luz torcida y cuñas en los polos (lo comprueba `validar_pack.py`). Además, **planas por encima de ~75°** de latitud |
| Altura (PQS) | DDS **R16** (16 bits, admitido por tu Kopernicus) o PNG gris de 8 bits | Con 8 bits, Halum tiene escalones de 17.6 m |
| Biomas | **PNG RGB sin compresión**, colores exactos y **sin antialiasing** | DXT altera los colores y rompe la detección de biomas |
| Anillo | PNG RGBA o DDS DXT5 | El canal alfa es la densidad del anillo |
| Nubes EVE | DDS DXT5 (RGBA) | El alfa es la cobertura |

---

## Lista de texturas

Estado: ✅ provisional ya generada · ⭐ prioridad para el arte final

### Creus — gigante de hielo (plantilla Jool)

| ⭐ | Archivo | Clave en el `.cfg` | Final recomendado | Contenido |
|---|---|---|---|---|
| ⭐ | `Creus/Creus_Color.png` | `ScaledVersion › Material › texture` | 4096×2048 DXT1 | Bandas de nubes de metano en 4 tonos planos, polos grises y la Gran Tormenta Blanca (óvalo de ~26°×11°) |
| | `Creus/Creus_Normal.png` | `ScaledVersion › Material › normals` | 2048×1024 | Relieve muy suave en los bordes de las nubes; casi plano |
| ⭐ | `Creus/Creus_Ring.png` | `Rings › Ring › texture` | 2048×16 RGBA | Tira horizontal: **u = 0 es el borde exterior y u = 1 el interior** (así muestrea Kopernicus). Color `#404040`; el alfa es la densidad. Lleva una división central |
| | `Creus/Creus_Biomes.png` | `Properties › biomeMap` | 2048×1024 PNG | 6 biomas. Los colores deben coincidir con `Creus.cfg` |

### Halum — mundo de hidrógeno con océano de neón (plantilla Eve)

| ⭐ | Archivo | Clave en el `.cfg` | Final recomendado | Contenido |
|---|---|---|---|---|
| ⭐ | `Halum/Halum_Color.png` | `ScaledVersion › Material › texture` | 4096×2048 DXT1 | Vista desde órbita: base azul con vetas zonales de nubes de H₂ ya horneadas (como en la imagen) e islas apenas visibles |
| | `Halum/Halum_Normal.png` | `ScaledVersion › Material › normals` | 2048×1024 | Relieve suave de las nubes |
| ⭐ | `Halum/Halum_Height.png` | `PQS › Mods › VertexHeightMap › map` | 8192×4096 **R16** | `h = −3500 + gris × 4500 m`. El **nivel del mar es gris 0.778**. Islas de hasta +930 m (~12 % de la superficie), plataformas, fosas de hasta −3 450 m |
| ⭐ | `Halum/Halum_Surface.png` | `PQS › Mods › VertexColorMap › map` | 4096×2048 DXT1 | El terreno real, sin nubes: hielo de agua `#dfe8f2` en las islas, nieve de hidrógeno `#f7fbff` en los polos (≥62°), fondo marino de `#6f8fb5` a `#162444` |
| | `Halum/Halum_Biomes.png` | `Properties › biomeMap` | 2048×1024 PNG | 5 biomas, derivados de la altura y la latitud |
| | `Halum/Halum_Clouds.png` | todavía no se usa | 4096×2048 DXT5 | Capa de nubes con alfa para EVE (v2). Cuando exista el config de EVE, quitar las nubes horneadas de `Halum_Color` |

### Ocrea — luna de escarcha de hidrógeno (plantilla Vall)

| ⭐ | Archivo | Clave en el `.cfg` | Final recomendado | Contenido |
|---|---|---|---|---|
| ⭐ | `Ocrea/Ocrea_Color.png` | `texture` **y** `VertexColorMap` | 4096×2048 DXT1 | Tres materiales planos ordenados por densidad: lecho violeta con cráteres (~32 %), mantos plateados de escarcha de H₂ con un borde más gris (~36 %) y glaciares cian con líneas de flujo en las cuencas (~11 %). Casquetes polares de borde irregular a partir de ~70° y 7 fumarolas con halo oscuro y vetas radiales |
| | `Ocrea/Ocrea_Normal.png` | `normals` | 2048×1024 | Generado desde la altura (exageración ×6). Los mantos y los glaciares deben verse lisos y el lecho, abrupto |
| ⭐ | `Ocrea/Ocrea_Height.png` | `VertexHeightMap › map` | 8192×4096 **R16** | `h = −1000 + gris × 3600 m`, con un relieve real de −750 a +2 430 m. El lecho es abrupto y tiene cráteres. Los glaciares son superficies casi planas que rellenan las cuencas. Los mantos suavizan el terreno y le añaden +150 m. Las fumarolas son pozos de 350 m |
| | `Ocrea/Ocrea_Biomes.png` | `biomeMap` | 2048×1024 PNG | 5 biomas: Lecho Desnudo, Mantos de Hidrógeno, Glaciares de Neón, Campos de Fumarolas (×1.7, pequeños: hay que buscarlos) y Polos de Escarcha |

### Cuerpos menores (plantilla Gilly) — Pastora, Prima, Secunda y Heraldo

Cada uno tiene 4 texturas: `<Cuerpo>_Color`, `_Normal`, `_Height` y `_Biomes`, todas de 1024×512 (con 2048×1024 sobra).

| Cuerpo | Radio | Altura (`offset` / `deformity`) | Aspecto |
|---|---|---|---|
| Pastora | 10 km | −3000 / 6000 | Hollín negro del anillo: `#4a4a4e`, `#3d3d40`, `#2e2e30`. **Rasgo**: cresta ecuatorial de ~3 km, más clara (`#6a6a70`), que le da forma de nuez |
| Prima | 28 km | −8000 / 16000 | Polvo de tolinas rojizo: `#8a7563`, `#6e5a4e`, `#4d4038`. **Rasgo**: binario de contacto; dos lóbulos y un cuello claro (`#cdbba3`) |
| Secunda | 18 km | −4000 / 8000 | Hielo de agua claro: `#d8e0e6`, `#b8c4cc`, `#9aa8b2`. **Rasgo**: acantilado de Verona (3.6 km) en 40° E y coronas ovaladas en 10° S 130° E |
| Heraldo | 5 km | −1500 / 3000 | Costra de cometa negra con manchas de hielo `#c8d4dc`. **Rasgo**: 6 pozos activos con fondo de hielo fresco |

Formas de patata con cráteres. Los biomas (Depresiones, Llanuras, Crestas) salen de la altura.

---

## Opcional, para la v2

| Recurso | Para qué |
|---|---|
| Config de EVE + `Halum_Clouds` | Nubes de hidrógeno reales y en movimiento sobre Halum |
| Config de Scatterer para Creus y Halum | Dispersión atmosférica; Halum tendría un cielo azul intenso |
| Textura de detalle propia del "hielo de neón" | Sustituir `ice.dds` de CTTP en las islas de Halum |
| Partículas o EVE para la bruma de las fumarolas de Ocrea y la cola de Heraldo | Kopernicus no las genera solo |
