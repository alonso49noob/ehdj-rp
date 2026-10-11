# Mundos Lejanos — versión de prueba (10-10-2026)

Gracias por probarlo. Es un planet pack de Kopernicus con dos sistemas y dos planetas nuevos:
- **Creus–Halum**: un binario errante capturado a 800 KAU de Kerbol.
- **Kraken**: una enana marrón T2 a 2 años luz kerbales.
- **Norh**: un planeta nuevo del sistema de Kerbol, entre Dres y Jool.
- **Skolta**: un "Titán cálido" del sistema de Kerbol, entre Duna y Dres, con su luna Ceniza.

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

Usa una **partida nueva**: el pack añade 27 cuerpos. La primera carga es lenta porque Kopernicus crea su caché. Se probó **sin OPM**.

## Ir rápido a cualquier sitio
Menú de depuración: `Alt+F12` → Cheats → **Set Orbit**. Pon una nave en órbita del cuerpo que quieras probar.

## Qué probar

- [ ] **Kraken** parece una enana T: bandas granate y pardo rojizo, sin corona y con luz tenue y rojiza (sin tonos violeta).
- [ ] Los **tres discos** de Kraken se ven desde el Tracking Station; el del Cinturón Oscuro casi no se ve.
- [ ] Los **polos** de Creus, Halum, Scarch, Tenebris y Vestigia ya no tienen cuñas de luz ni de sombra.
- [ ] **En vuelo**, los planetas del sistema Kraken quedan iluminados por Kraken (luz rojiza) y no por Kerbol (luz blanca).
- [ ] **Krax**: la Fundición (20° N, 60° O) tiene agujas metálicas de las máquinas (requiere Parallax).
- [ ] **Scarch**: los Campos de Extracción tienen máquinas. Haz un experimento allí: los registros están **en inglés**.
- [ ] **Tenebris**: es inhabitable (sin oxígeno; los motores de reacción no funcionan), pero fácil de colonizar: tiene agua líquida, paracaídas útiles y 5 °C. En 18° S 140° E están los restos de una máquina.
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
- [ ] **Norh** (entre Dres y Jool):
  - los anillos de hielo se ven inclinados y no giran con el planeta;
  - el cielo es ocre y el mar ecuatorial es líquido;
  - aterrizar con paracaídas es fácil; despegar de nuevo es muy difícil (12 bar);
  - el Gran Volcán (8° N, 50° O) mide 9 km: ¿se puede escalar?
- [ ] **Skolta** (entre Duna y Dres, órbita inclinada 19°):
  - desde el espacio es una bola naranja, como Titán;
  - el mar de amoníaco es incoloro: crema en la orilla, casi negro mar adentro y gris ámbar visto de lejos; las naves flotan peor que en agua;
  - busca las bahías azules junto a los volcanes y los yacimientos de cobre (azul y violeta);
  - en Ceniza, el Monte Solitario (12° N, 75° E).
- [ ] Con Scatterer y EVE: las nubes no se duplican (Halum, Tenebris y Salus cambian a texturas sin nubes).

## Problemas conocidos
- **Tracking Station**: a veces ilumina el sistema Kraken con la luz de Kerbol. Es el selector de estrella de Kopernicus, que elige la estrella más cercana a la cámara. En vuelo debería ir bien; confírmalo, por favor.
- La plataforma de lanzamiento de la colonia de Tenebris aún no está colocada.
- Las máquinas usan modelos provisionales de Parallax: las agujas metálicas de Moho.

## Cómo informar
Envía:
- `Kerbal Space Program/KSP.log`;
- la carpeta `Kerbal Space Program/Logs/Kopernicus/`;
- capturas de lo que veas raro, con el nombre del cuerpo.
