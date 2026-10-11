"""Vista previa del sistema con las texturas actuales, compuesta como la imagen de referencia.

Renderiza cada cuerpo como esfera (proyección ortográfica, luz lambertiana + halo atmosférico)
a escala real entre sí, más el anillo de Creus. Salida: docs/preview_sistema.png
Uso:  python herramientas/previsualizar.py
"""
import pathlib

import numpy as np
from PIL import Image, ImageDraw, ImageFont

import sistema as S

ROOT = pathlib.Path(__file__).resolve().parents[1]
TEX = ROOT / "GameData" / S.PACK / "PluginData"
LIGHT = np.array([-0.45, 0.35, 0.82])
LIGHT = LIGHT / np.linalg.norm(LIGHT)


def load(body, kind):
    return np.asarray(Image.open(TEX / body / f"{body}_{kind}.png").convert("RGB"), np.float32)


def sphere(tex, r, tilt=12.0, spin=0.0, glow=None, light=(1.0, 1.0, 1.0)):
    """Devuelve imagen RGBA (2r+pad) de una esfera texturizada, iluminada con el color `light`."""
    pad = int(r * 0.25) if glow is not None else 2
    size = 2 * (r + pad)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    x, y = (xx - size / 2 + 0.5) / r, -(yy - size / 2 + 0.5) / r
    rr = x * x + y * y
    inside = rr <= 1
    z = np.sqrt(np.clip(1 - rr, 0, 1))
    t = np.radians(tilt)
    # inclinar hacia el observador: rotación sobre el eje x
    yw, zw = y * np.cos(t) - z * np.sin(t), y * np.sin(t) + z * np.cos(t)
    lat = np.arcsin(np.clip(yw, -1, 1))
    lon = np.arctan2(x, zw) + np.radians(spin)
    H, W = tex.shape[:2]
    u = ((lon / (2 * np.pi) + 0.5) % 1 * W).astype(int) % W
    v = np.clip(((0.5 - lat / np.pi) * H).astype(int), 0, H - 1)
    col = tex[v, u]
    shade = np.clip(x * LIGHT[0] + y * LIGHT[1] + z * LIGHT[2], 0, 1) * 0.85 + 0.15
    out = np.zeros((size, size, 4), np.float32)
    out[..., :3] = col * shade[..., None] * np.array(light, np.float32)
    out[..., 3] = np.where(inside, 255, 0)
    if glow is not None:
        d = np.sqrt(rr)
        g = np.clip(1 - (d - 1) / 0.22, 0, 1) ** 2 * (d > 1)
        out[..., :3] = np.where(inside[..., None], out[..., :3], np.array(glow, np.float32))
        out[..., 3] = np.where(inside, 255, g * 200)
        rim = np.clip((d - 0.86) / 0.14, 0, 1) * inside
        out[..., :3] = out[..., :3] * (1 - 0.35 * rim[..., None]) + np.array(glow) * 0.35 * rim[..., None]
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")


def ring_layers(cx, cy, R, back, body="Creus", ring=S.RING, view=4.0):
    """Anillo como elipse plana (vista `view` grados sobre su plano) partida en mitad trasera/delantera."""
    prof = np.asarray(Image.open(TEX / body / f"{body}_Ring.png").convert("RGBA"), np.float32)[0]
    ri, ro = ring["inner"] / 1000 * R, ring["outer"] / 1000 * R
    s = np.sin(np.radians(view))
    w, h = int(2 * ro + 4), int(2 * ro * s + 4)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = xx - w / 2, (yy - h / 2) / s
    d = np.hypot(dx, dy)
    u = np.clip((ro - d) / (ro - ri), 0, 0.999)          # u=0 exterior, u=1 interior (como Kopernicus)
    px = prof[(u * (len(prof) - 1)).astype(int)]
    a = np.where((d >= ri) & (d <= ro), px[..., 3], 0)
    a = np.where((yy < h / 2) if back else (yy >= h / 2), a, 0)
    img = np.dstack([px[..., :3], a]).astype(np.uint8)
    return Image.fromarray(img, "RGBA"), (int(cx - w / 2), int(cy - h / 2))


