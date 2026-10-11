"""Texturas PROVISIONALES del pack (equirectangulares 2:1, PNG).

Estilo plano/posterizado como la imagen de referencia; paletas muestreadas de docs/referencia.png.
Todo se genera con ruido 3D sobre la esfera (sin costura en lon=±180° ni pellizco en los polos).
Las rutas de salida son las que esperan los .cfg; los artistas pueden sustituir cada archivo
por la versión final con el mismo nombre (ver docs/TEXTURAS.md).

Uso:  python herramientas/generar_texturas.py [cuerpo ...]
"""
import pathlib
import sys
import time

import numpy as np
from PIL import Image

import sistema as S

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "GameData" / S.PACK / "PluginData"

# Alturas codificadas en el mapa de grises: h = offset + gris * deformity  (igual que en los .cfg)
HEIGHTMAPS = {
    "Halum":   dict(offset=-3500, deformity=4500),
    "Ocrea":   dict(offset=-1000, deformity=3600),
    "Pastora": dict(offset=-3000, deformity=6000),
    "Prima":   dict(offset=-5000, deformity=10000),
    "Secunda": dict(offset=-4000, deformity=8000),
    "Heraldo": dict(offset=-1500, deformity=3000),
    # sistema Kraken
    "Krax":     dict(offset=-1800, deformity=3600),
    "Scarch":   dict(offset=-4000, deformity=9000),
    "Tenebris": dict(offset=-4000, deformity=8000),
    "Salus":    dict(offset=-2500, deformity=3600),
    "Vestigia": dict(offset=-1200, deformity=3600),
    "Nox":      dict(offset=-3000, deformity=6000),
    "Lumen":    dict(offset=-2000, deformity=5000),
    "Fuligo":   dict(offset=-2500, deformity=6000),
    "Caligo":   dict(offset=-2500, deformity=6000),
    "Atra":     dict(offset=-3000, deformity=7000),
    "Azabache": dict(offset=-3000, deformity=6000),
    "Brea":     dict(offset=-2500, deformity=5000),
    "Tizne":    dict(offset=-2000, deformity=4000),
    "Escoria":  dict(offset=-3000, deformity=6000),
    "Hollin":   dict(offset=-1200, deformity=2400),
    "Ignea":    dict(offset=-500, deformity=1200),
}

# Lugares fijos (lat, lon en grados de la textura) que también usan los .cfg y la documentación
SITES = {
    "Krax/Fundicion": (20.0, -60.0),          # mina a cielo abierto de las máquinas
    "Tenebris/Asentamiento": (12.0, 35.0),    # meseta plana para la colonia (Kerbal Konstructs)
    "Tenebris/Restos": (-18.0, 140.0),        # cráter de la máquina derribada
}

# Colores de bioma (deben coincidir exactamente con los .cfg; validar_pack.py lo comprueba)
BIOMES = {
    "Creus": {"Casquete Norte": "#5b8fd9", "Banda Templada Norte": "#7fd1c7",
              "Cinturon Ecuatorial": "#f2e394", "Banda Templada Sur": "#d98fb5",
              "Casquete Sur": "#9a7fd9", "Gran Tormenta Blanca": "#ff6b4a"},
    "Halum": {"Abismo Supercritico": "#1b2a6b", "Mar de Neon": "#3a6fd8",
              "Bajos Helados": "#6fd6e8", "Islas a la Deriva": "#e8d36f",
              "Nieves de Hidrogeno": "#f4f4f4"},
    "Ocrea": {"Lecho Desnudo": "#6a4c9c", "Mantos de Hidrogeno": "#b8a8f0",
              "Glaciares de Neon": "#5fd0e0", "Campos de Fumarolas": "#e04070",
              "Polos de Escarcha": "#f8f8f8"},
    "_pequeno": {"Depresiones": "#304a70", "Llanuras": "#5f8f4f", "Crestas": "#d0b060"},
    # sistema Kraken
    "Krax": {"Llanuras de Grafito": "#4a4a8a", "Escarpes Lobulados": "#8a6ad0",
             "Cuencas de Impacto": "#2a5a8a", "Crateres Jovenes": "#e0e0e0",
             "Fundicion de las Maquinas": "#d02020"},
    "Scarch": {"Mar Acido": "#6a8a2a", "Tierras Grises": "#a08070", "Mesetas Rojizas": "#d06040",
               "Campos de Lava": "#ff8800", "Neveros Organicos": "#f0d090",
               "Campos de Extraccion": "#d02020"},
    "Tenebris": {"Oceano Oscuro": "#203060", "Bosques Negros": "#305030",
                 "Tierras Altas de Basalto": "#707080", "Casquetes Polares": "#f0f0f0",
                 "Asentamiento Kerbal": "#40c0ff", "Restos de la Maquina": "#d02020"},
    "Salus": {"Oceano Salino": "#2080a0", "Fosas de Impacto": "#103050", "Arcos de Islas": "#c0a060",
              "Salinas": "#f0f0d0", "Hielo Salobre": "#ffffff"},
    "Ignea": {"Mar de Magma": "#ff6020", "Costra Enfriada": "#603020", "Grietas Incandescentes": "#ffd040"},
}


def hexrgb(h):
    h = h.lstrip("#")
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


