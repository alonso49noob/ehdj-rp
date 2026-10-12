"""Láminas de referencia para el artista que sustituirá las texturas provisionales.

Una lámina por cuerpo (más una de asteroides) con: render con luz neutra y con la luz real de su
sistema, mapa de color con rejilla y lugares clave, alturas, biomas con leyenda, paleta y notas.
Salida: docs/referencias_artista/NN_<Cuerpo>.png y MundosLejanos_referencias.pdf
Uso:  python herramientas/generar_referencias.py
"""
import pathlib
import textwrap

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import sistema as S
from generar_texturas import BIOMES, HEIGHTMAPS, SITES
from previsualizar import kraken_star, load, sphere

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEX = ROOT / "GameData" / S.PACK / "PluginData"
OUT = ROOT / "docs" / "referencias_artista"
FONT = "C:/Windows/Fonts/arial.ttf"
BOLD = "C:/Windows/Fonts/arialbd.ttf"
KRAKEN_LIGHT = (1.0, 0.50, 0.66)
ELARA_LIGHT = (1.0, 0.80, 0.62)   # sunlightColor de Elara (K4 V)
BG, FG, DIM = (16, 17, 22), (232, 234, 240), (150, 155, 170)

# cuerpo: (concepto en una línea, notas para el artista)
INFO = {
    "Creus": ("Gigante de hielo blanco: nubes de metano en tonos planos, anillo oscuro.", [
        "Estilo de la imagen original: 4 tonos planos posterizados (#f6f9f9, #eaefef, #d7e0e0, #cdd6d6); polos más grises.",
        "Gran Tormenta Blanca a 28° S: es el marcador de orientación (si sale en el norte, la textura está volteada).",
        "Anillo #404040 de 1.485 a 1.715 radios: tira 2048×16 RGBA, u = 0 es el borde EXTERIOR; el alfa es la densidad.",
        "Gigante gaseoso: el mapa normal debe ser casi plano y totalmente plano en los polos."]),
    "Halum": ("Mundo de hidrógeno: azul con vetas de nubes de H₂, océano de neón e islas de hielo.", [
        "Vista lejana (Color): azul #aac6e2 con vetas zonales #edf2f7 (~24 %) y tono medio #cbdcee.",
        "Terreno real (Surface): islas de hielo de agua #dfe8f2 (12 %), nieve de H₂ #f7fbff en los polos, fondo #6f8fb5 → #162444.",
        "Altura: h = −3500 + gris × 4500, nivel del mar en gris 0.778. Con EVE las nubes van aparte (Halum_EVEClouds).",
        "Hacer la capa de nubes también por separado (RGBA) para EVE."]),
    "Ocrea": ("Luna de escarcha de hidrógeno a 6 K: lecho violeta, mantos plateados, glaciares de neón.", [
        "Capas por densidad: glaciares de neón #bfe3ea planos en las cuencas, lecho de hielo de agua violeta abrupto, mantos de H₂ #e9e6f2 lisos.",
        "7 fumarolas: pozo #1f1b30, halo #2f2a44 con vetas radiales. Casquetes #f6f4fb de borde irregular desde ~70°.",
        "Altura: h = −1000 + gris × 3600. Paleta propia: no viene de la imagen de referencia."]),
    "Pastora": ("Luna pastora del anillo: roca negra de hollín.", [
        "Mismo material que el anillo: #4a4a4e, #3d3d40, #2e2e30. Forma de patata con cráteres.",
        "Altura: h = −3000 + gris × 6000 (deformación grande: es irregular)."]),
    "Prima": ("Troyano L4 de Halum: polvo de tolinas rojizo.", [
        "Paleta #8a7563, #6e5a4e, #4d4038. Cráteres y relieve de patata. h = −5000 + gris × 10000."]),
    "Secunda": ("Troyano L5 de Halum: hielo de agua casi puro.", [
        "Paleta #d8e0e6, #b8c4cc, #9aa8b2. h = −4000 + gris × 8000."]),
    "Heraldo": ("Cometa: costra negra con manchas de hielo.", [
        "Paleta #3a3430, #2a2624, #1c1918 con manchas de hielo #c8d4dc (~5 %). h = −1500 + gris × 3000."]),
    "Kraken": ("Enana T2: gigante gaseoso incandescente rosa y granate, sin corona (textura del artista).", [
        "El shader de estrella no usa textura de color: usa Kraken_Bands (sunspotTex) y Kraken_Noise (noiseMap).",
        "Bands: gris, zonas claras = blanco, cinturones = oscuro, huecos ovales en las nubes. Noise: vetas finas en latitud.",
        "Colores fijados en el .cfg: Fuente: arte/Kraken_Textura.png. emitColor0 #cc4057 → emitColor1 #de455e; bandas oscuras hacia #260d14; halo #731f2e.",
        "Discos (tiras 2048×16 RGBA): interior #b8643a; protoplanetario #8c6a62 con hueco a 250 000 km (Ignea); Cinturón Oscuro #20181c casi invisible."]),
    "Krax": ("Mundo de carbono tipo Mercurio, casi negro (albedo 0.03).", [
        "Grafito en 4 tonos (#3a3a42 → #141417) con brillo metálico; 4 cráteres jóvenes con rayos #4a4a55.",
        "La Fundición (20° N 60° O): mina en 6 terrazas (#4a2a26 / #3a201e) de 60 km y 4 zanjas #5a3a30 en X.",
        "Escarpes lobulados (fallas de contracción). Altura: h = −1800 + gris × 3600."]),
    "Scarch": ("Sauna volcánica de 25 atm bajo neblina gris rojiza; minas de las máquinas.", [
        "Color = neblina en bandas (#9b7a70, #8a6a62, #76585a) al 65 % + terreno al 35 %. Surface = terreno real.",
        "Nieve orgánica #b8925e / #c9a46e en cumbres y polos; lava #3a2c2c con grietas #c8502a; mar ácido (color en el .cfg).",
        "3 Campos de Extracción: rejillas de pozos de 6 km (#2e2a2c, paredes #4a4446). Deben verse artificiales.",
        "Altura: h = −4000 + gris × 9000; 40 % de mar; 12 volcanes en escudo con caldera."]),
    "Tenebris": ("Mundo frío y oscuro bajo 0.2 atm de metano: océanos helados y agua líquida solo en el ecuador.", [
        "Roca de albedo bajísimo #1c1b1a → #100f0e, tierras altas #24232a / #2c2b32, océanos helados (hielo sucio) #7a8088 → #5c6168, mar ecuatorial #0e1114, casquetes #8a8e92.",
        "Respiraderos de metano (6, en la costa ecuatorial): manchas pardas #6a5030 / #4a3a26: ¿tapetes microbianos?",
        "COLONIA (12° N 35° E): meseta PLANA a +320 m, gris #5a5a60 con luces #ffd890. No alterar su relieve.",
        "Restos de la máquina (18° S 140° E): cráter de 13 km #2a1a18 con anillo de óxido #5a3020.",
        "Sin nubes: Color = Surface (atmósfera tenue). Altura: h = −4000 + gris × 8000; la banquisa está a +15–40 m."]),
    "Lumen": ("Luna de hielo sucio (albedo 0.35): la lámpara tenue de la noche de Tenebris.", [
        "Paleta gris #9c9894, #86827e, #6e6a68 (hielo con polvo del disco). Lleva cristales de hielo de Parallax encima.",
        "Solo el polo sur es nieve limpia. La luz de Kraken la teñirá de rojizo: pintar en gris neutro."]),
    "Salus": ("Océano hipersalino (97 %): arcos de islas en los bordes de cuencas de impacto.", [
        "Mar gris verdoso #244648 → #13292a (poco azul: la enana casi no emite azul), someras #8aa49a, islas de sal #d8d0c0 con roca #4a4440 en las laderas.",
        "Hielo salobre polar #e0e2de de borde irregular; nubes blancas (25 %).",
        "Altura: h = −2500 + gris × 3600, nivel del mar en gris 0.694; exactamente un 3 % de tierra en arcos."]),
    "Vestigia": ("Luna nacida del gran impacto de Salus: basalto vitrificado.", [
        "Paleta #807a74, #6a6460, #57524e. Cráteres; superficie vidriosa. h = −1200 + gris × 3600."]),
    "Nox": ("Segunda luna de Salus: roca casi negra capturada del Cinturón Oscuro.", [
        "Paleta #141416, #0e0e10, #09090a (albedo 0.02). h = −3000 + gris × 6000."]),
    "Ignea": ("Protoplaneta con océano de magma dentro del disco.", [
        "Costra #4a2a20 → #2a1a16, grietas #f0b040, mar de magma #e0602a con piel enfriada #8a3018.",
        "KSP no tiene superficies emisivas: el brillo debe ir pintado y saturado. h = −500 + gris × 1200."]),
    "Fuligo": ("Planeta enano del Cinturón Oscuro: hollín orgánico (albedo 0.01).", [
        "Paleta #1a1a1d, #141416, #0e0e10 con cráteres frescos #3a3a40 (los únicos puntos visibles).",
        "Tiene que verse 'apenas': casi negro incluso con luz directa. h = −2500 + gris × 6000."]),
    "Caligo": ("Planeta enano: polvo de carbono finísimo.", [
        "Paleta #19171a, #121114, #0c0b0d. Sin manchas claras. h = −2500 + gris × 6000."]),
    "Atra": ("El menor de los enanos del cinturón: negro y abollado.", [
        "Paleta #161618, #101012, #0a0a0b. h = −3000 + gris × 7000."]),
}
ASTEROIDS = ["Azabache", "Brea", "Tizne", "Escoria", "Hollin"]
# Rasgos únicos de los cuerpos menores (lo que los saca de ser "relleno"): el artista debe conservarlos.
INFO.update({
    "Pastora": ("Luna pastora con forma de nuez: cresta ecuatorial de polvo del anillo.", [
        "RASGO: cresta ecuatorial de ~3 km (como Pan y Atlas), más clara (#6a6a70) que el resto (#4a4a4e → #2e2e30).",
        "La cresta debe ser continua y lisa: es polvo acumulado, no roca. h = −3000 + gris × 6000."]),
    "Prima": ("Troyano L4: binario de contacto de tolinas, con un cuello brillante.", [
        "RASGO: dos lóbulos unidos por un cuello (como Arrokoth). El cuello es el anillo |x| ≈ 0 (meridianos ±90° y polos), más claro (#cdbba3).",
        "Lóbulos de tolinas #8a7563 → #4d4038. La forma está en la altura: h = −8000 + gris × 16000; no aplanarla."]),
    "Secunda": ("Troyano L5 de hielo con el acantilado de Verona (3.6 km).", [
        "RASGO: bloque hundido entre 40° E (pared vertical, cara de hielo #eef3f6) y 80–110° E (rampa suave), entre 32° N y 32° S.",
        "Coronas ovaladas (surcos #aab8c2) en 10° S 130° E. Hielo #d8e0e6 → #9aa8b2. h = −4000 + gris × 8000."]),
    "Heraldo": ("Cometa: costra negra perforada por pozos activos con hielo fresco.", [
        "RASGO: 6 pozos de paredes verticales con fondo de hielo #c8d4dc; costra #3a3430 → #1c1918.",
        "h = −1500 + gris × 3000."]),
    "Vestigia": ("Luna nacida del impacto de Salus, con una cuenca multianillo.", [
        "RASGO: cuenca de tres anillos concéntricos centrada en 10° N 0° (radio ~0.9 rad): fondo de vidrio oscuro #3a3836, anillos #9a948e.",
        "Resto: basalto vitrificado #807a74 → #57524e. h = −1200 + gris × 3600."]),
    "Nox": ("Luna capturada casi negra, con un cráter gigante y surcos paralelos.", [
        "RASGO: cráter que ocupa media cara (5° S 60° E, como Stickney) y surcos paralelos que cruzan todo el cuerpo.",
        "Paleta #141416 → #09090a (albedo 0.02). h = −3000 + gris × 6000."]),
    "Lumen": ("Luna de hielo sucio con franjas de tigre y géiseres en el polo sur.", [
        "RASGO: polo sur (al sur de 55° S) de nieve limpia #cfccc8 con 4–7 grietas paralelas #6a8894 (como Encélado).",
        "Resto: hielo sucio #9c9894 → #6e6a68. El casquete polar debe ser lo único claro."]),
    "Fuligo": ("Planeta enano negro con el Ojo: un cráter de sales brillantes.", [
        "RASGO: el Ojo en 18° N 30° O, un cráter con fondo de sales #e8e4dc (como Occator en Ceres). Es lo único visible desde lejos.",
        "Resto: hollín #1a1a1d → #0e0e10 con cráteres frescos #3a3a40. h = −2500 + gris × 6000."]),
    "Caligo": ("Planeta enano de polvo de carbono, cruzado por una catena.", [
        "RASGO: cadena de 12 cráteres alineados de 20° N 60° O a 10° S 40° E, con fondos #24222a.",
        "Resto: #19171a → #0c0b0d. h = −2500 + gris × 6000."]),
    "Atra": ("Intruso interestelar con forma de puro 3:1 y extremos rojizos.", [
        "RASGO: la forma alargada está en la altura (h = −20000 + gris × 40000, eje ±X): no aplanarla.",
        "Extremos rojizos #2a1c1a (|x| > 0.85, en lon 0° y 180°); resto #161618 → #0a0a0b."]),
})

