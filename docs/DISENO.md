# Diseño del sistema Creus–Halum

Las cifras de este documento salen de `herramientas/sistema.py`, que es la fuente única de los parámetros.
`herramientas/validar_pack.py` comprueba que los `.cfg` coinciden con ella.

## Decisiones aprobadas

| # | Decisión | Motivo |
|---|---|---|
| 1 | El sistema orbita a **880 KAU** de Kerbol (1.197 × 10¹³ m; antes 800 KAU) | Con motores muy eficientes que queman por encima de la velocidad de escape se llega en un tiempo razonable. Su influencia gravitatoria apenas altera el resto del sistema de Kerbol |
| 2 | Creus y Halum están separados **5 KAU** | Decisión del creador del concepto. Deja sitio para lunas futuras dentro de la SOI de Creus (12.3 KAU) |
| 3 | El binario es **Halum orbitando a Creus** | Las cónicas por tramos son estables y los periodos salen correctos. Un baricentro invisible desfasaría los periodos con masas distintas |
| 4 | Halum es el planeta azul de la imagen. El planeta rocoso era la referencia de escala (Kerbin) | No se usa para ningún cuerpo |
| 5 | Ocrea se rediseñó como **luna de escarcha de hidrógeno** | La versión anterior copiaba la imagen de Kerbin. El concepto nuevo solo es posible a 880 KAU y enlaza con el hidrógeno y el neón de Halum |

1 KAU = semieje mayor de Kerbin = 13 599 840 256 m.

## Cálculo visual de radios

Lo hizo `docs/medicion_radios.png`, con perfil radial de brillo sobre `docs/referencia.png`:

| Cuerpo | px | r / R_Creus | Valor elegido |
|---|---|---|---|
| Creus | 174.8 | 1.000 | 2 100 km |
| Halum | 57.2 (sin contar el halo) | 0.327 | 690 km |
| Rocoso (escala = Kerbin) | 50.5 | 0.289 | Solo fija la escala: 1 px = 11.88 km |
| Anillo | 259.5–299.5 | 1.485–1.713 | `innerRadius = 1485`, `outerRadius = 1715` (milésimas de R, convención verificada con Sarnus de OPM) |

## Cuerpos

| Cuerpo | Padre | Radio | g | Órbita | Plantilla | Notas |
|---|---|---|---|---|---|---|
| **Creus** | Kerbol | 2 100 km | 0.80 | a = 880 KAU, e = 0.03, i = 3.1° | Jool | Gigante de hielo. SOI de 13.5 KAU. Anillo oscuro de 1.485 a 1.715 R |
| **Halum** | Creus | 690 km | 0.55 | a = 5 KAU, e = 0.04, i = 2.5° | Eve | Océano de neón, 7 atm, 32 K. Periodo de 2 058 años kerbales |
| **Ocrea** | Creus | 380 km | 0.18 | a = 22 000 km, e = 0.05, **i = 152° (retrógrada)** | Vall | Capturada, en rotación síncrona. Escarcha de H₂, glaciares de neón y fumarolas, a ~6 K |
| **Pastora** | Creus | 10 km | 0.03 | a = 3 700 km (justo fuera del anillo) | Gilly | Luna pastora. **SOI ampliada a 40 km** (la de Laplace sería de 13.8 km) |
| **Prima** | Creus | 28 km | 0.012 | Órbita de Halum + 60° (L4) | Gilly | Troyano de tolinas |
| **Secunda** | Creus | 18 km | 0.009 | Órbita de Halum − 60° (L5) | Gilly | Troyano de hielo de agua |
| **Heraldo** | Kerbol | 5 km | 0.002 | rp = 4.2 KAU, ra = 880 KAU, i = 28° | Gilly | Cometa. Pasa por el perihelio en el año 4 de la partida |

El validador comprueba que ninguna SOI se solapa ni toca la atmósfera o el anillo de Creus.

## Física

### Halum: el océano de neón
- El punto crítico del neón está en **44.4 K y unos 27 atm**. A 7 atm en superficie el océano es **líquido**.
- El océano se vuelve **supercrítico a partir de unos 310 m de profundidad**: la presión del neón (1.21 t/m³ con 0.55 g) supera las 27 atm y, si el fondo está por encima de 44 K, la fase líquida desaparece. En el juego, el bioma *Abismo Supercrítico* marca las fosas.
- **La superficie tiene que estar entre 29 y 36 K.** Por debajo de 29 K el H₂ se condensa a 7 atm, y por encima de 36 K el neón hierve. Se eligieron **32 K**.
- **El calor viene de dentro.** A 880 KAU, Kerbol da unos 9 K de equilibrio (2 mW/m²). Halum necesita un flujo interno de **unos 0.07 W/m²**, parecido al de la Tierra (0.087).
- **Las islas flotan.** El hielo de agua (0.93 g/cm³) es menos denso que el neón líquido (1.21), así que flota. El hielo de neón (1.44) se hunde.
- **Las nubes son de hidrógeno.** Con una adiabática húmeda de κ ≈ 0.25, el H₂ se satura hacia 1.2 atm y 20.6 K. Las vetas blancas de la imagen son esas nubes.
- **Atmósfera:** 92 % H₂ y 8 % Ne evaporado del océano, con M = 3.5 g/mol. γ = 1.62, porque a 32 K la rotación del H₂ está congelada.
  - Densidad en superficie: **9.3 kg/m³** (1.5 veces la de Eve).
  - Velocidad del sonido: 351 m/s.
  - Techo: **212 km**.
  - Velocidad orbital a 100 km: 1.8 km/s.