# ------------------------------------------------------------------ ruido 3D
class Perlin:
    G = np.array([[1, 1, 0], [-1, 1, 0], [1, -1, 0], [-1, -1, 0], [1, 0, 1], [-1, 0, 1],
                  [1, 0, -1], [-1, 0, -1], [0, 1, 1], [0, -1, 1], [0, 1, -1], [0, -1, -1]],
                 np.float32)

    def __init__(self, seed):
        p = np.random.default_rng(seed).permutation(256).astype(np.int32)
        self.p = np.concatenate([p, p])

    def __call__(self, x, y, z):
        xi, yi, zi = (np.floor(v).astype(np.int32) for v in (x, y, z))
        xf, yf, zf = x - xi, y - yi, z - zi
        xi, yi, zi = xi & 255, yi & 255, zi & 255
        f = lambda t: t * t * t * (t * (t * 6 - 15) + 10)
        u, v, w = f(xf), f(yf), f(zf)
        p, G = self.p, self.G

        def g(ix, iy, iz, dx, dy, dz):
            gr = G[p[p[p[ix] + iy] + iz] % 12]
            return gr[..., 0] * dx + gr[..., 1] * dy + gr[..., 2] * dz

        L = lambda a, b, t: a + t * (b - a)
        x1 = L(g(xi, yi, zi, xf, yf, zf), g(xi + 1, yi, zi, xf - 1, yf, zf), u)
        x2 = L(g(xi, yi + 1, zi, xf, yf - 1, zf), g(xi + 1, yi + 1, zi, xf - 1, yf - 1, zf), u)
        x3 = L(g(xi, yi, zi + 1, xf, yf, zf - 1), g(xi + 1, yi, zi + 1, xf - 1, yf, zf - 1), u)
        x4 = L(g(xi, yi + 1, zi + 1, xf, yf - 1, zf - 1),
               g(xi + 1, yi + 1, zi + 1, xf - 1, yf - 1, zf - 1), u)
        return L(L(x1, x2, v), L(x3, x4, v), w)


def fbm(noise, P, scale=(1, 1, 1), octaves=6, persistence=0.5, lacunarity=2.0, ridged=False):
    x, y, z = P
    total = np.zeros_like(x)
    amp, freq, norm = 1.0, 1.0, 0.0
    for k in range(octaves):
        o = 17.31 * (k + 1)
        n = noise(x * scale[0] * freq + o, y * scale[1] * freq - o, z * scale[2] * freq + 0.5 * o)
        if ridged:
            n = 1.0 - np.abs(n) * 1.6
        total += amp * n
        norm += amp
        amp *= persistence
        freq *= lacunarity
    return total / norm


def grid(W, H):
    """Vectores unitarios (x, y, z; z = eje polar), latitud y longitud en grados."""
    lon = (np.arange(W, dtype=np.float32) + 0.5) / W * 2 * np.pi - np.pi
    lat = np.pi / 2 - (np.arange(H, dtype=np.float32) + 0.5) / H * np.pi
    LON, LAT = np.meshgrid(lon, lat)
    P = (np.cos(LAT) * np.cos(LON), np.cos(LAT) * np.sin(LON), np.sin(LAT))
    return P, np.degrees(LAT), np.degrees(LON)