# Norh (sistema de Kerbol): última lámina antes de la de asteroides, para no renumerar las anteriores
INFO["Norh"] = ("Mundo rocoso helado bajo 12 bar: neblina ocre, mar ecuatorial líquido, volcanes y anillos de hielo.", [
    "Color: neblina ocre en bandas (#a06a34 → #7a4e22) al 70 % + terreno al 30 %; polos más claros (#c49a6a).",
    "Surface: mar #33403f, costas #8a7a68, roca #6e4a34 → #4a3224, coladas #33241c, escarcha #b4aca4, hielo #dfe6ea.",
    "SIN CRÁTERES. Decenas de volcanes con caldera (algunos activos, #e8702a). Gran Volcán: 8° N 50° O, ~90 km de radio, +8 900 m.",
    "Anillos #bcd8ea (borde interior #7d8f9c), 1.45–2.05 R, inclinados 20°. Tira RGBA: u = 0 es el borde EXTERIOR."])

# Skolta y Ceniza (ficha del equipo del 2026-10-11): colores de la paleta de la ficha
INFO["Skolta"] = ("Titán cálido: bruma naranja, mar pálido de amoníaco con hidracina, tierras altas blancas y dunas oscuras.", [
    "Color: bruma naranja (#D68B52 → #A86C3F) al 72 % + terreno muy difuminado al 28 %; casquetes crema #efe6cf.",
    "Surface: tierras altas #EDEBE5/#F2F0EA con vetas #B5CDB0, escarpes #C4C1B9, llanuras #C98C50, volcanes #D9742A/#E0A52A.",
    "Dunas #4A3326/#2E1F18 (15–35°), salinas #F3ECDB, deltas #9A5A38, bahías de azufre #2F4C9E, yacimientos #4E7BE0/#7A5CC8.",
    "Mar (65 %): líquido INCOLORO: fondo somero crema #D6CDB2 (marrón #4A3326 junto a dunas), profundo #3A3028; de lejos gris ámbar #8C7A62.",
    "Bahías de azufre #2F4C9E; cerca del cobre y níquel #4E7BE0. h = −3500 + gris × 12000."])
