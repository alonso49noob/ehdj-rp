# Sistema Kraken — diseño

Los números salen de `herramientas/sistema.py`, y `herramientas/validar_pack.py` comprueba que los `.cfg` coinciden con él.
Configs: `GameData/MundosLejanos/Configs/Kraken/` (cuerpos) y `Configs/Visuales/` (Scatterer, EVE y PlanetShine).
Vista previa: [preview_kraken.png](preview_kraken.png). Láminas para el artista: [../referencias_artista/](../referencias_artista/).

## Decisiones

| # | Decisión |
|---|---|
| 1 | Kraken es una **enana T2 coherente con la física**: 1 250 K, ~400 millones de años, 22 masas de Jool y **1.05 radios de Jool** |
| 2 | Está a **0.2 kly kerbales** (~12 650 KAU; hasta el 11-10-2026 eran 2 kly): 1 kly = 63 241 KAU = 8.60 × 10¹⁴ m, así que a = 1.72 × 10¹⁴ m. La doble precisión en esa posición es de 3 cm |
| 3 | Halus pasó a llamarse **Salus** y Testis a **Vestigia** ("huellas, restos" en latín) |
| 4 | **Máquinas** = scatters de Parallax (más rocas nativas). Su historia se descubre en **registros de ciencia en inglés** |
| 5 | Lunas nuevas: **Lumen** (Tenebris) y **Nox** (Salus). **Tres discos** visibles desde el Tracking Station. **Cinturón Oscuro** de planetas enanos y asteroides |
| 6 | **Aspecto de enana T**: gigante gaseoso incandescente con bandas granate y pardo rojizo, sin corona |
| 7 | Configs visuales opcionales: **Scatterer** (con océanos), **EVE** (2D + volumétricas V5) y **PlanetShine** |

Con unos 400 millones de años ya no queda gas primordial: técnicamente los discos son de escombros de segunda generación. En el juego se llaman discos protoplanetarios.

## La enana

- **Masa y tamaño:** μ = 6.216 × 10¹⁵ (22 veces la de Jool), R = 6 300 km y g = 16. Rotación de 5 h.
- **Luz:** L = 6.9 × 10¹⁹ W. Kopernicus mide `luminosity` en W/m² a 1 KAU, donde Kerbol vale 1360, así que Kraken lleva **0.0297**.
- **Color de la luz:** rojo apagado y tenue, como unas brasas: `sunlightColor = 1, 0.55, 0.48` con intensidad 0.35. El metano y el sodio absorben el amarillo y el verde, y casi no queda azul. Por eso los océanos de Tenebris y Salus son grises y verdosos, no azules.
- **Aspecto:** shader de estrella de Kopernicus con texturas propias:
  - `sunspotTex = Kraken_Bands`: zonas claras, cinturones oscuros y 9 huecos en las nubes, por donde asoma el interior caliente. Así son las enanas T reales, que varían de brillo.
  - `noiseMap = Kraken_Noise`: turbulencia fina.
  - Colores: `emitColor0` #4d0a1f, `emitColor1` #8c1a3d, cinturones hacia #140309 y halo tenue, **sin corona**.

### Discos

Los tres discos son **sin luz propia** (`unlit`) y con `fadeoutMinAlpha = 1`, así que no se desvanecen al alejar la cámara.

| Disco | Radio | Aspecto |
|---|---|---|
| Interior | 36 000–50 000 km (entre Krax y Scarch) | Polvo caliente anaranjado |
| Protoplanetario | 150 000–400 000 km | Rosa malva y opaco. Hueco a 250 000 km, donde orbita Ignea, y otro a 330 000 km |
| Cinturón Oscuro | 450 000–820 000 km | Polvo casi negro: **apenas visible** |

## Cuerpos

Todos los cuerpos cercanos a Kraken están en **rotación síncrona**: la enana nunca se mueve en su cielo.

