# Creus y Halum — ficha de concepto (versión final)

Este documento cierra los huecos de concepto que dejó el diseño. La física y los números de juego están en
[DISENO.md](DISENO.md). Lo marcado como **(nuevo)** es historia añadida en este refinamiento; se puede vetar sin tocar los `.cfg` de órbitas ni atmósferas.

## La historia del sistema **(nuevo)**

**Creus y Halum son un binario errante que Kerbol capturó.** Se formaron juntos en otro sistema, como dos planetas ligados entre sí. Una inestabilidad los expulsó y vagaron millones de años por el espacio interestelar. Al cruzar la nube exterior de Kerbol quedaron atrapados en una órbita lejanísima.

Esto explica cuatro cosas del concepto original:

| Rasgo | Explicación |
|---|---|
| A 800 KAU, mucho más allá de cualquier otro planeta | Kerbol no los formó: los capturó. Las capturas de planetas errantes acaban en órbitas así de amplias |
| Halum, casi solo hidrógeno, mantiene un océano líquido | En el espacio interestelar un planeta errante con hidrógeno a presión conserva su calor interno, porque el H₂ comprimido absorbe el infrarrojo. Es la idea de Stevenson (1999) sobre planetas errantes con océanos. Halum sobrevivió así antes de ser capturado |
| Una separación de 5 KAU | Los binarios anchos se forman ligados y viajan juntos; una captura suave no los separa |
| El anillo oscuro y Ocrea | Durante la captura, una luna original de Creus se acercó demasiado y se rompió: sus restos son el anillo y Pastora. Más tarde Creus capturó a Ocrea de la nube exterior, por eso gira al revés |

Desde Halum, Creus es solo un punto: a 5 KAU mide 0.0035° en el cielo. Para un kerbal en Halum, su gemelo es la estrella más brillante, por encima del propio Kerbol.

## Creus

| Capa | Profundidad (desde la cota 0, a 10 atm) | Qué hay |
|---|---|---|
| Atmósfera alta | +410 km … +100 km | H₂ con 5 % de CH₄. Tropopausa a 35 K y 0.19 atm |
| Nubes de metano | ~+70 km (~1 atm) | La capa blanca que se ve desde fuera. Oculta el azul del metano gaseoso |
| Nubes de agua | −100 km … −200 km | Ocultas para siempre bajo el metano; aquí el agua se condensa en nubes de hielo y gotas |
| **Océano supercrítico** | Desde ~−400 km (≈0.8 R) | Agua, metano y algo de amoníaco por encima de 647 K y 218 atm: ni líquido ni gas |
| Lluvia de diamantes | > −1 000 km | La presión rompe el metano y el carbono cae como diamante. Se ha reproducido en laboratorio para Urano y Neptuno |
| Agua superiónica y núcleo | Centro, ~500 km de radio | Agua superiónica conductora alrededor de un núcleo de roca y hielo. Ese agua genera un campo magnético torcido que da auroras fuera de los polos |

**Fuente de calor:** emite más energía de la que recibe de Kerbol, unos 0.4 W/m², por la contracción lenta y el calor de formación, como Neptuno. Por eso su tropopausa está a 35 K y no a los 9 K que daría el Sol.

**Lugares con nombre** (para anomalías futuras):
- **Gran Tormenta Blanca**, a 28° S: un anticiclón que sube metano fresco y lo vuelve aún más blanco.
- **La División**: el hueco central del anillo.

## Halum

| Capa | Profundidad | Qué hay |
|---|---|---|
| Atmósfera | +212 km … 0 | 92 % H₂ y 8 % Ne a 7 atm y 32 K. Nubes de hidrógeno líquido entre ~1.2 y 0.9 atm |
| Océano de neón líquido | 0 … −310 m | Neón con H₂ disuelto, transparente como el cristal |
| **Neón supercrítico** | −310 m … ~−30 km | Ni líquido ni gas: la densidad crece sin una superficie que la separe |
| Manto | ~−30 km … centro | Hidrógeno sólido comprimido. No hay núcleo rocoso apreciable: el 99 % de su masa es H |

**Fuente de calor (resuelto):** con un 99 % de hidrógeno no hay roca radiactiva que lo caliente. El calor viene de la **contracción lenta** de un planeta de gas, como en Júpiter. Lo atrapa el **efecto invernadero del H₂ a 7 atm**: el hidrógeno comprimido absorbe el infrarrojo. Hacen falta unos 0.07 W/m², parecido al calor interno de la Tierra.

**Origen de las islas (resuelto):** el agua no es de Halum. Llega con los **cometas de la nube exterior**, los mismos de los que viene Heraldo. Cada impacto deja hielo de agua (0.93 g/cm³), que flota en el neón (1.21 g/cm³) y se va acumulando en balsas a la deriva. Las islas más grandes son la suma de miles de impactos. Su relieve de hasta +930 m es hielo apilado, no roca.

**Lugares con nombre** (para anomalías futuras):
- **Archipiélago del Náufrago**: la mayor balsa de hielo.
- **La Fosa Crítica**: la fosa más profunda, en pleno neón supercrítico.
- **Mar de las Calmas**: neón sin oleaje, liso como un espejo.

## Ruta de exploración sugerida

1. **Relé de espacio profundo**: la pareja de RA-K, sin la cual no hay control remoto.
2. **Aerocaptura en Creus**: su atmósfera de 410 km frena las llegadas rápidas que el diseño prevé, porque el viaje se hace quemando por encima de la velocidad de escape.
3. **Ocrea y Pastora**: aterrizajes sin atmósfera para practicar; la caza de fumarolas da ciencia ×1.7.
4. **Halum**: amerizar es fácil, porque los paracaídas rinden muchísimo en 9.3 kg/m³. Volver a órbita es difícil: 7 atm con 0.55 g. Es la misión final del sistema.
5. **Prima y Secunda**: escalas en la órbita de Halum, siempre a ±60° de él.