INFO["Ceniza"] = ("Luna de Skolta: arcillas amoniacadas pardas (como Ceres) y el Monte Solitario.", [
    "Paleta #6a645c → #46413c. RASGO: Monte Solitario en 12° N 75° E, domo de 3 km con vetas claras #c8c4bc.",
    "h = −3000 + gris × 7000."])

# Termos, Tyrna, Karmen, Talia y Akira (fichas del equipo): detrás de Ceniza, antes de la lámina de asteroides
INFO["Termos"] = ("Planeta enano activo bajo 5 atm: lagos de agua casi hirviendo, terrazas de sílice, volcanes y pozos ácidos.", [
    "Color: terreno con velo azulado #c4d0dc (26 %) y nubes de vapor #f3f2ee → #cbced2 (~35 % del cielo, más en el ecuador y los polos).",
    "Surface: basalto #58534c → #393633, toba #aa9c84 → #857a6b en las tierras altas, arcillas verdosas #7e8472 hacia los polos, coladas #2e2a27, calderas activas #d8582a.",
    "Lagos (22 %): agua lechosa, turquesa #9fd6cc en la orilla → #1d5866 en lo profundo; #4f9aa6 desde órbita. Orillas de sínter #ece6d6 con bandas ocres #d29b63.",
    "8 pozos ácidos tropicales (como Dallol): sal #f2ead2, azufre #e6d23a, verde ácido #9cc83c, óxido #c8642a. h = −3000 + gris × 10000. Termos_Clouds: nubes para EVE."])