### Ocrea: la luna de escarcha de hidrógeno
- **Es el lugar más frío del sistema.** La escarcha refleja ~90 % de la poca luz que llega y queda a **~5.5–6 K**. El lecho desnudo (albedo ~0.3) llega a ~9 K.
- **Lo brillante sigue brillante.** A 9 K el H₂ sólido tiene ~59 Pa de presión de vapor; a 6 K, ~0.06 Pa. El hidrógeno se escapa del lecho oscuro y se vuelve a depositar sobre la escarcha. Plutón y Calisto separan así sus zonas claras y oscuras.
- **Las capas se ordenan por densidad:**
  - el neón sólido (1.44 g/cm³) se acumula en las cuencas como glaciares planos;
  - el hielo de agua (0.93) forma el lecho;
  - el hidrógeno sólido (0.086) lo cubre todo con mantos lisos que entierran los cráteres.
- **El neón es permanente.** Su presión de vapor a 6 K es de ~10⁻⁸ Pa. Es un sólido blando, así que fluye muy despacio, como los glaciares de nitrógeno de Plutón.
- **La atmósfera es prácticamente nula:** menos de 1 µbar de H₂ en equilibrio con la escarcha, así que no se modela en KSP. El hidrógeno escapa despacio: con v_esc = 1.16 km/s y v_térmica = 0.22 km/s, el parámetro de Jeans es λ ≈ 27.
- **Las fumarolas** son el resto del calor de la captura. La órbita retrógrada todavía es excéntrica (e = 0.05) y las mareas de Creus mantienen 7 puntos a ~14 K, donde el H₂ no puede seguir sólido. Cada uno es un pozo de 350 m con un halo oscuro de lecho expuesto.

### Creus
- **Atmósfera:** 94 % H₂, 5 % CH₄ y 1 % H₂O, con M = 2.9 g/mol y γ = 1.43.
  - La cota 0 está a 10 atm y 116 K, que es el límite de aplastamiento.
  - Hacia arriba sigue una adiabática (κ = 0.30) hasta la tropopausa, a 35 K y 0.19 atm. Después la temperatura sube hasta 75 K.
  - Techo: **410 km**. Densidad en la cota 0: 3.0 kg/m³.
- **Es blanco** porque el metano se condensa en nubes altas y oculta la absorción del metano gaseoso, que hace azules a Urano y Neptuno.
- **Océano supercrítico:** agua por encima de 647 K y 218 atm, a miles de km de profundidad, como en Urano y Neptuno. En el juego queda bajo la cota de aplastamiento, así que solo aparece en los textos de ciencia.
- **Anillo oscuro:** hollín de metano irradiado, como los anillos de Urano, con albedo de unos 2 %.

### Curvas de atmósfera
Las genera `herramientas/generar_atmosferas.py`:
- Integra el equilibrio hidrostático con g(h) = g₀(R/(R+h))² sobre el perfil T(p).
- Coloca 22 claves cada 0.75 de ln p, con tangentes dp/dh exactas.
- Pone a cero las curvas de Sol y latitud, porque a 880 KAU la luz de Kerbol no calienta.

## Jugabilidad

| Tema | Dato |
|---|---|
| Viaje Hohmann desde Kerbin | 4 008 años kerbales (~102 h reales a 100 000×). El Δv no es el problema: ~2.7 km/s desde LKO más ~0.3 km/s de captura. Lo que acorta el viaje es quemar por encima de la velocidad de escape, como se decidió |
| Entre Creus y Halum | Unos 7 años a 1 km/s (11 min reales a 100 000×). La velocidad orbital de Halum es de solo 23 m/s |
| Energía | Kerbol da 1/640 000 de la luz que hay en Kerbin: los paneles solares no sirven. Hacen falta RTG o fisión (Near Future Electrical) |
| Comunicaciones | La antena más potente instalada (5 × 10¹¹) llega a ~37 KAU. El pack añade el **RA-K Relé de Espacio Profundo** (2 × 10¹³, nodo `largeUnmanned`): una pareja de relés enlaza ambos sistemas con ~40 % de señal en el afelio |
| Ciencia | Multiplicadores entre ×8 y ×25. Hay biomas con bonus: Campos de Fumarolas ×1.7, Abismo Supercrítico ×1.6, Gran Tormenta Blanca ×1.5 |
| Heraldo | El cometa pasa por el perihelio en el año 4. Es el único trozo de la nube exterior al alcance del sistema interior, pero va a más de 6 km/s |

## Ideas implementadas (todas las aprobadas)

| Idea | Implementación |
|---|---|
| Islas a la deriva de hielo de agua | Bioma de Halum, mapa de altura y texto de ciencia sísmico |
| Nubes de hidrógeno | Vetas de la textura de Halum, capa `Halum_Clouds` para EVE y textos de ciencia |
| Biomas de Halum | Mar de Neón, Islas a la Deriva (islas, continentes de hielo flotante y la franja de témpanos frente a ellos), Nieves de Hidrógeno, Abismo Supercrítico y Bajos Helados |
| Creus blanco por nubes de metano | Textura y descripción |
| Anillo oscuro con luna pastora | Anillo, Pastora en su borde exterior y textos de ciencia |
| Biomas de Creus por bandas | 5 bandas más la Gran Tormenta Blanca |
| Luna capturada con actividad propia | Ocrea, rediseñada como mundo de escarcha de hidrógeno (ver Física) |
| Troyanos de Halum | Prima (L4) y Secunda (L5) |
| Cometa de periodo largo | Heraldo |
| Paneles solares inútiles | Documentado aquí. El parche de CommNet añade el relé de espacio profundo |