def smooth(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def posterize(field, palette, fractions):
    """Asigna colores planos por cuantiles: fractions = fracción de píxeles de cada tono (de alto a bajo)."""
    cuts = np.quantile(field, 1 - np.cumsum(fractions)[:-1])
    idx = np.digitize(field, np.sort(cuts))[..., None]       # 0 = más bajo
    pal = np.array([hexrgb(c) for c in palette[::-1]])
    return pal[idx[..., 0]]


def normal_map(h, radius, strength):
    """Normales en espacio tangente (X = este, Y = norte). Se aplanan hacia los polos (72°–84°):
    en el polo la proyección equirectangular degenera y cualquier pendiente produce una cuña de luz."""
    Hh, W = h.shape
    lat_deg = 90 - (np.arange(Hh) + 0.5) / Hh * 180
    lat = np.radians(lat_deg)[:, None]
    dx = radius * np.maximum(np.cos(lat), 0.05) * 2 * np.pi / W
    dy = radius * np.pi / Hh
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) / (2 * dx)
    hp = np.pad(h, ((1, 1), (0, 0)), mode="edge")
    gy = (hp[:-2] - hp[2:]) / (2 * dy)                        # hacia el norte
    fade = smooth(84, 72, np.abs(lat_deg))[:, None]           # 1 lejos de los polos, 0 en el polo
    n = np.dstack([-gx * strength * fade, -gy * strength * fade, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return ((n * 0.5 + 0.5) * 255).astype(np.uint8)


def biome_image(index, names, table):
    cols = np.array([hexrgb(table[n]) for n in names], np.uint8)
    return Image.fromarray(cols[index], "RGB")


def save(img, body, kind):
    d = OUT / body
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{body}_{kind}.png"
    (img if isinstance(img, Image.Image) else Image.fromarray(np.asarray(img).astype(np.uint8))).save(path, optimize=True)
    print(f"  {path.relative_to(ROOT)}  {Image.open(path).size}")


def downsample(a, f):
    Hh, W = a.shape[:2]
    return a.reshape(Hh // f, f, W // f, f, *a.shape[2:]).mean(axis=(1, 3))


def encode_height(h, body):
    hm = HEIGHTMAPS[body]
    g = np.clip((h - hm["offset"]) / hm["deformity"], 0, 1)
    return Image.fromarray((g * 255 + 0.5).astype(np.uint8), "L")


# ------------------------------------------------------------------ Creus
def creus():
    W, H = 2048, 1024
    P, LAT, LON = grid(W, H)
    n = Perlin(11)
    warp = 9 * fbm(n, P, (2.2, 2.2, 2.2), 5)
    latw = LAT + warp
    band = 1 - np.abs(np.sin(np.radians(latw))) ** 1.25
    swirl = fbm(n, P, (1.6, 1.6, 7.0), 6)                 # estirado entre latitudes → manchas zonales
    field = band + 0.42 * swirl
    # Gran Tormenta Blanca: óvalo a 28° S
    d_storm = np.hypot((LON - 40) / 13, (LAT + 28) / 5.5)
    field = np.where(d_storm < 1, field.max() + 0.1, field)
    pal = ["#f6f9f9", "#eaefef", "#d7e0e0", "#cdd6d6"]       # muestreada (57/23/15/5 %)
    color = posterize(field, pal, [0.57, 0.23, 0.15, 0.05])
    color[(d_storm >= 0.55) & (d_storm < 1)] = hexrgb("#eaefef")
    color[(d_storm >= 1) & (d_storm < 1.25)] = hexrgb("#d7e0e0")
    save(color, "Creus", "Color")

    tone = posterize(field, ["#ffffff", "#aaaaaa", "#555555", "#000000"], [0.57, 0.23, 0.15, 0.05])[..., 0]
    save(normal_map(downsample(tone, 2) * 6.0, S.BODIES["Creus"]["radius"], 1.0), "Creus", "Normal")   # gigante gaseoso: casi liso

    names = list(BIOMES["Creus"])
    a = np.abs(latw)
    idx = np.where(a > 62, np.where(latw > 0, 0, 4), np.where(a > 22, np.where(latw > 0, 1, 3), 2))
    idx = np.where(d_storm < 1.25, 5, idx)
    save(biome_image(idx[::2, ::2], names, BIOMES["Creus"]), "Creus", "Biomes")

    # Anillo: tira horizontal (u = radio). Perfil casi simétrico: Kopernicus muestrea u=0 borde
    # exterior y u=1 borde interior; así la orientación no altera el aspecto.
    u = (np.arange(1024) + 0.5) / 1024
    alpha = 0.88 * smooth(0.0, 0.06, u) * smooth(1.0, 0.94, u)
    alpha *= 1 - 0.75 * np.exp(-((u - 0.47) / 0.018) ** 2)                 # división tipo Cassini
    alpha *= 0.9 + 0.1 * np.sin(u * 61) * np.sin(u * 23)                   # ondulaciones finas
    ring = np.zeros((8, 1024, 4), np.uint8)
    ring[..., :3] = hexrgb("#404040").astype(np.uint8)                     # gris oscuro de la imagen
    ring[..., 3] = (alpha * 255).astype(np.uint8)
    save(Image.fromarray(ring, "RGBA"), "Creus", "Ring")


# ------------------------------------------------------------------ Halum
def halum():
    W, H = 4096, 2048
    P, LAT, LON = grid(W, H)
    n = Perlin(23)
    cont = fbm(n, P, (1.8, 1.8, 1.8), 7)
    t = np.quantile(cont, 0.88)                                # 12 % de islas
    lo = cont.min()
    detail = fbm(n, P, (14, 14, 14), 4)
    h = np.where(cont > t,
                 950 * np.clip((cont - t) / (cont.max() - t), 0, 1) ** 0.7 + 60 * detail,
                 -40 - 2300 * np.clip((t - cont) / (t - lo), 0, 1) ** 0.55 + 120 * detail)
    trench = fbm(n, P, (2.6, 2.6, 2.6), 5, ridged=True)        # fosas del abismo supercrítico
    h -= np.where(cont < t - 0.04, 1300 * smooth(0.55, 0.9, trench), 0)
    h = np.clip(h, -3450, 980)
    save(encode_height(h, "Halum"), "Halum", "Height")

    h2 = downsample(h, 2)
    P2, LAT2, LON2 = grid(W // 2, H // 2)
    polar = np.abs(LAT2) >= 62
    surf = np.zeros(h2.shape + (3,), np.float32)
    deep, mid, shallow = hexrgb("#162444"), hexrgb("#2e4470"), hexrgb("#6f8fb5")
    land, snow = hexrgb("#dfe8f2"), hexrgb("#f7fbff")
    s1 = smooth(-2600, -900, h2)[..., None]
    s2 = smooth(-900, -40, h2)[..., None]
    surf = deep * (1 - s1) + mid * s1
    surf = surf * (1 - s2) + shallow * s2
    surf = np.where((h2 >= 0)[..., None], np.where(polar[..., None], snow, land), surf)
    save(surf, "Halum", "Surface")                             # color del terreno (PQS)

    # Nubes de hidrógeno: vetas zonales (ruido estirado en el eje polar)
    c = fbm(n, P2, (1.4, 1.4, 13.0), 6) + 0.35 * fbm(n, P2, (4, 4, 34), 4)
    t_white, t_mid = np.quantile(c, 0.76), np.quantile(c, 0.66)
    clouds = np.zeros(c.shape + (4,), np.uint8)
    clouds[..., :3] = hexrgb("#edf2f7").astype(np.uint8)
    clouds[..., 3] = np.where(c > t_white, 255, np.where(c > t_mid, 120, 0))
    save(Image.fromarray(clouds, "RGBA"), "Halum", "Clouds")    # capa para EVE (futuro)

    tint = fbm(n, P2, (2, 2, 5), 4)
    base = np.where((tint > np.quantile(tint, 0.82))[..., None], hexrgb("#9db9da"), hexrgb("#aac6e2"))
    base = np.where((h2 >= 0)[..., None], hexrgb("#b9d1ea"), base)   # islas apenas intuidas bajo 7 atm
    scaled = np.where((c > t_white)[..., None], hexrgb("#edf2f7"),
                      np.where((c > t_mid)[..., None], hexrgb("#cbdcee"), base))
    save(scaled, "Halum", "Color")                             # vista lejana (nubes horneadas)

    tone = np.where(c > t_white, 1.0, np.where(c > t_mid, 0.5, 0.0))
    save(normal_map(tone * 20.0, S.BODIES["Halum"]["radius"], 1.0), "Halum", "Normal")

    names = list(BIOMES["Halum"])
    idx = np.select([h2 < -2200, h2 < -250, h2 < 0, ~polar], [0, 1, 2, 3], 4)
    save(biome_image(idx[::2, ::2], names, BIOMES["Halum"]), "Halum", "Biomes")


# ------------------------------------------------------------------ Ocrea
def ocrea():
    """Luna de escarcha de hidrógeno: las capas se ordenan por densidad.

    Lecho de hielo de agua (0.93 g/cm3) violeta y abrupto; el neón sólido (1.44) se acumula
    como glaciares planos en las cuencas; el hidrógeno sólido (0.086) cubre el resto con mantos
    lisos que entierran los cráteres. Las fumarolas abren pozos con halos oscuros.
    """
    W, H = 4096, 2048
    P, LAT, LON = grid(W, H)
    X = np.dstack(P)
    n = Perlin(41)
    rng = np.random.default_rng(41)

    low = fbm(n, P, (1.4, 1.4, 1.4), 3)                        # relieve de gran escala
    bed = 2600 * low + 1100 * fbm(n, P, (9, 9, 9), 6, ridged=True)
    for _ in range(60):                                        # cráteres del lecho
        c = rng.normal(size=3)
        c /= np.linalg.norm(c)
        r = rng.uniform(0.02, 0.18) ** 1.3
        d = np.arccos(np.clip(X @ c, -1, 1)) / r
        depth = 900 * (r / 0.18) ** 0.5
        bed += np.where(d < 1, -depth * (1 - d ** 2), 0) + np.where((d >= 1) & (d < 1.4),
                                                                      0.25 * depth * (1 - (d - 1) / 0.4), 0)

    # Glaciares de neón: rellenan las cuencas más bajas (~16 %) con una superficie casi plana
    lvl = np.quantile(low, 0.16)
    w_gl = smooth(lvl + 0.03, lvl - 0.03, low)
    flow = fbm(n, P, (6, 6, 24), 3, ridged=True)
    h = bed * (1 - w_gl) + (2600 * lvl - 200 + 25 * flow) * w_gl

    # Mantos de hidrógeno: suavizan el terreno (+120 m de espesor) en ~45 % del resto y en los polos
    mant = fbm(n, P, (2.2, 2.2, 2.2), 5)
    mt = np.quantile(mant[w_gl < 0.5], 0.55)
    latn = np.abs(LAT) + 25 * fbm(n, P, (3, 3, 3), 4)         # borde polar irregular (±7°)
    w_m = np.maximum(smooth(mt - 0.03, mt + 0.03, mant), smooth(64, 72, latn)) * (1 - w_gl)
    h = h * (1 - w_m) + (2600 * low + 150) * w_m

    # Fumarolas: 7 respiraderos en el lecho desnudo, con pozos de 350 m
    vents = []
    while len(vents) < 7:
        c = rng.normal(size=3)
        c /= np.linalg.norm(c)
        i = int((0.5 - np.degrees(np.arcsin(c[2])) / 180) * H)
        j = int((np.arctan2(c[1], c[0]) / (2 * np.pi) + 0.5) * W) % W
        if w_m[i, j] < 0.1 and w_gl[i, j] < 0.1 and abs(LAT[i, j]) < 60:
            vents.append(c)
    for c in vents:
        d = np.arccos(np.clip(X @ c, -1, 1)) / 0.012
        h -= np.where(d < 1, 350 * (1 - d ** 2), 0)
    h = np.clip(h, -980, 2580)
    save(encode_height(h, "Ocrea"), "Ocrea", "Height")

    # ---- color (2048×1024) y biomas
    h2, wg2, wm2, flow2, latn2 = (downsample(a, 2) for a in (h, w_gl, w_m, flow, latn))
    P2, LAT2, LON2 = grid(W // 2, H // 2)
    X2 = np.dstack(P2)
    col = posterize(h2 + 150 * fbm(n, P2, (14, 14, 14), 3),
                    ["#6a6488", "#5e5878", "#4a4462"], [0.3, 0.45, 0.25])   # lecho violeta
    frost = np.where((wm2 < 0.65)[..., None], hexrgb("#cfcbe0"), hexrgb("#e9e6f2"))
    col = np.where((wm2 > 0.35)[..., None], frost, col)
    ice = np.where((flow2 > np.quantile(flow2, 0.8))[..., None], hexrgb("#a6d3dc"), hexrgb("#bfe3ea"))
    col = np.where((wg2 > 0.5)[..., None], ice, col)
    polar = latn2 >= 70
    col = np.where((polar & (wg2 <= 0.5))[..., None], hexrgb("#f6f4fb"), col)
    halo = np.zeros(h2.shape, bool)
    rays = fbm(n, P2, (40, 40, 40), 2) > -0.05
    for c in vents:                                            # halos oscuros con vetas radiales
        ang = np.arccos(np.clip(X2 @ c, -1, 1))
        dark = (ang < 0.035) | ((ang < 0.058) & rays)
        col = np.where(dark[..., None], hexrgb("#2f2a44"), col)
        col = np.where((ang < 0.012)[..., None], hexrgb("#1f1b30"), col)
        halo |= ang < 0.058
    save(col, "Ocrea", "Color")
    save(normal_map(h2, S.BODIES["Ocrea"]["radius"], 6.0), "Ocrea", "Normal")

    names = list(BIOMES["Ocrea"])
    idx = np.select([polar, halo, wg2 > 0.5, wm2 > 0.5], [4, 3, 2, 1], 0)
    save(biome_image(idx[::2, ::2], names, BIOMES["Ocrea"]), "Ocrea", "Biomes")


# ------------------------------------------------------------------ cuerpos pequeños
SMALL = {
    "Pastora": dict(seed=51, pal=["#4a4a4e", "#3d3d40", "#2e2e30"], ice=None),
    "Prima":   dict(seed=52, pal=["#8a7563", "#6e5a4e", "#4d4038"], ice=None),
    "Secunda": dict(seed=53, pal=["#d8e0e6", "#b8c4cc", "#9aa8b2"], ice=None),
    "Heraldo": dict(seed=54, pal=["#3a3430", "#2a2624", "#1c1918"], ice="#c8d4dc"),
    "Vestigia": dict(seed=55, pal=["#807a74", "#6a6460", "#57524e"], ice=None),
    "Nox":      dict(seed=56, pal=["#141416", "#0e0e10", "#09090a"], ice=None),
    "Lumen":    dict(seed=57, pal=["#f6f4fa", "#e4e1ec", "#cdc8da"], ice=None),
    # Cinturón Oscuro: albedo 0.01–0.02, solo se distinguen por el matiz
    "Fuligo":   dict(seed=58, pal=["#1a1a1d", "#141416", "#0e0e10"], ice="#3a3a40"),
    "Caligo":   dict(seed=59, pal=["#19171a", "#121114", "#0c0b0d"], ice=None),
    "Atra":     dict(seed=60, pal=["#161618", "#101012", "#0a0a0b"], ice=None),
    "Azabache": dict(seed=61, pal=["#141418", "#0e0e12", "#0a0a0d"], ice=None),
    "Brea":     dict(seed=62, pal=["#1a1612", "#14110e", "#0e0c0a"], ice=None),
    "Tizne":    dict(seed=63, pal=["#171717", "#111111", "#0b0b0b"], ice=None),
    "Escoria":  dict(seed=64, pal=["#1c1714", "#15110f", "#0f0c0a"], ice=None),
    "Hollin":   dict(seed=65, pal=["#131313", "#0d0d0d", "#080808"], ice=None),
}


def small(body):
    cfg, hm = SMALL[body], HEIGHTMAPS[body]
    W, H = 1024, 512
    P, LAT, LON = grid(W, H)
    n = Perlin(cfg["seed"])
    rng = np.random.default_rng(cfg["seed"])
    span = hm["deformity"]
    h = 0.42 * span * fbm(n, P, (0.9, 0.9, 0.9), 3) + 0.08 * span * fbm(n, P, (6, 6, 6), 5)
    X = np.dstack(P)
    for _ in range(45):                                        # cráteres
        c = rng.normal(size=3)
        c /= np.linalg.norm(c)
        r = rng.uniform(0.05, 0.35) ** 1.5
        d = np.arccos(np.clip(X @ c, -1, 1)) / r
        depth = 0.18 * span * r ** 0.5
        h += np.where(d < 1, -depth * (1 - d ** 2), 0) + np.where((d >= 1) & (d < 1.4),
                                                                   0.25 * depth * (1 - (d - 1) / 0.4), 0)
    h = h - np.median(h) + hm["offset"] + 0.5 * span
    h = np.clip(h, hm["offset"] + 1, hm["offset"] + span - 1)
    save(encode_height(h, body), body, "Height")

    field = h + 0.05 * span * fbm(n, P, (12, 12, 12), 3)
    col = posterize(field, cfg["pal"], [0.3, 0.45, 0.25])
    if cfg["ice"]:
        ice = fbm(n, P, (4, 4, 4), 4) > 0.33
        col = np.where(ice[..., None], hexrgb(cfg["ice"]), col)
    save(col, body, "Color")
    save(normal_map(h, S.BODIES[body]["radius"], 1.5), body, "Normal")

    names = list(BIOMES["_pequeno"])
    q1, q2 = np.quantile(h, [0.3, 0.8])
    idx = np.select([h < q1, h < q2], [0, 1], 2)
    save(biome_image(idx, names, BIOMES["_pequeno"]), body, "Biomes")


# ================================================================== sistema Kraken
def unit(lat, lon):
    la, lo = np.radians(lat), np.radians(lon)
    return np.array([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)], np.float32)


def angdist(X, c):
    return np.arccos(np.clip(X @ c, -1, 1))


def random_unit(rng):
    c = rng.normal(size=3)
    return (c / np.linalg.norm(c)).astype(np.float32)


def crater(X, c, r, depth):
    d = angdist(X, c) / r
    return np.where(d < 1, -depth * (1 - d ** 2), 0) + np.where((d >= 1) & (d < 1.4),
                                                                 0.25 * depth * (1 - (d - 1) / 0.4), 0)


def tangent_uv(X, c, r):
    """Coordenadas locales (este, norte) alrededor de c, en unidades de r radianes."""
    east = np.cross([0, 0, 1], c)
    east /= np.linalg.norm(east)
    north = np.cross(c, east)
    return (X @ east) / r, (X @ north) / r


def pixel_of(c, W, H):
    lat, lon = np.degrees(np.arcsin(c[2])), np.degrees(np.arctan2(c[1], c[0]))
    return int((90 - lat) / 180 * H) % H, int((lon + 180) / 360 * W) % W


def krax():
    """Mundo de carbono tipo Mercurio: grafito, escarpes de contracción, cráteres y la Fundición."""
    W, H = 2048, 1024
    P, LAT, LON = grid(W, H)
    X = np.dstack(P)
    n, rng = Perlin(61), np.random.default_rng(61)
    h = 1300 * fbm(n, P, (1.3, 1.3, 1.3), 4) + 300 * fbm(n, P, (10, 10, 10), 4)
    sc = fbm(n, P, (2.0, 2.0, 2.0), 3)
    h += 650 * smooth(-0.015, 0.015, sc)                       # escarpes lobulados
    for _ in range(90):
        r = rng.uniform(0.01, 0.16)
        h += crater(X, random_unit(rng), r, 1100 * np.sqrt(r / 0.16))
    young = [(random_unit(rng), rng.uniform(0.02, 0.04)) for _ in range(4)]
    for c, r in young:
        h += crater(X, c, r, 700)
    # La Fundición: mina a cielo abierto en 6 terrazas + 4 zanjas radiales
    cf = unit(*SITES["Krax/Fundicion"])
    df = angdist(X, cf) / 0.12
    w = smooth(0.95, 1.2, df)
    terr = np.ceil(np.clip(1 - df, 0, 1) * 6) / 6
    h = h * w + (200 - 1500 * terr) * (1 - w)
    trench = np.zeros(h.shape, bool)
    u, v = tangent_uv(X, cf, 1.0)
    for k in range(4):
        ang = np.radians(45 + 90 * k)
        along = u * np.cos(ang) + v * np.sin(ang)
        across = -u * np.sin(ang) + v * np.cos(ang)
        trench |= (np.abs(across) < 0.004) & (along > 0) & (df > 1) & (df < 3.2)
    h -= 120 * trench
    h = np.clip(h, -1780, 1780)
    save(encode_height(h, "Krax"), "Krax", "Height")

    col = posterize(h + 250 * fbm(n, P, (16, 16, 16), 3),
                    ["#3a3a42", "#2b2b31", "#1f1f24", "#141417"], [0.15, 0.35, 0.35, 0.15])
    rays = fbm(n, P, (60, 60, 60), 2) > 0.05
    yc = np.zeros(h.shape, bool)
    for c, r in young:
        d = angdist(X, c) / r
        yc |= d < 1.6
        col = np.where(((d < 1.2) | ((d < 3.5) & rays))[..., None], hexrgb("#4a4a55"), col)
    pit = df < 1
    tcol = np.where((np.ceil((1 - np.clip(df, 0, 1)) * 6) % 2 == 0)[..., None], hexrgb("#4a2a26"), hexrgb("#3a201e"))
    col = np.where(pit[..., None], tcol, col)
    col = np.where(trench[..., None], hexrgb("#5a3a30"), col)
    save(col, "Krax", "Color")
    save(normal_map(h, S.BODIES["Krax"]["radius"], 5.0), "Krax", "Normal")

    names = list(BIOMES["Krax"])
    idx = np.select([(df < 1.3) | trench, yc, np.abs(sc) < 0.02, h < np.quantile(h, 0.2)], [4, 3, 1, 2], 0)
    save(biome_image(idx[::2, ::2], names, BIOMES["Krax"]), "Krax", "Biomes")


def scarch():
    """Sauna volcánica: 40 % de mar ácido, volcanes, nieve orgánica y campos de extracción."""
    W, H = 4096, 2048
    P, LAT, LON = grid(W, H)
    X = np.dstack(P)
    n, rng = Perlin(71), np.random.default_rng(71)
    cont = fbm(n, P, (1.6, 1.6, 1.6), 7)
    t = np.quantile(cont, 0.40)
    h = np.where(cont > t, 2600 * np.clip((cont - t) / (cont.max() - t), 0, 1) ** 0.8,
                 -3400 * np.clip((t - cont) / (t - cont.min()), 0, 1) ** 0.6) + 150 * fbm(n, P, (12, 12, 12), 4)
    volc, lava = [], np.zeros(h.shape, bool)
    flow = fbm(n, P, (25, 25, 25), 3)
    while len(volc) < 12:
        c = random_unit(rng)
        if cont[pixel_of(c, W, H)] > t + 0.03:
            volc.append(c)
    for c in volc:
        r = rng.uniform(0.04, 0.09)
        d = angdist(X, c) / r
        peak = 3000 * r / 0.09
        h += peak * np.clip(1 - d, 0, 1) ** 1.5 - np.where(d < 0.18, 0.35 * peak, 0)
        lava |= (d < 2.2) & (flow > 0.08 + 0.1 * d) & (h > 0)
    fields = np.zeros(h.shape, bool)
    pits = np.zeros(h.shape, bool)
    placed = 0
    while placed < 3:                                          # 3 campos de extracción en tierra firme
        c = random_unit(rng)
        if cont[pixel_of(c, W, H)] > t + 0.06 and all(float(c @ v) < np.cos(0.3) for v in volc):
            d = angdist(X, c) / 0.08
            u, v = tangent_uv(X, c, 0.08)
            cell = ((u * 6) % 1 < 0.72) & ((v * 6) % 1 < 0.72)
            fields |= d < 1
            pits |= (d < 1) & cell
            h = np.where(d < 1, np.where(cell, 350, 600), h)   # rejilla industrial nivelada
            placed += 1
    h = np.clip(h, -3980, 4980)
    save(encode_height(h, "Scarch"), "Scarch", "Height")

    h2 = downsample(h, 2)
    lava2, fields2, pits2 = (downsample(m.astype(np.float32), 2) > 0.5 for m in (lava, fields, pits))
    P2, LAT2, _ = grid(W // 2, H // 2)
    land = h2 >= 0
    surf = np.where(land[..., None],
                    posterize(h2 + 300 * fbm(n, P2, (10, 10, 10), 3), ["#8a6a62", "#76585a", "#62484a"], [0.3, 0.4, 0.3]),
                    posterize(h2, ["#3a3430", "#2e2a26"], [0.5, 0.5]))
    snow = land & ((h2 > 2200) | (np.abs(LAT2) + 20 * fbm(n, P2, (3, 3, 3), 4) > 62))
    surf = np.where(snow[..., None], np.where((fbm(n, P2, (8, 8, 8), 3) > 0)[..., None],
                                              hexrgb("#c9a46e"), hexrgb("#b8925e")), surf)
    cracks = lava2 & (fbm(n, P2, (60, 60, 60), 2) > 0.25)
    surf = np.where(lava2[..., None], np.where(cracks[..., None], hexrgb("#c8502a"), hexrgb("#3a2c2c")), surf)
    surf = np.where(fields2[..., None], np.where(pits2[..., None], hexrgb("#2e2a2c"), hexrgb("#4a4446")), surf)
    save(surf, "Scarch", "Surface")

    haze = fbm(n, P2, (1.5, 1.5, 7.0), 5)
    hazecol = posterize(haze, ["#9b7a70", "#8a6a62", "#76585a"], [0.3, 0.45, 0.25])
    save(0.65 * hazecol + 0.35 * surf, "Scarch", "Color")       # vista lejana: neblina rojiza
    tone = posterize(haze, ["#ffffff", "#808080", "#000000"], [0.3, 0.45, 0.25])[..., 0]
    save(normal_map(tone * 10.0, S.BODIES["Scarch"]["radius"], 1.0), "Scarch", "Normal")

    names = list(BIOMES["Scarch"])
    idx = np.select([~land, fields2, lava2, snow, h2 > 1500], [0, 5, 3, 4, 2], 1)
    save(biome_image(idx[::2, ::2], names, BIOMES["Scarch"]), "Scarch", "Biomes")


def tenebris():
    """Mundo oscuro: océanos negros, bosques negros, basalto, colonia kerbal y restos de una máquina."""
    W, H = 4096, 2048
    P, LAT, LON = grid(W, H)
    X = np.dstack(P)
    n = Perlin(81)
    cc, cw = unit(*SITES["Tenebris/Asentamiento"]), unit(*SITES["Tenebris/Restos"])
    dc, dw = angdist(X, cc), angdist(X, cw)
    cont = fbm(n, P, (1.7, 1.7, 1.7), 7) + 0.25 * np.exp(-(dc / 0.10) ** 2) + 0.25 * np.exp(-(dw / 0.10) ** 2)
    t = np.quantile(cont, 0.65)
    ridge = fbm(n, P, (4, 4, 4), 6, ridged=True)
    h = np.where(cont > t, 900 * np.clip((cont - t) / (cont.max() - t), 0, 1) ** 0.7
                 + 2200 * smooth(0.45, 0.8, ridge) * smooth(t, t + 0.12, cont),
                 -3600 * np.clip((t - cont) / (t - cont.min()), 0, 1) ** 0.55) + 80 * fbm(n, P, (14, 14, 14), 3)
    w = smooth(0.018, 0.03, dc)
    h = h * w + 320 * (1 - w)                                  # meseta plana del asentamiento
    h += crater(X, cw, 0.012, 150)                             # cráter de la máquina derribada
    h = np.clip(h, -3980, 3980)
    save(encode_height(h, "Tenebris"), "Tenebris", "Height")

    h2 = downsample(h, 2)
    P2, LAT2, _ = grid(W // 2, H // 2)
    X2 = np.dstack(P2)
    dc2, dw2 = angdist(X2, cc), angdist(X2, cw)
    land = h2 >= 0
    veg = posterize(h2 + 200 * fbm(n, P2, (12, 12, 12), 3), ["#20241d", "#191d17", "#121512"], [0.3, 0.4, 0.3])
    surf = np.where(land[..., None], veg, posterize(h2, ["#141c28", "#0c121c"], [0.5, 0.5]))
    high = land & (h2 > 1300)
    surf = np.where(high[..., None], np.where((h2 > 2300)[..., None], hexrgb("#3a3a42"), hexrgb("#2c2c32")), surf)
    surf = np.where((land & (h2 < 40))[..., None], hexrgb("#3a3632"), surf)
    polar = np.abs(LAT2) + 25 * fbm(n, P2, (3, 3, 3), 4) > 72     # borde polar irregular
    surf = np.where(polar[..., None], hexrgb("#c8ccd4"), surf)
    colony = dc2 < 0.03
    lights = colony & (dc2 < 0.012) & (fbm(n, P2, (400, 400, 400), 1) > 0.2)
    surf = np.where(colony[..., None], hexrgb("#5a5a60"), surf)
    surf = np.where(lights[..., None], hexrgb("#ffd890"), surf)
    wreck = dw2 < 0.025
    surf = np.where(wreck[..., None], np.where((dw2 < 0.012)[..., None], hexrgb("#2a1a18"), hexrgb("#5a3020")), surf)
    save(surf, "Tenebris", "Surface")

    cl = fbm(n, P2, (1.5, 1.5, 5.0), 6)
    t1, t2 = np.quantile(cl, 0.70), np.quantile(cl, 0.82)
    scaled = np.where((cl > t2)[..., None], hexrgb("#9a9ea8"), np.where((cl > t1)[..., None], hexrgb("#6e727c"), surf))
    save(scaled, "Tenebris", "Color")
    save(normal_map(h2, S.BODIES["Tenebris"]["radius"], 2.0), "Tenebris", "Normal")

    names = list(BIOMES["Tenebris"])
    idx = np.select([colony, wreck, polar, ~land, high], [4, 5, 3, 0, 2], 1)
    save(biome_image(idx[::2, ::2], names, BIOMES["Tenebris"]), "Tenebris", "Biomes")


def salus():
    """Océano hipersalino: solo emergen (3 %) los arcos de los bordes de 4 cuencas de impacto."""
    W, H = 4096, 2048
    P, LAT, LON = grid(W, H)
    X = np.dstack(P)
    n, rng = Perlin(91), np.random.default_rng(91)
    h = -3200 + 500 * fbm(n, P, (2, 2, 2), 6)
    arcs = 0.55 + 0.45 * fbm(n, P, (6, 6, 6), 3) / 0.5
    basin = np.zeros(h.shape, bool)
    for _ in range(4):
        c, r = random_unit(rng), rng.uniform(0.35, 0.6)
        d = angdist(X, c) / r
        h += np.where(d < 1, -900 * (1 - d ** 2), 0) + 3800 * np.exp(-((d - 1) / 0.06) ** 2) * arcs
        basin |= d < 0.85
    h -= np.quantile(h, 0.97)                                  # exactamente un 3 % de tierra
    h = np.clip(h, -2480, 1080)
    save(encode_height(h, "Salus"), "Salus", "Height")

    h2 = downsample(h, 2)
    basin2 = downsample(basin.astype(np.float32), 2) > 0.5
    P2, LAT2, _ = grid(W // 2, H // 2)
    land = h2 >= 0
    shallow = (h2 < 0) & (h2 > -150)
    slope = np.abs(np.gradient(h2, axis=0)) + np.abs(np.gradient(h2, axis=1))
    surf = posterize(h2, ["#1e4a5a", "#163a44", "#0f2a33"], [0.3, 0.4, 0.3])
    surf = np.where(shallow[..., None], hexrgb("#7aa8a8"), surf)
    isl = np.where((slope > np.quantile(slope[land], 0.7))[..., None], hexrgb("#4a4440"), hexrgb("#d8d0c0"))
    surf = np.where(land[..., None], isl, surf)
    save(surf, "Salus", "Surface")

    polar = np.abs(LAT2) + 25 * fbm(n, P2, (3, 3, 3), 4) > 70     # hielo salobre de borde irregular
    cl = fbm(n, P2, (1.6, 1.6, 5.0), 6)
    t1, t2 = np.quantile(cl, 0.75), np.quantile(cl, 0.85)
    scaled = np.where(polar[..., None], hexrgb("#dfe8ee"), surf)
    scaled = np.where((cl > t2)[..., None], hexrgb("#e6eef2"), np.where((cl > t1)[..., None], hexrgb("#a8c0c8"), scaled))
    save(scaled, "Salus", "Color")
    save(normal_map(h2, S.BODIES["Salus"]["radius"], 2.0), "Salus", "Normal")

    names = list(BIOMES["Salus"])
    deep = basin2 & (h2 < np.quantile(h2[basin2], 0.5))       # mitad más profunda de las cuencas
    idx = np.select([polar, land, shallow, deep], [4, 2, 3, 1], 0)
    save(biome_image(idx[::2, ::2], names, BIOMES["Salus"]), "Salus", "Biomes")


def ignea():
    """Protoplaneta con océano de magma: placas de costra separadas por grietas incandescentes."""
    W, H = 2048, 1024
    P, LAT, LON = grid(W, H)
    n = Perlin(101)
    crack = fbm(n, P, (5, 5, 5), 5, ridged=True)
    h = 900 * fbm(n, P, (1.5, 1.5, 1.5), 5) + 200 * fbm(n, P, (14, 14, 14), 3) - 600 * smooth(0.55, 0.85, crack)
    sea_t = np.quantile(h, 0.35)
    sea = h < sea_t
    h = np.where(sea, sea_t + 15 * fbm(n, P, (20, 20, 20), 2), h)
    h = np.clip(h, -490, 690)
    save(encode_height(h, "Ignea"), "Ignea", "Height")

    col = posterize(h, ["#4a2a20", "#3a221a", "#2a1a16"], [0.3, 0.4, 0.3])
    glow = (crack > 0.7) & ~sea
    col = np.where(glow[..., None], hexrgb("#f0b040"), col)
    skin = fbm(n, P, (8, 8, 30), 3) > 0.1
    col = np.where(sea[..., None], np.where(skin[..., None], hexrgb("#8a3018"), hexrgb("#e0602a")), col)
    save(col, "Ignea", "Color")
    save(normal_map(h, S.BODIES["Ignea"]["radius"], 3.0), "Ignea", "Normal")

    names = list(BIOMES["Ignea"])
    idx = np.select([sea, glow], [0, 2], 1)
    save(biome_image(idx[::2, ::2], names, BIOMES["Ignea"]), "Ignea", "Biomes")


def disk_strip(alpha, color):
    ring = np.zeros((8, 1024, 4), np.uint8)
    ring[..., :3] = hexrgb(color).astype(np.uint8)
    ring[..., 3] = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(ring, "RGBA")


def kraken():
    """Tres discos de Kraken (tiras: u = 0 borde exterior, u = 1 interior). Sin luz propia: deben verse en el mapa."""
    u = (np.arange(1024) + 0.5) / 1024
    x = 1 - u                                                  # 0 interior … 1 exterior
    edges = lambda a, b: smooth(0.0, a, x) * smooth(1.0, 1 - b, x)
    # Interior caliente (36 000–50 000 km): polvo anaranjado, fino y brillante
    a = 0.6 * edges(0.1, 0.15) * (0.75 + 0.25 * np.sin(x * 47) ** 2)
    save(disk_strip(a, "#e07a3a"), "Kraken", "DiskInner")
    # Protoplanetario (150 000–400 000 km): rosa malva, opaco, con cúmulos y dos huecos
    a = 0.85 * edges(0.05, 0.12) * (0.6 + 0.4 * np.abs(np.sin(x * 37) * np.sin(x * 11 + 1)))
    for g, wd in ((0.40, 0.02), (0.72, 0.012)):               # hueco de Ignea (250 000 km) y otro embrión
        a *= 1 - 0.9 * np.exp(-((x - g) / wd) ** 2)
    save(disk_strip(a, "#d09ab8"), "Kraken", "Disk")
    # Cinturón Oscuro (450 000–820 000 km): polvo casi negro, apenas visible
    a = 0.28 * edges(0.15, 0.2) * (0.7 + 0.3 * np.sin(x * 23) ** 2)
    save(disk_strip(a, "#20181c"), "Kraken", "DarkBelt")

    # Superficie de enana T para el shader de estrella (sunspotTex = bandas, noiseMap = turbulencia).
    # Las enanas T son gigantes gaseosos incandescentes: zonas claras y cinturones oscuros de nubes
    # de sulfuros y sales, con huecos por donde asoma el interior más caliente (variabilidad real).
    W, H = 2048, 1024
    P, LAT, LON = grid(W, H)
    n = Perlin(111)
    latw = LAT + 4.5 * fbm(n, P, (2.5, 2.5, 6.0), 5)                       # bordes de banda turbulentos
    belts = 0.5 + 0.5 * np.sin(np.radians(latw) * 14 + 0.6 * np.sin(np.radians(latw) * 5))
    belts = belts * smooth(88, 60, np.abs(LAT)) + 0.6 * (1 - smooth(88, 60, np.abs(LAT)))   # polos difusos
    swirl = fbm(n, P, (2.0, 2.0, 12.0), 6)
    band = np.clip(0.42 + 0.5 * belts + 0.35 * swirl, 0, 1)               # 1 = zona clara, 0 = cinturón
    rng = np.random.default_rng(111)
    X = np.dstack(P)
    for _ in range(9):                                                     # huecos en las nubes
        c = random_unit(rng)
        if abs(c[2]) < 0.85:
            u, v = tangent_uv(X, c, 1.0)
            d = np.hypot(u / 0.09, v / 0.035)                              # óvalos estirados en longitud
            band = np.where((d < 1) & (X @ c > 0), band * (0.35 + 0.65 * d ** 2), band)   # solo su hemisferio
    g = (band * 255).astype(np.uint8)
    save(Image.fromarray(np.dstack([g, g, g]), "RGB"), "Kraken", "Bands")
    P2, _, _ = grid(1024, 512)
    fine = fbm(n, P2, (6.0, 6.0, 40.0), 5)
    chans = [np.clip(0.5 + 1.6 * f, 0, 1) for f in (fine, fbm(n, P2, (9.0, 9.0, 55.0), 4), fbm(n, P2, (4.0, 4.0, 25.0), 4))]
    save(Image.fromarray((np.dstack(chans) * 255).astype(np.uint8), "RGB"), "Kraken", "Noise")


JOBS = {"Creus": creus, "Halum": halum, "Ocrea": ocrea,
        "Kraken": kraken, "Krax": krax, "Scarch": scarch, "Tenebris": tenebris, "Salus": salus, "Ignea": ignea,
        **{b: (lambda b=b: small(b)) for b in SMALL}}

if __name__ == "__main__":
    for body in sys.argv[1:] or JOBS:
        t0 = time.time()
        print(body)
        JOBS[body]()
        print(f"  ({time.time() - t0:.1f} s)")