INFO["Tyrna"] = ("Luna helada de Termos: criovulcanismo y metales por toda la superficie.", [
    "Hielo #e2e8ec → #b2bcc4 salpicado de granos metálicos #8e8a84 (~25 %).",
    "RASGO: 6 fisuras criovolcánicas (arcos de ~70°) con el fondo oscuro #5a4e44 (costras metálicas) y un halo de hielo fresco #f3f7f9.",
    "h = −2000 + gris × 4000."])
INFO["Karmen"] = ("Luna-asteroide de Termos: fragmento del núcleo metálico de un cuerpo roto.", [
    "Metal oscuro #77726c → #4d4a46 (tipo M). RASGO: cara de fractura plana y pulida hacia 0° 90° E (#85827d con reflejos #a29f9a).",
    "La cara plana está en la altura (un plano a 0.82 R del centro): no redondearla. h = −1500 + gris × 3000."])
INFO["Titanus"] = ("Sub-enana marrón de 12 M_J (21 g): nubes en bandas, océano de agua supercrítica, balsas minerales y anillos enormes.", [
    "Color (vista lejana, solo nubes): bandas crema #f3e7cf / #e2c9a0 y cinturones pardos #c99f74 → #7a4a36, con óvalos de tormenta claros.",
    "Surface (fondo del manto, bajo el mar): peridotita verdosa #55604f → #2c312b; dorsales de disolución con sales y sulfuros #e0d2a8 → #a8723c.",
    "Biomas: balsas (16 %) en franjas de convergencia sobre las dorsales; Jardines Químicos (3.7 %) en parte de ellas. h = −9000 + gris × 8600.",
    "Anillo (Titanus_Ring, u = 0 exterior): de 1.6 a 80 radios, roca parda #b9a891 dentro → hielo #d8dde2 fuera, huecos en 3.1, 7.5, 13, 21 y 34 R."])
