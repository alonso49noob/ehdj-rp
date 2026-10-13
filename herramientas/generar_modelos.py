"""Modelos procedurales de los scatters de Titanus (Parallax): formaciones de espuma mineral que flotan en el mar
de agua supercrítica. Escribe .mu propios (herramientas/mu.py) con tres niveles de detalle y la textura de roca.

Física: el agua supercrítica disuelve el manto; la sílice y las sales de magnesio precipitan como espuma llena de
hidrógeno, más ligera que el agua supercrítica, y crecen hacia arriba como los «jardines químicos»: tubos, agujas
de cristal, columnas por contracción (como las de basalto) y mesetas en terrazas, capa a capa. Con 21 g nada muy
alto se sostiene sin una raíz ancha: todo es achaparrado y macizo salvo las agujas y los tubos, que son huecos.

Modelos (origen = línea de flotación, Y arriba; Parallax los pone a nivel del mar con placementAltitude = 0):
  continente_a/b  meseta flotante de ~3 km en terrazas, con crestas de minerales, acantilados y muesca de oleaje
  montana         pico mineral de ~800 m con cárcavas y estratos, rodeado de órganos de columnas hexagonales
  agujas          racimo de cristales de sílice hexagonales, inclinados, con punta piramidal (hasta ~400 m)
  chimeneas       tubos huecos de precipitación química, con la boca acampanada (hasta ~260 m)
  balsa           balsa pequeña de espuma (~250 m), para rellenar entre las grandes
Cada uno en tres LOD: <nombre>0 (cerca), 1 y 2 (lejos). Salida: GameData/MundosLejanos/Modelos/Titanus/*.mu
y PluginData/Titanus/Titanus_Roca.png (textura biplanar: estratos, vetas y costras).

Uso:  python herramientas/generar_modelos.py
"""
import pathlib

import numpy as np
from PIL import Image

import mu
import sistema as S

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "GameData" / S.PACK / "Modelos" / "Titanus"
TEX = ROOT / "GameData" / S.PACK / "PluginData" / "Titanus" / "Titanus_Roca.png"
MODEL_PATH = f"{S.PACK}/Modelos/Titanus"            # ruta para los .cfg (sin .mu)
LOD_RES = (1.0, 0.5, 0.25)


# ------------------------------------------------------------------ ruido suave (ondas aleatorias, sin rejilla)
class Ruido:
    def __init__(self, seed, n=48):
        rng = np.random.default_rng(seed)
        d = rng.normal(size=(n, 3))
        self.dir = d / np.linalg.norm(d, axis=1, keepdims=True)
        self.phase = rng.uniform(0, 2 * np.pi, n)

    def __call__(self, p, freq, octaves=4, ridged=False):
        """p: (..., 3) en metros; freq en ciclos por metro. Devuelve ~[-1, 1]."""
        total, amp, norm = 0.0, 1.0, 0.0
        for k in range(octaves):
            f = freq * 2.0 ** k
            w = np.sin(np.tensordot(p, self.dir.T * f * 2 * np.pi, axes=1) + self.phase * (k + 1))
            o = w.mean(axis=-1) * np.sqrt(len(self.phase) / 2)
            if ridged:
                o = 1 - np.abs(o) * 1.4
            total = total + amp * o
            norm += amp
            amp *= 0.5
        return total / norm


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def terraces(h, step, sharp=0.8):
    """Escalones de estratos: llano casi todo el escalón y rampa corta al final."""
    q = h / step
    return step * (np.floor(q) + smoothstep(sharp, 1.0, q - np.floor(q)))


