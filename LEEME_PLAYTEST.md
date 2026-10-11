# Mundos Lejanos — versión de prueba (10-10-2026)

Gracias por probarlo. Es un planet pack de Kopernicus con dos sistemas:
- **Creus–Halum**: un binario errante capturado a 800 KAU de Kerbol.
- **Kraken**: una enana marrón T2 a 2 años luz kerbales.

Las texturas son **provisionales**: las pintará un artista más adelante.

## Instalación

1. Copia la carpeta `GameData/MundosLejanos` dentro de `Kerbal Space Program/GameData/`.
2. Imprescindibles: **Kopernicus** (probado con 1.12.1-247), **ModuleManager** y **CTTP** (Community Terrain Texture Pack). KSP 1.12.x.
3. Opcionales, que el pack aprovecha si están instalados:

| Mod | Qué aporta |
|---|---|
| Parallax Continued + Parallax_StockScatterTextures | Rocas, cristales y las máquinas |
| Scatterer + StockScattererConfigs | Atmósferas y océanos |
| EVE (Blackrack) + StockVolumetricClouds | Nubes volumétricas |
| PlanetShine | Luz reflejada por los planetas |

Usa una **partida nueva**: el pack añade 24 cuerpos. La primera carga es lenta porque Kopernicus crea su caché. Se probó **sin OPM**.

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