INFO["Talia"] = ("Planeta enano muerto y saturado de cráteres: el registro de impactos más antiguo del sistema, con metales.", [
    "Regolito gris pardo #a29b92 → #5b5752 según la altura. Cráteres de todos los tamaños, unos sobre otros.",
    "Gran Cuenca (22° S 110° E, 220 km): fondo de vidrio de impacto más oscuro y tres anillos de macizos rotos, algo más claros (#b4ada2).",
    "6 cráteres jóvenes con rayos claros #d2ccc2; 12 afloramientos metálicos #6c717a / #a7abb2 en los bordes de las cuencas.",
    "h = −5500 + gris × 11000."])
INFO["Akira"] = ("Mundo transneidoniano de hielos de N2 y CH4, muy activo y con atmósfera densa: hielo rosado, glaciar y tolinas.", [
    "Color = terreno al 64 % + velo azul #bccbe0 → #98abc8 al 36 %. Surface = terreno real (PQS).",
    "Llanuras de N2 #ece4e6 → #cbbfc4; tolinas ecuatoriales #84503a → #542f24 con cráteres; crestas de metano en cuchillas #b9a9c4 / #a493b3.",
    "Glaciar de Celdas (25° N 160° E, lágrima de 0.42 × 0.30 rad): #eef1f6 con bordes de celda #c3cbd8; montañas de hielo #9b9bab en el borde.",
    "4 criovolcanes #9a6a68 → #784e50 con escarcha fresca #f6f2f4; casquetes #f2f5fa desde ~66°. h = −3000 + gris × 9000."])