# ------------------------------------------------------------------ construcción de mallas
class Malla:
    def __init__(self):
        self.v, self.n, self.uv, self.tri = [], [], [], []
        self.count = 0

    def _orient(self, V, T, out):
        a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
        flip = np.sum(np.cross(b - a, c - a) * out, axis=1) < 0
        T = T.copy()
        T[flip] = T[flip][:, ::-1]
        return T

    def suave(self, V, T, out, uv):
        """Parte con normales suaves (compartidas). out: dirección «hacia fuera» por triángulo, para orientarlos."""
        T = self._orient(V, T, out)
        a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
        fn = np.cross(b - a, c - a)
        N = np.zeros_like(V)
        for k in range(3):
            np.add.at(N, T[:, k], fn)
        N /= np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)
        self._add(V, N, uv, T)

    def plana(self, V, T, out, uvscale=0.01):
        """Parte facetada: cada triángulo con sus propios vértices y su normal (cristales, columnas)."""
        T = self._orient(V, T, out)
        P = V[T].reshape(-1, 3)
        a, b, c = V[T[:, 0]], V[T[:, 1]], V[T[:, 2]]
        fn = np.cross(b - a, c - a)
        fn /= np.maximum(np.linalg.norm(fn, axis=1, keepdims=True), 1e-9)
        N = np.repeat(fn, 3, axis=0)
        horiz = np.abs(N[:, 1]) > 0.7                                   # proyección de UV según la cara
        uv = np.where(horiz[:, None], P[:, [0, 2]], np.stack([P[:, 0] + P[:, 2], P[:, 1]], 1)) * uvscale
        self._add(P, N, uv, np.arange(len(P)).reshape(-1, 3))

    def _add(self, V, N, uv, T):
        self.v.append(V)
        self.n.append(N)
        self.uv.append(uv)
        self.tri.append(T + self.count)
        self.count += len(V)

    def escribir(self, nombre):
        v, n, uv, tri = (np.concatenate(x) for x in (self.v, self.n, self.uv, self.tri))
        mu.write(OUT / f"{nombre}.mu", nombre, v, n, uv, tri)
        return len(v), len(tri)


def grid_tris(rows, cols, wrap=True):
    """Triángulos de una rejilla rows × cols (índice r * cols + c); envuelve en columnas si wrap."""
    r, c = np.meshgrid(np.arange(rows - 1), np.arange(cols if wrap else cols - 1), indexing="ij")
    a = r * cols + c
    b = r * cols + (c + 1) % cols
    d = (r + 1) * cols + c
    e = (r + 1) * cols + (c + 1) % cols
    return np.concatenate([np.stack([a, b, d], -1).reshape(-1, 3), np.stack([b, e, d], -1).reshape(-1, 3)])


def meseta(m, rz, R0, rough, top, base, res, seed, notch=True):
    """Bloque flotante de planta irregular: cima (top(x, z, rf) en m), acantilado con muesca de oleaje en la
    línea de flotación y fondo a `base` m (bajo el agua). rf = fracción del radio (0 centro, 1 borde)."""
    NA, NR = max(24, int(160 * res)), max(6, int(40 * res))
    th = np.linspace(0, 2 * np.pi, NA, endpoint=False)
    ring = np.stack([np.cos(th), np.zeros_like(th), np.sin(th)], 1)
    edge = R0 * (1 + rough * rz(ring * R0, 1 / (2.2 * R0), 4) + 0.35 * rough * rz(ring * R0 + 77, 4 / R0, 3))
    # cima: anillos concéntricos hasta el borde
    rf = (np.arange(1, NR + 1) / NR) ** 0.8
    X = rf[:, None] * edge[None, :] * np.cos(th)[None, :]
    Z = rf[:, None] * edge[None, :] * np.sin(th)[None, :]
    Y = top(X, Z, np.broadcast_to(rf[:, None], X.shape))
    cy = top(np.zeros(1), np.zeros(1), np.zeros(1))[0]
    V = np.concatenate([[[0, cy, 0]], np.stack([X, Y, Z], -1).reshape(-1, 3)])
    fan = np.stack([np.zeros(NA, int), 1 + (np.arange(NA) + 1) % NA, 1 + np.arange(NA)], 1)
    T = np.concatenate([fan, grid_tris(NR, NA) + 1])
    m.suave(V, T, np.array([0, 1.0, 0]), V[:, [0, 2]] * 0.01)
    # acantilado: del borde de la cima hacia abajo, con muesca de oleaje (el mar se come la espuma a ras de agua)
    rim = np.stack([X[-1], Y[-1], Z[-1]], -1)
    levels = [(1.0, None), (1.01, 12.0), (0.96 if notch else 1.0, 2.0), (0.95 if notch else 1.0, -6.0),
              (1.0, -25.0), (0.92, base * 0.6), (0.8, base)]
    rows = []
    for f, y in levels:
        p = rim.copy()
        p[:, [0, 2]] *= f
        if y is not None:
            p[:, 1] = np.minimum(y, rim[:, 1] - 1) if y > 0 else y
        if y is not None:                                                # roca rota, no un cilindro (el borde
            p[:, [0, 2]] += 6 * rz(p + 300, 1 / 90, 2)[:, None] * ring[:, [0, 2]]   # de la cima no se mueve)
        rows.append(p)
    W = np.concatenate(rows)
    uvw = np.stack([np.tile(th * R0 / 100, len(rows)), W[:, 1] / 100], 1)
    Tw = grid_tris(len(rows), NA)
    outw = np.repeat(ring, 1, axis=0)[Tw[:, 0] % NA]
    m.suave(W, Tw, outw, uvw)
    # fondo (no se ve, cierra la malla para las colisiones)
    B = np.concatenate([[[0, base - 20, 0]], rows[-1]])
    Tb = np.stack([np.zeros(NA, int), 1 + np.arange(NA), 1 + (np.arange(NA) + 1) % NA], 1)
    m.suave(B, Tb, np.array([0, -1.0, 0]), B[:, [0, 2]] * 0.01)
    return edge


