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
    "Kraken": ("Enana T2: gigante gaseoso incandescente granate-magenta, sin corona.", [
        "El shader de estrella no usa textura de color: usa Kraken_Bands (sunspotTex) y Kraken_Noise (noiseMap).",
        "Bands: gris, zonas claras = blanco, cinturones = oscuro, huecos ovales en las nubes. Noise: vetas finas en latitud.",
        "Colores fijados en el .cfg: emitColor0 #4d0a1f → emitColor1 #8c1a3d; cinturones hacia #140309; halo #660f2e.",
        "Discos (tiras 2048×16 RGBA): interior #e07a3a; protoplanetario #d09ab8 con hueco a 250 000 km (Ignea); Cinturón Oscuro #20181c casi invisible."]),
    "Krax": ("Mundo de carbono tipo Mercurio, casi negro (albedo 0.03).", [
        "Grafito en 4 tonos (#3a3a42 → #141417) con brillo metálico; 4 cráteres jóvenes con rayos #4a4a55.",
        "La Fundición (20° N 60° O): mina en 6 terrazas (#4a2a26 / #3a201e) de 60 km y 4 zanjas #5a3a30 en X.",
        "Escarpes lobulados (fallas de contracción). Altura: h = −1800 + gris × 3600."]),
    "Scarch": ("Sauna volcánica de 25 atm bajo neblina gris rojiza; minas de las máquinas.", [
        "Color = neblina en bandas (#9b7a70, #8a6a62, #76585a) al 65 % + terreno al 35 %. Surface = terreno real.",
        "Nieve orgánica #b8925e / #c9a46e en cumbres y polos; lava #3a2c2c con grietas #c8502a; mar ácido (color en el .cfg).",
        "3 Campos de Extracción: rejillas de pozos de 6 km (#2e2a2c, paredes #4a4446). Deben verse artificiales.",
        "Altura: h = −4000 + gris × 9000; 40 % de mar; 12 volcanes en escudo con caldera."]),
    "Tenebris": ("Mundo oscuro de bosques negros y océanos negros; colonia kerbal.", [
        "Bosques #20241d → #121512, basalto #2c2c32 / #3a3a42, playas #3a3632, fondo marino #0c121c, casquetes #c8ccd4.",
        "COLONIA (12° N 35° E): meseta PLANA a +320 m, gris #5a5a60 con luces #ffd890. No alterar su relieve.",
        "Restos de la máquina (18° S 140° E): cráter de 13 km #2a1a18 con anillo de óxido #5a3020.",
        "Nubes grises (#6e727c, #9a9ea8, 30 %); con EVE van aparte. Altura: h = −4000 + gris × 8000."]),
    "Lumen": ("Luna de hielo brillante (albedo 0.85): la lámpara de la noche de Tenebris.", [
        "Paleta #f6f4fa, #e4e1ec, #cdc8da. Lleva cristales de hielo de Parallax encima.",
        "En el juego se verá rosada por la luz de Kraken: pintar en blanco frío, no en rosa."]),
    "Salus": ("Océano hipersalino (97 %): arcos de islas en los bordes de cuencas de impacto.", [
        "Mar #1e4a5a → #0f2a33, someras turquesa #7aa8a8, islas de sal #d8d0c0 con roca #4a4440 en las laderas.",
        "Hielo salobre polar #dfe8ee de borde irregular; nubes blancas (25 %).",
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
MARKS = {"Creus": [("Gran Tormenta", (-28.0, 40.0))],
         "Krax": [("Fundición", SITES["Krax/Fundicion"])],
         "Tenebris": [("Colonia", SITES["Tenebris/Asentamiento"]), ("Restos", SITES["Tenebris/Restos"])]}


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def palette(arr, n=6):
    a = arr.reshape(-1, 3).astype(int)
    key = a[:, 0] * 65536 + a[:, 1] * 256 + a[:, 2]
    u, c = np.unique(key // 4 * 4, return_counts=True)       # agrupa tonos casi iguales
    o = np.argsort(-c)[:n]
    return [("#%06x" % u[i], c[i] / len(key)) for i in o]


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
    title = "Mapa de color" if src.name.endswith("_Color.png") else "Kraken_Bands: el shader de estrella lo tiñe de granate-magenta"
    d.text((x0, y0 - 24), f"{title} (equirectangular 2:1, norte arriba, lon −180°…180°)", font=font(15), fill=DIM)


def thumb(canvas, path, x0, y0, w, h, title):
    if not path.exists():
        return
    im = Image.open(path).convert("RGB").resize((w, h), Image.NEAREST if "Biomes" in path.name else Image.LANCZOS)
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
    system = "Sistema Kraken" if ref["system"] == "Kraken" else "Sistema Creus–Halum"
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
        light = KRAKEN_LIGHT if ref["system"] == "Kraken" else (1.0, 1.0, 1.0)
        for i, (lt, label) in enumerate((((1, 1, 1), "Luz neutra (colores reales)"),
                                         (light, "Con la luz de Kraken" if ref["system"] == "Kraken" else "Con la luz de Kerbol"))):
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
    notes = ["Azabache: carbono vítreo, negro con reflejos azulados. Brea: orgánicos pegajosos pardo-negros.",
             "Tizne: polvo finísimo negro neutro. Escoria: restos fundidos, vetas pardas. Hollín: el más oscuro (0.01).",
             "Formas de patata con cráteres (plantilla Gilly). Texturas 1024×512 bastan; mismas reglas de formato."]
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