MARKS = {"Creus": [("Gran Tormenta", (-28.0, 40.0))], "Norh": [("Gran Volcán", (8.0, -50.0))],
         "Ceniza": [("Monte Solitario", (12.0, 75.0))], "Karmen": [("Cara de Fractura", (0.0, 90.0))],
         "Talia": [("Gran Cuenca", SITES["Talia/GranCuenca"])], "Akira": [("Glaciar de Celdas", SITES["Akira/Glaciar"])],
         "Krax": [("Fundición", SITES["Krax/Fundicion"])],
         "Tenebris": [("Colonia", SITES["Tenebris/Asentamiento"]), ("Restos", SITES["Tenebris/Restos"])]}
MARKS.update({"Secunda": [("Verona", (0.0, 40.0)), ("Coronas", (-10.0, 130.0))], "Vestigia": [("Cuenca", (10.0, 0.0))],
              "Nox": [("Gran Cráter", (-5.0, 60.0))], "Fuligo": [("El Ojo", (18.0, -30.0))],
              "Caligo": [("Catena", (5.0, -10.0))]})


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def palette(arr, n=6):
    """Tonos dominantes. Las texturas llevan grano (ningún píxel repite color exacto): se cuantizan a n colores."""
    q = Image.fromarray(np.asarray(arr, np.uint8)).quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = np.asarray(q.getpalette()[:3 * n]).reshape(-1, 3)
    c = np.bincount(np.asarray(q).ravel(), minlength=n)[:n]
    return [("#%02x%02x%02x" % tuple(pal[i]), c[i] / c.sum()) for i in np.argsort(-c) if c[i]]


def map_panel(canvas, body, x0, y0, w, h):
    d = ImageDraw.Draw(canvas)
    src = TEX / body / f"{body}_Color.png"
    if not src.exists():                                       # Kraken: el shader de estrella usa las bandas
        src = TEX / body / f"{body}_Bands.png"
    col = Image.open(src).convert("RGB").resize((w, h), Image.LANCZOS)
    canvas.paste(col, (x0, y0))
    for lat in (-60, -30, 0, 30, 60):
        y = y0 + int((90 - lat) / 180 * h)
        d.line([(x0, y), (x0 + w, y)], fill=(255, 255, 255, 70) if lat else (255, 220, 120), width=1)
        d.text((x0 - 34, y - 8), f"{lat:+d}°", font=font(13), fill=DIM)
    for lon in range(-150, 181, 30):
        x = x0 + int((lon + 180) / 360 * w)
        d.line([(x, y0), (x, y0 + h)], fill=(255, 255, 255), width=1)
    for name, (lat, lon) in MARKS.get(body, []):
        x, y = x0 + int((lon + 180) / 360 * w), y0 + int((90 - lat) / 180 * h)
        d.ellipse([x - 9, y - 9, x + 9, y + 9], outline=(255, 80, 80), width=3)
        d.text((x + 12, y - 9), name, font=font(15, True), fill=(255, 120, 120))
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=(90, 95, 110))
    title = "Mapa de color" if src.name.endswith("_Color.png") else "Kraken_Bands: el shader de estrella lo tiñe de granate oscuro"
    d.text((x0, y0 - 24), f"{title} (equirectangular 2:1, norte arriba, lon −180°…180°)", font=font(15), fill=DIM)