def prisma(m, x, z, y0, y1, r, rot, tilt=(0.0, 0.0), tip=0.0, lean=(0.0, 0.0), sides=6):
    """Columna/cristal facetado: prisma de `sides` caras de y0 a y1, cima inclinada (tilt = pendiente en x, z) o
    punta piramidal de altura `tip`; lean desplaza la cima (cristales inclinados)."""
    a = rot + np.arange(sides) * 2 * np.pi / sides
    bot = np.stack([x + r * np.cos(a), np.full(sides, y0), z + r * np.sin(a)], 1)
    top = bot.copy()
    top[:, 0] += lean[0]
    top[:, 2] += lean[1]
    top[:, 1] = y1 + tilt[0] * (top[:, 0] - x) + tilt[1] * (top[:, 2] - z)
    V = np.concatenate([bot, top])
    i = np.arange(sides)
    j = (i + 1) % sides
    T = np.concatenate([np.stack([i, j, i + sides], 1), np.stack([j, j + sides, i + sides], 1)])
    cen = np.array([x + lean[0] / 2, (y0 + y1) / 2, z + lean[1] / 2])
    out = V[T].mean(1) - cen
    out[:, 1] = 0
    m.plana(V, T, out)
    apex = np.array([[x + lean[0], y1 + tip, z + lean[1]]]) if tip > 0 else top.mean(0, keepdims=True)
    Vt = np.concatenate([top, apex])
    Tt = np.stack([i, j, np.full(sides, sides)], 1)
    outt = Vt[Tt].mean(1) - (top.mean(0) - [0, max(tip, 1.0), 0])
    m.plana(Vt, Tt, outt)


def tubo(m, x, z, y0, h, r, wall, lean, rz, res, flare=1.6):
    """Chimenea de precipitación: tubo hueco (pared exterior e interior) con la boca acampanada."""
    NA, NH = max(7, int(14 * res)), max(4, int(10 * res))
    th = np.linspace(0, 2 * np.pi, NA, endpoint=False)
    t = np.linspace(0, 1, NH)
    cx = x + lean[0] * t ** 1.5
    cz = z + lean[1] * t ** 1.5
    rad = r * (1 + (flare - 1) * smoothstep(0.75, 1.0, t)) * (1 + 0.12 * rz(np.stack([cx, y0 + h * t, cz], 1), 1 / 60, 2))
    walls = []
    for rr in (rad, np.maximum(rad - wall, 0.3 * rad)):
        P = np.stack([cx[:, None] + rr[:, None] * np.cos(th), np.broadcast_to((y0 + h * t)[:, None], (NH, NA)),
                      cz[:, None] + rr[:, None] * np.sin(th)], -1).reshape(-1, 3)
        walls.append(P)
    T = grid_tris(NH, NA)
    for k, P in enumerate(walls):
        c = np.stack([np.repeat(cx, NA), P[:, 1], np.repeat(cz, NA)], 1)
        out = (P - c)[T[:, 0]] * (1 if k == 0 else -1)
        uv = np.stack([np.tile(th, NH) * r / 50, P[:, 1] / 100], 1)
        m.suave(P, T, out, uv)
    lip = np.concatenate([walls[0][-NA:], walls[1][-NA:]])         # labio: anillo entre las dos paredes
    m.suave(lip, grid_tris(2, NA), np.array([0, 1.0, 0]), lip[:, [0, 2]] * 0.01)