| Cuerpo | Padre | Órbita | Periodo | R | g | Plantilla | Notas |
|---|---|---|---|---|---|---|---|
| **Krax** | Kraken | 28 400 km | 3.35 h | 260 km | 0.45 | Moho | Carbono, albedo 0.03; la **Fundición** de las máquinas |
| **Scarch** | Kraken | 58 000 km | 9.8 h | 650 km | 0.80 | Eve | 25 atm de CO₂ y CH₄ a 50 °C, 38.9 kg/m³; mar ácido; Campos de Extracción |
| **Tenebris** | Kraken | 76 000 km | 14.7 h | 560 km | 0.29 | Laythe | **Frío y oscuro** (referencia del equipo): 0.2 atm de metano, sin invernadero. Océanos helados (35 %) y agua líquida solo en el ecuador; roca de albedo bajísimo; respiraderos de metano (¿vida?); colonia en cúpulas; restos de una máquina. Día de 36 h |
| ↳ **Lumen** | Tenebris | 1 400 km | 3.1 h | 90 km | 0.08 | Minmus | Hielo sucio de polvo del disco (albedo 0.35); solo las **franjas de tigre** del polo sur, con sus géiseres, dejan nieve limpia. Más cerca que antes porque la SOI de Tenebris (0.29 g) es de 2 214 km. Alumbra las noches de Tenebris |
| **Salus** | Kraken | 95 000 km | 20.5 h | 750 km | 1.00 | Laythe | 97 % de océano de salmuera; arcos de islas |
| ↳ **Vestigia** | Salus | 3 000 km | 3.9 h | 120 km | 0.12 | Ike | Restos del gran impacto; **cuenca multianillo**; cae en espiral |
| ↳ **Nox** | Salus | 4 600 km, retrógrada | 7.3 h | 35 km | 0.02 | Gilly | Capturada del Cinturón Oscuro; casi negra; **cráter gigante y surcos** |
| **Ignea** | Kraken | 250 000 km (hueco del disco) | 87.5 h | 180 km | 0.15 | Dres | Protoplaneta con océano de magma |

### Cinturón Oscuro (450 000–820 000 km, albedo 0.01–0.02)

| Cuerpo | Órbita | R | Plantilla | Rasgo |
|---|---|---|---|---|
| **Fuligo** | 520 000 km | 140 km | Dres | El mayor. **El Ojo**: cráter con sales brillantes, lo único visible desde lejos |
| **Caligo** | 605 000 km | 95 km | Bop | Polvo de carbono; una **catena** de 12 cráteres alineados |
| **Atra** | 690 000 km | 70 km | Bop | **Puro 3:1** de origen interestelar (como ʻOumuamua) |
| Azabache · Brea · Tizne · Escoria · Hollín | 480 000–780 000 km | 4–12 km | Gilly | Facetas vítreas · charcos de brea · bloques · vesículas · **la baliza de las máquinas** (Hollín) |

El validador comprueba que ninguna SOI se solapa y que todas miden al menos el doble del radio de su cuerpo. Las órbitas del cinturón tienen bandas radiales separadas.

No añadí el generador de asteroides de Kopernicus a propósito: crea asteroides de serie, que son claros, y contradiría el albedo bajo del cinturón.

## Física (resumen)

- **Krax:** absorbe el 97 % de la luz. Su media es de 413 K, frente a 381 K con un albedo normal, y llega a 311 °C en el punto subestelar.
- **Scarch:** una neblina orgánica cíclica lo mantiene en 50 °C y cae como nieve. El metano lo reponen los volcanes y las máquinas.
- **Tenebris** (referencia del equipo, con el diámetro actual de 1 120 km y la gravedad de la referencia, 2.87 m/s²):
  - Atmósfera tenue de metano (0.2 atm, 97 % CH₄) sin efecto invernadero: 3 °C en el ecuador y ~−67 °C en los polos.
  - Los océanos están congelados en el 35 % de la superficie; solo una franja ecuatorial sigue líquida.
  - Roca de albedo bajísimo. El metano lleva millones de años aumentando: en la costa ecuatorial hay 6 respiraderos con manchas pardas, quizá vida metanógena (bioma ×2).
  - Gira con un día de 36 h: con rotación síncrona el agua líquida estaría en un solo punto, no en una franja ecuatorial.
  - Con 0.29 g y un gas tan ligero, la atmósfera se extendería miles de km. Se corta en 1e-4 atm: techo a 527 km, por debajo de la órbita de Lumen.
  - La colonia vive en cúpulas cerca del mar ecuatorial, de donde saca el agua.
  - De la referencia no se usó la masa (5.2 masas lunares, incompatible con el diámetro actual) ni el origen del metano en la exosfera de Arkennia, que no existe en el pack.