def thumb(canvas, path, x0, y0, w, h, title):
    if not path.exists():
        return
    im = Image.open(path)
    if im.mode.startswith("I"):                                  # alturas de 16 bits
        im = Image.fromarray((np.asarray(im, np.float32) / 257).astype(np.uint8))
    im = im.convert("RGB").resize((w, h), Image.NEAREST if "Biomes" in path.name else Image.LANCZOS)
    canvas.paste(im, (x0, y0))
    d = ImageDraw.Draw(canvas)
    d.rectangle([x0, y0, x0 + w, y0 + h], outline=(90, 95, 110))
    d.text((x0, y0 - 22), title, font=font(15), fill=DIM)


def sheet(body, num):
    W, H = 1600, 1000
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)
    ref = S.BODIES[body]
    concept, notes = INFO[body]
    system = {"Kraken": "Sistema Kraken", "Kerbol": "Sistema de Kerbol", "Elara": "Sistema Elara"}.get(ref["system"],
                                                                                                    "Sistema Creus–Halum")
    d.text((40, 24), body, font=font(40, True), fill=FG)
    d.text((40 + d.textlength(body, font=font(40, True)) + 20, 40),
           f"{system} · R = {ref['radius'] / 1000:g} km · g = {ref['gee']:g} · plantilla {ref['template']}",
           font=font(18), fill=DIM)
    d.text((40, 76), concept, font=font(20), fill=(220, 200, 160))

    # renders
    if ref.get("kind") == "star":
        star = kraken_star(210)
        canvas.paste(star, (60, 140), star)
        d.text((60, 650), "Aspecto en el juego (shader de estrella)", font=font(15), fill=DIM)
    else:
        tex = load(body, "Color")
        star = {"Kraken": "Kraken", "Elara": "Elara"}.get(ref["system"], "Kerbol")
        light = {"Kraken": KRAKEN_LIGHT, "Elara": ELARA_LIGHT}.get(star, (1.0, 1.0, 1.0))
        for i, (lt, label) in enumerate((((1, 1, 1), "Luz neutra (colores reales)"), (light, f"Con la luz de {star}"))):
            im = sphere(tex, 165, spin=30 + 150 * i, light=lt)
            canvas.paste(im, (40 + i * 360, 150), im)
            d.text((60 + i * 360, 500), label, font=font(15), fill=DIM)

    map_panel(canvas, body, 800, 150, 760, 380)
    thumb(canvas, TEX / body / f"{body}_Height.png", 800, 590, 370, 185, "Altura" + (
        f": h = {HEIGHTMAPS[body]['offset']} + gris × {HEIGHTMAPS[body]['deformity']} m" if body in HEIGHTMAPS else ""))
    if body == "Kraken":
        thumb(canvas, TEX / "Kraken" / "Kraken_Noise.png", 800, 590, 370, 185, "Kraken_Noise (noiseMap)")
        for i, k in enumerate(("DiskInner", "Disk", "DarkBelt")):
            strip = Image.open(TEX / "Kraken" / f"Kraken_{k}.png").convert("RGBA").resize((370, 22))
            bgc = Image.new("RGBA", strip.size, (60, 60, 70, 255))
            bgc.alpha_composite(strip)
            canvas.paste(bgc.convert("RGB"), (1190, 600 + i * 55))
            d.text((1190, 580 + i * 55), f"Kraken_{k} (exterior ← → interior)", font=font(13), fill=DIM)
    else:
        thumb(canvas, TEX / body / f"{body}_Biomes.png", 1190, 590, 370, 185, "Biomas")
        table = BIOMES.get(body, BIOMES["_pequeno"])
        for i, (name, c) in enumerate(table.items()):
            x, y = 1190 + (i % 2) * 190, 785 + (i // 2) * 22
            d.rectangle([x, y + 3, x + 14, y + 17], fill=c)
            d.text((x + 20, y), name, font=font(13), fill=FG)

    # paleta y notas
    if ref.get("kind") != "star":
        pal = palette(np.asarray(Image.open(TEX / body / f"{body}_Color.png").convert("RGB")))
        d.text((40, 545), "Paleta provisional (más frecuente primero)", font=font(15), fill=DIM)
        for i, (hx, frac) in enumerate(pal):
            x = 40 + i * 120
            d.rectangle([x, 570, x + 100, 620], fill=hx, outline=(90, 95, 110))
            d.text((x, 625), f"{hx}  {frac * 100:.0f}%", font=font(13), fill=FG)
    y = 690
    d.text((40, y), "Notas para el artista", font=font(20, True), fill=FG)
    y += 32
    for n in notes:
        for j, line in enumerate(textwrap.wrap(n, 92)):
            d.text((40, y), ("• " if j == 0 else "  ") + line, font=font(16), fill=FG)
            y += 22
        y += 4
    ring = TEX / body / f"{body}_Ring.png"
    if ring.exists():                         # tira del anillo: u = 0 borde exterior (izquierda)
        strip = Image.open(ring).convert("RGBA").resize((700, 14))
        bgc = Image.new("RGBA", strip.size, (60, 60, 70, 255))
        bgc.alpha_composite(strip)
        canvas.paste(bgc.convert("RGB"), (800, 958))
        d.text((800, 940), f"{body}_Ring.png (exterior ← → interior; el alfa es la densidad)", font=font(13), fill=DIM)
    d.text((40, H - 52), "Normales: DXT5nm (X en ALFA, Y en verde, rojo = 255) y planas por encima de ~75° de latitud.",
           font=font(13), fill=(255, 190, 120))
    d.text((40, H - 30), f"Mundos Lejanos · referencia {num:02d} · texturas provisionales generadas por código "
                        f"(GameData/{S.PACK}/PluginData/{body}/)", font=font(13), fill=DIM)
    path = OUT / f"{num:02d}_{body}.png"
    canvas.save(path)
    return path


def asteroid_sheet(num):
    W, H = 1600, 1000
    canvas = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(canvas)
    d.text((40, 24), "Asteroides del Cinturón Oscuro", font=font(40, True), fill=FG)
    d.text((40, 76), "Albedo 0.01–0.02: casi negros; solo se distinguen por el matiz.", font=font(20), fill=(220, 200, 160))
    for i, b in enumerate(ASTEROIDS):
        x = 40 + i * 310
        im = sphere(load(b, "Color"), 120, spin=40, light=(1, 1, 1))
        canvas.paste(im, (x, 140), im)
        r = S.BODIES[b]["radius"] / 1000
        d.text((x, 400), f"{'Hollín' if b == 'Hollin' else b} · {r:g} km", font=font(20, True), fill=FG)
        for j, (hx, _) in enumerate(palette(np.asarray(Image.open(TEX / b / f"{b}_Color.png").convert("RGB")), 3)):
            d.rectangle([x, 440 + j * 40, x + 60, 470 + j * 40], fill=hx, outline=(90, 95, 110))
            d.text((x + 70, 446 + j * 40), hx, font=font(15), fill=FG)
    notes = ["Azabache: facetas planas de carbono vítreo con bordes que destellan en azul (#3c4658).",
             "Brea: blob liso sin cráteres, con charcos planos de brea #0b0908. Tizne: montón de escombros sembrado de bloques.",
             "Escoria: esponja de cientos de vesículas (#2a1a12). Hollín: el más oscuro (0.01), con la BALIZA de las máquinas en 0° 0°.",
             "Formas de patata (plantilla Gilly); 1024×512 bastan. Cada uno conserva su rasgo: es lo que los distingue."]
    y = 640
    d.text((40, y), "Notas para el artista", font=font(20, True), fill=FG)
    for n in notes:
        y += 30
        d.text((40, y), "• " + n, font=font(16), fill=FG)
    path = OUT / f"{num:02d}_Asteroides.png"
    canvas.save(path)
    return path


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    pages = [sheet(b, i + 1) for i, b in enumerate(INFO)]
    pages.append(asteroid_sheet(len(pages) + 1))
    imgs = [Image.open(p).convert("RGB") for p in pages]
    pdf = OUT / "MundosLejanos_referencias.pdf"
    imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=100)
    print(f"{len(pages)} láminas + {pdf.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