# ------------------------------------------------------------------ las formaciones
def continente(res, seed):
    rz = Ruido(seed)
    m = Malla()
    R0 = 1500.0

    rng = np.random.default_rng(seed)
    buttes = [(rng.uniform(0, 2 * np.pi), rng.uniform(0.15, 0.7) * R0, rng.uniform(110, 330), rng.uniform(90, 260))
              for _ in range(7)]                                            # (ángulo, distancia, radio, altura)

    def top(x, z, rf):
        p = np.stack([x, np.zeros_like(x), z], -1)
        h = 60 + 380 * (1 - rf ** 2.0) * (0.55 + 0.45 * rz(p, 1 / 1400, 3))   # domo ancho
        for a, d, r, hb in buttes:                                          # mesetas testigo de paredes verticales
            dist = np.hypot(x - d * np.cos(a), z - d * np.sin(a)) * (1 + 0.25 * rz(p + a * 100, 1 / 250, 2))
            h = h + hb * smoothstep(r, 0.8 * r, dist)
        h = terraces(h, 45.0, 0.75) + 6 * rz(p + 500, 1 / 120, 3)           # estratos y rugosidad
        crest = np.maximum(rz(p + 900, 1 / 600, 3, ridged=True) - 0.45, 0)  # crestas de minerales cristalizados
        return h + 420 * crest ** 1.4 * (1 - rf) + 18 * (rf > 0.97)         # el borde se levanta un poco (labio)
    meseta(m, rz, R0, 0.28, top, -320.0, res, seed)                         # agujas sueltas sobre la meseta
    for _ in range(int(14 * res) + 3):
        a, d = rng.uniform(0, 2 * np.pi), rng.uniform(0.1, 0.75) * R0
        x, z = d * np.cos(a), d * np.sin(a)
        y0 = top(np.array([x]), np.array([z]), np.array([d / R0]))[0] - 10
        prisma(m, x, z, y0, y0 + rng.uniform(40, 140), rng.uniform(6, 14), rng.uniform(0, 1), tip=rng.uniform(15, 45),
               lean=tuple(rng.normal(0, 12, 2)))
    return m


def montana(res, seed):
    rz = Ruido(seed)
    m = Malla()
    R0 = 700.0

    def top(x, z, rf):
        p = np.stack([x, np.zeros_like(x), z], -1)
        th = np.arctan2(z, x)
        gully = 0.75 + 0.25 * np.cos(9 * th + 2.5 * rz(p, 1 / 500, 2))       # cárcavas radiales
        h = 820 * (1 - rf) ** 1.5 * gully * (0.85 + 0.15 * rz(p + 50, 1 / 300, 3))
        return terraces(h + 30, 22.0, 0.7) + 5 * rz(p + 200, 1 / 60, 2)
    meseta(m, rz, R0, 0.18, top, -380.0, res, seed)
    rng = np.random.default_rng(seed + 1)                                   # órganos de columnas en las faldas
    for _ in range(int(60 * res) + 8):
        a = rng.uniform(0, 2 * np.pi)
        d = R0 * rng.uniform(0.75, 1.15)
        x, z = d * np.cos(a), d * np.sin(a)
        h = rng.uniform(90, 320) * (1.15 - 0.4 * d / R0)
        prisma(m, x, z, -120.0, h, rng.uniform(18, 40), rng.uniform(0, 1),
               tilt=tuple(rng.normal(0, 0.12, 2)))
    return m


def agujas(res, seed):
    rz = Ruido(seed)
    m = Malla()
    meseta(m, rz, 140.0, 0.25, lambda x, z, rf: 25 * (1 - rf ** 2) + 4, -90.0, res * 0.35, seed, notch=False)
    rng = np.random.default_rng(seed)
    for _ in range(int(16 * res) + 5):
        a, d = rng.uniform(0, 2 * np.pi), rng.uniform(0, 100)
        h = rng.uniform(80, 380)
        r = h * rng.uniform(0.05, 0.09)
        prisma(m, d * np.cos(a), d * np.sin(a), -20.0, h, r, rng.uniform(0, 1), tip=r * rng.uniform(2.5, 4.0),
               lean=tuple(rng.normal(0, 0.18, 2) * h))
    return m