def main():
    W, H = 1600, 900
    scale = 175 / S.BODIES["Creus"]["radius"]               # px por metro (Creus = 175 px como en la ref.)
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    cx, cy, Rc = 900, 430, 175 * 1.6
    k = Rc / 175
    back, pos = ring_layers(cx, cy, Rc, True)
    canvas.alpha_composite(back, pos)
    cre = sphere(load("Creus", "Color"), int(Rc), tilt=4)
    canvas.alpha_composite(cre, (int(cx - cre.width / 2), int(cy - cre.height / 2)))
    front, pos = ring_layers(cx, cy, Rc, False)
    canvas.alpha_composite(front, pos)

    def place(body, x, y, glow=None, spin=0):
        r = max(int(S.BODIES[body]["radius"] * scale * k), 3)
        im = sphere(load(body, "Color"), r, spin=spin, glow=glow)
        canvas.alpha_composite(im, (int(x - im.width / 2), int(y - im.height / 2)))
        return r

    place("Halum", 230, 250, glow=(205, 225, 245))
    place("Ocrea", 250, 600, spin=40)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
    d = ImageDraw.Draw(canvas)
    small_x = 1300
    for i, b in enumerate(["Prima", "Secunda", "Pastora", "Heraldo"]):
        y = 140 + i * 180
        big = sphere(load(b, "Color"), 55, spin=30 * i)
        canvas.alpha_composite(big, (small_x + 60 - big.width // 2, y - big.height // 2))
        d.text((small_x + 130, y - 24), f"{b}\n{S.BODIES[b]['radius']/1000:g} km\n(ampliado)", font=f,
               fill=(200, 205, 215))
    for name, x, y in (("Creus  2 100 km", cx - 80, cy + Rc + 30), ("Halum  690 km", 160, 360),
                       ("Ocrea  380 km", 180, 670)):
        d.text((x, y), name, font=f, fill=(220, 225, 235))
    out = ROOT / "docs" / "preview_sistema.png"
    canvas.convert("RGB").save(out)
    print(out)


def detalle(body, r=260, folder="docs"):
    """Primer plano de un cuerpo: dos hemisferios opuestos (docs/preview_<cuerpo>.png)."""
    tex = load(body, "Color")
    canvas = Image.new("RGBA", (4 * r + 120, 2 * r + 80), (0, 0, 0, 255))
    for k, spin in enumerate((0, 180)):
        im = sphere(tex, r, tilt=18, spin=spin)
        canvas.alpha_composite(im, (40 + k * (2 * r + 40), 40))
    out = ROOT / folder / f"preview_{body.lower()}.png"
    canvas.convert("RGB").save(out)
    print(out)


def norh_preview():
    """Norh con sus anillos de hielo inclinados, como en el dibujo del concepto (docs/norh/preview_norh_anillos.png)."""
    W, H = 1400, 1100
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    cx, cy, R, roll = W // 2, H // 2, 300, -55                # roll: giro de la elipse en pantalla
    glow = (200, 140, 80)

    def put(layer):
        im = layer.rotate(roll, resample=Image.BICUBIC, expand=True)
        canvas.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

    back, _ = ring_layers(cx, cy, R, True, body="Norh", ring=S.NORH_RING, view=24)
    put(back)
    pl = sphere(load("Norh", "Color"), R, tilt=20, spin=130, glow=glow)
    canvas.alpha_composite(pl, (int(cx - pl.width / 2), int(cy - pl.height / 2)))
    front, _ = ring_layers(cx, cy, R, False, body="Norh", ring=S.NORH_RING, view=24)
    put(front)
    d = ImageDraw.Draw(canvas)
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 24)
    d.text((40, H - 70), "Norh  1 207 km · 0.94 masas de Kerbin · 12 bar · anillos de hielo (1.45–2.05 R, 20°)",
           font=f, fill=(225, 200, 170))
    out = ROOT / "docs" / "norh" / "preview_norh_anillos.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(out)
    print(out)


def kraken_star(r):
    """Kraken como en el juego: emitColor0→1 según Kraken_Bands (sunspotTex), cinturones hacia sunspotColor,
    oscurecimiento de borde y un halo granate tenue (rimColor). Sin iluminación: es la fuente de luz."""
    bands = np.asarray(Image.open(TEX / "Kraken" / "Kraken_Bands.png").convert("L"), np.float32) / 255
    pad = int(r * 0.25)
    size = 2 * (r + pad)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    x, y = (xx - size / 2 + 0.5) / r, -(yy - size / 2 + 0.5) / r
    d = np.sqrt(x * x + y * y)
    inside = d <= 1
    z = np.sqrt(np.clip(1 - d * d, 0, 1))
    t = np.radians(10)
    yw, zw = y * np.cos(t) - z * np.sin(t), y * np.sin(t) + z * np.cos(t)
    lat, lon = np.arcsin(np.clip(yw, -1, 1)), np.arctan2(x, zw)
    H, W = bands.shape
    b = bands[np.clip(((0.5 - lat / np.pi) * H).astype(int), 0, H - 1), ((lon / (2 * np.pi) + 0.5) * W).astype(int) % W]
    c0, c1 = np.array([0.17, 0.04, 0.05]) * 255, np.array([0.34, 0.08, 0.09]) * 255
    spot = np.array([0.05, 0.01, 0.012]) * 255
    col = c0 + (c1 - c0) * b[..., None]
    col = col * b[..., None] ** 0.4 + spot * (1 - b[..., None] ** 0.4)                # cinturones oscuros
    col = col * (0.55 + 0.45 * z[..., None])                                           # oscurecimiento de borde
    halo = np.clip(1 - (d - 1) / 0.25, 0, 1) ** 2.5 * (d > 1)
    out = np.zeros((size, size, 4), np.float32)
    out[..., :3] = np.where(inside[..., None], col, np.array([61, 13, 13], np.float32))
    out[..., 3] = np.where(inside, 255, halo * 140)
    return Image.fromarray(out.clip(0, 255).astype(np.uint8), "RGBA")


def kraken_preview():
    """Sistema Kraken: la enana y sus mundos a escala entre sí (planetas aparte, con la luz rojiza de la enana)."""
    W, H = 1600, 900
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    star = kraken_star(330)
    canvas.alpha_composite(star, (-star.width // 2 + 120, H // 2 - star.height // 2))
    f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
    fs = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    d = ImageDraw.Draw(canvas)
    d.text((40, H - 60), "Kraken  6 300 km (T2, 1 250 K)", font=f, fill=(220, 170, 160))
    light = (1.0, 0.55, 0.48)                                    # sunlightColor de Kraken
    scale = 110 / S.BODIES["Salus"]["radius"]                   # Salus = 110 px
    glows = {"Scarch": (170, 120, 110), "Tenebris": (115, 100, 95), "Salus": (140, 152, 146)}
    for b, x in zip(["Krax", "Scarch", "Tenebris", "Salus", "Ignea"], [560, 760, 960, 1200, 1430]):
        r = max(int(S.BODIES[b]["radius"] * scale), 6)
        im = sphere(load(b, "Color"), r, spin=20, glow=glows.get(b), light=light)
        y = 250
        canvas.alpha_composite(im, (x - im.width // 2, y - im.height // 2))
        d.text((x - 45, y + r + 28), f"{b}\n{S.BODIES[b]['radius'] / 1000:g} km", font=fs, fill=(220, 200, 215))
    # Lunas y Cinturón Oscuro, ampliados
    for b, x in zip(["Lumen", "Vestigia", "Nox", "Fuligo", "Caligo", "Atra", "Azabache"],
                    [560, 720, 880, 1040, 1200, 1360, 1510]):
        im = sphere(load(b, "Color"), 45, spin=30, light=light)
        y = 560
        canvas.alpha_composite(im, (x - im.width // 2, y - im.height // 2))
        d.text((x - 40, y + 60), f"{b}\n{S.BODIES[b]['radius'] / 1000:g} km", font=fs, fill=(220, 200, 215))
    d.text((560, 430), "Planetas a escala entre sí (no respecto a Kraken), bajo la luz de la enana.",
           font=fs, fill=(170, 150, 165))
    d.text((560, 690), "Lunas (Lumen de Tenebris; Vestigia y Nox de Salus) y Cinturón Oscuro: ampliados.",
           font=fs, fill=(170, 150, 165))
    out = ROOT / "docs" / "kraken" / "preview_kraken.png"
    canvas.convert("RGB").save(out)
    print(out)


if __name__ == "__main__":
    main()
    detalle("Ocrea")
    kraken_preview()
    for body in ("Scarch", "Tenebris", "Salus"):
        detalle(body, folder="docs/kraken")
    norh_preview()
    detalle("Norh", folder="docs/norh")
    (ROOT / "docs" / "skolta").mkdir(exist_ok=True)
    detalle("Skolta", folder="docs/skolta")
    detalle("Ceniza", r=160, folder="docs/skolta")
    (ROOT / "docs" / "termos").mkdir(exist_ok=True)
    for body, r in (("Termos", 260), ("Talia", 260), ("Tyrna", 160), ("Karmen", 120)):
        detalle(body, r=r, folder="docs/termos")
    (ROOT / "docs" / "akira").mkdir(exist_ok=True)
    detalle("Akira", folder="docs/akira")
