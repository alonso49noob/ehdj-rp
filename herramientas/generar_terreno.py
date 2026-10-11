"""Texturas de detalle del terreno de respaldo, para cuando CTTP no está instalado.

Los .cfg usan las texturas de detalle de CTTP (Community Terrain Texture Pack). Si falta CTTP,
Kopernicus avisa de "Missing Textures" y el terreno de cerca queda roto. Este script genera:
  PluginData/Terreno/<material>.png         color en gris, repetible sin costuras (512×512)
  PluginData/Terreno/<material>_normal.png  normales DXT5nm (X en alfa, Y en verde, rojo = 255)
  Configs/Respaldo_CTTP.cfg                 parche :NEEDS[!CTTP] que cambia cada ruta de CTTP por la propia

Con CTTP instalado, el parche no se aplica y se usan las texturas de CTTP, que son mejores.
Uso:  python herramientas/generar_terreno.py
"""
import pathlib
import re

import numpy as np
from PIL import Image

import sistema as S
from generar_texturas import swizzle_dxt5nm

ROOT = pathlib.Path(__file__).resolve().parents[1]
GD = ROOT / "GameData"
CFG_DIR = GD / S.PACK / "Configs"
OUT_TEX = GD / S.PACK / "PluginData" / "Terreno"
PATCH = CFG_DIR / "Respaldo_CTTP.cfg"
CTTP = re.compile(r"^(\s*)(\w+)\s*=\s*CTTP/Textures/PluginData/(\w+)\.dds\s*$")
N = 512


# ------------------------------------------------------------------ ruido periódico (sin costuras al repetir)
def noise(seed, beta, stretch=(1.0, 1.0)):
    """Ruido 1/f^beta por FFT: periódico por construcción. Media 0, desviación 1."""
    rng = np.random.default_rng(seed)
    f = np.fft.fft2(rng.normal(size=(N, N)))
    fy, fx = np.meshgrid(np.fft.fftfreq(N) * stretch[0], np.fft.fftfreq(N) * stretch[1], indexing="ij")
    k = np.hypot(fx, fy)
    k[k * N < 3] = np.inf                                      # sin manchas de más de 1/3 de tesela: no se nota la repetición
    out = np.real(np.fft.ifft2(f / k ** beta))
    return (out - out.mean()) / out.std()


def voronoi(seed, count):
    """Distancias F1 y F2 al punto más cercano, con vecinos periódicos. Devuelve (F1, F2, índice de celda)."""
    rng = np.random.default_rng(seed)
    pts = rng.random((count, 2))
    y, x = (np.mgrid[0:N, 0:N] + 0.5) / N
    f1, f2, idx = np.full((N, N), 9.0), np.full((N, N), 9.0), np.zeros((N, N), int)
    for i, (py, px) in enumerate(pts):
        dy = np.abs(y - py)
        dx = np.abs(x - px)
        d = np.hypot(np.minimum(dy, 1 - dy), np.minimum(dx, 1 - dx))
        closer = d < f1
        f2 = np.where(closer, f1, np.minimum(f2, d))
        idx = np.where(closer, i, idx)
        f1 = np.where(closer, d, f1)
    return f1 * np.sqrt(count), f2 * np.sqrt(count), idx


def norm(a):
    return (a - a.mean()) / a.std()


# ------------------------------------------------------------------ materiales (media y contraste parecidos a CTTP)
def rock():
    f1, f2, _ = voronoi(11, 40)
    h = noise(1, 1.7) + 0.35 * noise(2, 1.1) - 0.8 * np.exp(-((f2 - f1) / 0.08) ** 2)
    return h, h, 110, 30, 3.0, 30


def cliff():
    strata = np.sin(np.linspace(0, 2 * np.pi * 14, N, endpoint=False))[:, None] + 0.6 * noise(3, 1.5, (1.0, 0.25))
    h = 0.7 * noise(4, 1.6) + 0.5 * strata + 0.3 * noise(5, 1.0)
    return h, h, 40, 14, 4.0, 15


def cracked():
    f1, f2, _ = voronoi(12, 28)
    crack = np.exp(-((f2 - f1) / 0.05) ** 2)
    h = 0.6 * noise(6, 1.6) + 0.2 * noise(7, 0.9) - 1.6 * crack
    return h, h, 142, 15, 2.5, 15


def gravel():
    f1, _, idx = voronoi(13, 900)
    tone = np.random.default_rng(13).normal(size=900)[idx]
    h = np.clip(1 - f1 / 0.75, 0, 1) ** 0.5 + 0.15 * noise(8, 0.8)
    return h, 0.6 * tone + 0.8 * h, 97, 19, 3.0, 15