def chimeneas(res, seed):
    rz = Ruido(seed)
    m = Malla()
    meseta(m, rz, 170.0, 0.3, lambda x, z, rf: 18 * (1 - rf ** 2) + 3, -80.0, res * 0.35, seed, notch=False)
    rng = np.random.default_rng(seed)
    for _ in range(int(14 * res) + 4):
        a, d = rng.uniform(0, 2 * np.pi), rng.uniform(0, 120)
        h = rng.uniform(60, 260)
        r = rng.uniform(8, 26)
        tubo(m, d * np.cos(a), d * np.sin(a), -10.0, h, r, r * 0.35, tuple(rng.normal(0, 0.12, 2) * h), rz, res)
    return m


def balsa(res, seed):
    rz = Ruido(seed)
    m = Malla()

    def top(x, z, rf):
        p = np.stack([x, np.zeros_like(x), z], -1)
        return 6 + 16 * (1 - rf ** 2) * (0.6 + 0.4 * rz(p, 1 / 80, 3)) + 3 * rz(p + 9, 1 / 15, 2)
    meseta(m, rz, 125.0, 0.3, top, -45.0, res * 0.5, seed)
    return m


MODELOS = {"continente_a": (continente, 9101), "continente_b": (continente, 9177), "montana": (montana, 9202),
           "agujas": (agujas, 9303), "chimeneas": (chimeneas, 9404), "balsa": (balsa, 9505)}


# ------------------------------------------------------------------ textura biplanar de roca mineral
def textura(N=1024):
    """Estratos de espuma mineral (repetible): capas de colores alternos con ondulaciones, vetas claras de sales y
    costras oscuras de sulfuros. Casi neutra: el tinte de cada scatter (_Color) da el color final."""
    y, x = (np.mgrid[0:N, 0:N] + 0.5) / N
    rng = np.random.default_rng(77)

    def per(fx, fy, ph):                                               # ondas periódicas en la tesela
        return np.sin(2 * np.pi * (fx * x + fy * y) + ph)
    warp = sum(per(rng.integers(1, 4), rng.integers(1, 4), rng.uniform(0, 6)) / k for k in (2, 3, 4)) * 0.04
    layer = (y + warp) * 23
    band = np.floor(layer)
    tone = np.array([rng.uniform(0.55, 1.0) for _ in range(24)])[band.astype(int) % 24]
    grain = sum(per(rng.integers(-40, 41), rng.integers(-40, 41), rng.uniform(0, 6)) for _ in range(30)) / 30
    veins = np.abs(sum(per(rng.integers(-6, 7), rng.integers(-6, 7), rng.uniform(0, 6)) for _ in range(6)) / 6)
    lum = np.clip(tone * (0.85 + 0.25 * grain) + 0.45 * (veins < 0.03) - 0.25 * (np.abs(layer - band - 0.5) > 0.46), 0, 1)
    rgb = np.stack([lum * 0.95 + 0.05, lum * 0.88 + 0.04, lum * 0.80 + 0.03], -1)
    TEX.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray((rgb * 255).astype(np.uint8), "RGB").save(TEX, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for nombre, (fn, seed) in MODELOS.items():
        stats = []
        for lod, res in enumerate(LOD_RES):
            nv, nt = fn(res, seed).escribir(f"{nombre}{lod}")
            d = mu.read(OUT / f"{nombre}{lod}.mu")                     # comprobación de ida y vuelta
            assert len(d["v"]) == nv and len(d["tri"]) == nt
            stats.append(f"{nt}")
        v = mu.read(OUT / f"{nombre}0.mu")["v"]
        size = v.max(0) - v.min(0)
        print(f"  {nombre:13s} {size[0]:5.0f} × {size[2]:5.0f} m, de {v[:, 1].min():5.0f} a {v[:, 1].max():4.0f} m; "
              f"triángulos por LOD: {' / '.join(stats)}")
    textura()
    print(f"{OUT.relative_to(ROOT)}: {len(MODELOS) * len(LOD_RES)} modelos; {TEX.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