- **Salus:** la sal baja el punto de congelación a −20 °C, así que el océano sigue líquido a −5 °C. Pasó por hiceano porque el H₂ sale de la serpentinización del fondo.
- **Lumen:** albedo de 0.35. Es la única luz de las noches de Tenebris.
- **Cinturón Oscuro:** hollín orgánico irradiado, de la misma química que Krax pero aún más oscuro.

## Las máquinas

| Dónde | Bioma (×ciencia) | Qué se ve (Parallax) | Registros (en inglés) |
|---|---|---|---|
| **Krax**, 20° N 60° O | Fundicion de las Maquinas (×2.0) | Mina en terrazas de 60 km, torres, refinerías y módulos | Dónde se replican |
| **Scarch**, 3 zonas | Campos de Extraccion (×2.0) | Rejillas de pozos de 6 km con extractoras | Qué extraen; su metano alimenta la nieve |
| **Tenebris**, 18° S 140° E | Restos de la Maquina (×2.5) | Cráter de 13 km con una máquina derribada | Qué opinan de los kerbals |
| **Hollín**, 0° 0° | Baliza (×1.6) | Plataforma nivelada con una aguja | Que estuvieron en el cinturón antes que nadie: un nodo repetidor hacia Scarch |

Los modelos son provisionales: las agujas y racimos de Moho de `Parallax_StockScatterTextures`.

**Arreglo tras la primera prueba:** el `KSP.log` mostraba "Celestial body X is missing the Parallax PQSMod" y no aparecía ningún scatter. `Parallax_PQS.cfg`, que se genera con `generar_scatters.py`, añade ese PQSMod a los 10 cuerpos con scatters. El validador lo comprueba.

## La luz de Kraken en el Tracking Station

En la primera prueba algunos planetas salieron iluminados con luz blanca desde la dirección equivocada. El log lo explica:

```
20:42:19 StarLightSwitcher: Set active star => Kraken
20:45:28 StarLightSwitcher: Set active star => Sun     <- todavía en el Tracking Station
```

En el Tracking Station Kopernicus activa la estrella **más cercana a la cámara**. A 0.2 kly su cálculo a veces elige Kerbol. Es un comportamiento de Kopernicus, no de los configs.

**En vuelo usa la posición de la nave, y la luz debería ser siempre la de Kraken** (pendiente de confirmar en el juego).

El pack añade **PlanetShine**, la luz que cada mundo refleja sobre las naves, con el color medio de su textura y una intensidad proporcional a su albedo. Así Krax y el Cinturón Oscuro apenas reflejan, y Lumen y Creus reflejan mucho.

## Visuales opcionales (`Configs/Visuales/`, generados por `generar_visuales.py`)

| Mod | Qué añade |
|---|---|
| **Scatterer** | Atmósferas de Creus, Halum, Scarch, Tenebris y Salus. Océanos de Halum (neón líquido: transparente, n = 1.09), Scarch (turbio), Tenebris (negro; atmósfera muy tenue) y Salus (salmuera espumosa). Destello rojo apagado y tenue para Kraken. Las lunas proyectan eclipses |
| **EVE** (Blackrack, volumétricas V5) | Nubes 2D y volumétricas en Creus, Halum, Scarch y Salus, con mapas de cobertura sacados de sus texturas (Tenebris no tiene nubes: su atmósfera es muy tenue). Con EVE, Halum y Salus cambian a una vista lejana **sin nubes horneadas** (`_ScaledEVE`), para que no se dupliquen |
| **PlanetShine** | Luz reflejada de los 24 cuerpos, más Kraken como fuente |

## La colonia de Tenebris

El mapa de altura tiene una **meseta plana a +320 m en 12° N 35° E** (bioma Asentamiento Kerbal).

1. Lleva una nave a la meseta.
2. Abre el editor de Kerbal Konstructs desde su botón de la barra de herramientas.
3. Coloca una plataforma de lanzamiento (los modelos de KSCExtended sirven) y configúrala como *LaunchSite*.
4. Guarda y envíame la config que genera. La integro en el pack.