def sand():
    y = np.arange(N)[:, None] / N
    ripples = np.sin(2 * np.pi * (24 * y + 1.5 * noise(9, 2.0) / 3))
    h = 0.5 * ripples + 0.4 * noise(10, 1.2) + 0.3 * noise(14, 0.6)
    return h, h, 153, 23, 1.5, 24


def beach():
    h = 0.6 * noise(15, 1.8) + 0.4 * noise(16, 0.7)
    return h, h, 145, 14, 1.0, 15


def ice():
    f1, f2, _ = voronoi(17, 12)
    h = noise(18, 2.2) - 0.25 * np.exp(-((f2 - f1) / 0.03) ** 2)
    return h, h, 173, 10, 1.0, 143


def snow():
    h = 0.7 * noise(19, 2.0) + 0.3 * noise(20, 0.9)
    return h, h, 223, 7, 0.7, 113


MATERIALS = {"rock": rock, "cliff": cliff, "cracked": cracked, "gravel": gravel,
             "sand": sand, "beach": beach, "ice": ice, "snow": snow}


def normals(h, strength):
    """Normales de una altura periódica (diferencias centradas con vuelta), en DXT5nm."""
    dx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * strength / 8
    dy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * strength / 8
    n = np.dstack([-dx, dy, np.ones_like(h)])
    n /= np.linalg.norm(n, axis=2, keepdims=True)
    return swizzle_dxt5nm(((n * 0.5 + 0.5) * 255).astype(np.uint8))


def make_textures():
    OUT_TEX.mkdir(parents=True, exist_ok=True)
    for name, fn in MATERIALS.items():
        h, tone, mean, std, strength, alpha = fn()
        g = np.clip(mean + std * norm(tone), 0, 255).astype(np.uint8)
        col = np.dstack([g, g, g, np.full_like(g, alpha)])
        Image.fromarray(col, "RGBA").save(OUT_TEX / f"{name}.png", optimize=True)
        Image.fromarray(normals(norm(h), strength), "RGBA").save(OUT_TEX / f"{name}_normal.png", optimize=True)


# ------------------------------------------------------------------ parche
def cttp_uses():
    """{(archivo, cuerpo, ruta de nodos): [(clave, material)]} de cada valor que apunta a CTTP."""
    uses = {}
    for p in sorted(CFG_DIR.rglob("*.cfg")):
        if p == PATCH:
            continue
        stack, body, pending = [], None, None
        for line in p.read_text(encoding="utf-8").splitlines():
            s = line.split("//")[0].strip()
            if s == "{":
                stack.append(pending)
                continue
            if s == "}":
                stack.pop()
                continue
            if re.fullmatch(r"[@\w:\[\]!,]+", s or "-"):
                pending = s
                continue
            if stack[-1:] == ["Body"] and s.startswith("name"):
                body = s.split("=", 1)[1].strip()
            m = CTTP.match(line)
            if m:
                path = tuple(stack[stack.index("Body") + 1:])
                uses.setdefault((p.relative_to(CFG_DIR).as_posix(), body, path), []).append((m.group(2), m.group(3)))
    return uses


def make_patch(uses):
    out = ["// GENERADO por herramientas/generar_terreno.py — no editar a mano.",
           "// Sin CTTP instalado, el terreno de cerca usa texturas de detalle propias (PluginData/Terreno)",
           "// en vez de quedar roto. Con CTTP, este parche no se aplica.",
           f"@Kopernicus:AFTER[{S.PACK}]:NEEDS[!CTTP]", "{"]
    for (_, body, path), keys in uses.items():
        out += [f"\t@Body[{body}]", "\t{"]
        for depth, node in enumerate(path, 2):
            out += ["\t" * depth + f"@{node}", "\t" * depth + "{"]
        ind = "\t" * (len(path) + 2)
        out += [f"{ind}@{k} = {S.TEX}/Terreno/{mat}.png" for k, mat in keys]
        for depth in range(len(path) + 1, 1, -1):
            out.append("\t" * depth + "}")
        out.append("\t}")
    out.append("}")
    PATCH.write_text("\n".join(out) + "\n", encoding="utf-8")


def main():
    uses = cttp_uses()
    mats = sorted({m.replace("_normal", "") for keys in uses.values() for _, m in keys})
    missing = set(mats) - set(MATERIALS)
    if missing:
        raise SystemExit(f"Faltan materiales de respaldo para: {', '.join(sorted(missing))}")
    make_textures()
    make_patch(uses)
    bodies = sorted({b for _, b, _ in uses})
    print(f"{OUT_TEX.relative_to(ROOT)}: {len(MATERIALS)} materiales (color + normales)")
    print(f"{PATCH.relative_to(ROOT)}: respaldo de {sum(len(k) for k in uses.values())} rutas de CTTP en {', '.join(bodies)}")


if __name__ == "__main__":
    main()
