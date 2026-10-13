"""Configs visuales opcionales: Scatterer, EVE (nubes 2D + volumétricas V5) y PlanetShine.

Genera también las texturas que EVE necesita a partir de las texturas del pack:
  <Cuerpo>_EVECoverage.png  cobertura en gris (canal R) para las nubes volumétricas
  <Cuerpo>_EVEClouds.png    capa 2D RGBA (color + alfa = cobertura)
  <Cuerpo>_ScaledEVE.png    vista lejana SIN nubes horneadas (se activa solo si EVE está instalado)

Salida: GameData/<pack>/Configs/Visuales/{Scatterer,EVE,PlanetShine}.cfg
Uso:  python herramientas/generar_visuales.py
"""
import pathlib

import numpy as np
from PIL import Image, ImageFilter

import sistema as S
from generar_texturas import GLOSS_SEA, HEIGHTMAPS, ICE_ALPHA, height_unit

ROOT = pathlib.Path(__file__).resolve().parents[1]
GD_TEX = ROOT / "GameData" / S.PACK / "PluginData"
OUT = ROOT / "GameData" / S.PACK / "Configs" / "Visuales"
KSP = pathlib.Path(r"C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program/GameData")
CAUSTICS = "StockScattererConfigs/Planets/Caustics2.png"
SVC = "StockVolumetricClouds/Clouds/Textures/PluginData"      # texturas de detalle/ruido de los volumétricos

# ------------------------------------------------------------------ Scatterer
# HR/HM: alturas de escala Rayleigh/Mie (km). betaR: color del cielo. mie: neblina. eclipses: lunas cercanas.
SCATTERER = {
    "Creus": dict(sun="Sun", flat=True, load=5e8, unload=1e9, start=0.997, HR=40, HM=6,
                  betaR=(0.0040, 0.0090, 0.0180), mie=0.0060, mieG=0.85, ozone=False, eclipse=["Ocrea", "Pastora"]),
    "Halum": dict(sun="Sun", flat=True, load=3e8, unload=5e8, start=1, HR=14, HM=3,
                  betaR=(0.0100, 0.0240, 0.0600), mie=0.0040, mieG=0.80, ozone=False, eclipse=[]),
    "Scarch": dict(sun="Kraken", flat=False, load=3e8, unload=5e8, start=1, HR=8, HM=6,
                   betaR=(0.0450, 0.0260, 0.0120), mie=0.0300, mieG=0.75, ozone=False, eclipse=[]),
    "Tenebris": dict(sun="Kraken", flat=True, load=3e8, unload=5e8, start=1, HR=35, HM=3,   # 0.2 atm de metano: tenue
                     betaR=(0.0012, 0.0018, 0.0026), mie=0.0010, mieG=0.80, ozone=False, eclipse=["Lumen"]),
    "Salus": dict(sun="Kraken", flat=True, load=3e8, unload=5e8, start=1, HR=5.5, HM=1.5,
                  betaR=(0.0250, 0.0450, 0.0750), mie=0.0200, mieG=0.85, ozone=False, eclipse=["Vestigia", "Nox"]),
    # Norh: 12 bar con neblina fotoquímica de amoníaco: cielo ocre, mucha dispersión de Mie
    "Norh": dict(sun="Sun", flat=True, load=3e8, unload=5e8, start=1, HR=11, HM=4,
                 betaR=(0.0300, 0.0220, 0.0100), mie=0.0300, mieG=0.78, ozone=False, eclipse=[]),
    # Skolta: "Titán cálido": cielo naranja oscuro con mucha bruma orgánica
    "Skolta": dict(sun="Sun", flat=True, load=3e8, unload=5e8, start=1, HR=10, HM=6,
                   betaR=(0.0280, 0.0180, 0.0080), mie=0.0400, mieG=0.75, ozone=False, eclipse=["Ceniza"]),
    # Termos: 5 atm de N2/CO2 con vapor: cielo azul pálido, casi blanco (mucha Mie del vapor). Atmósfera de 51 km.
    "Termos": dict(sun="Elara", flat=True, load=3e8, unload=5e8, start=1, HR=4.5, HM=1.5,
                   betaR=(0.0160, 0.0300, 0.0560), mie=0.0200, mieG=0.80, ozone=False, eclipse=["Tyrna"]),
    # Titanus: 218 atm de H2 con nubes de agua: cielo pardo anaranjado y muy brumoso. Con 21 g la atmósfera mide 53 km
    "Titanus": dict(sun="Elara", flat=True, load=8e8, unload=1.5e9, start=1, HR=6, HM=3,   # rojo herrumbre, opresivo
                    betaR=(0.0420, 0.0150, 0.0060), mie=0.0500, mieG=0.86, ozone=False, eclipse=[]),
    # Akira: 1.2 atm de N2 a 62 K con bruma de metano: cielo azul oscuro, como el de Plutón
    "Akira": dict(sun="Sun", flat=True, load=3e8, unload=5e8, start=1, HR=12, HM=4,
                  betaR=(0.0060, 0.0130, 0.0300), mie=0.0080, mieG=0.75, ozone=False, eclipse=[]),
}
OCEANS = {  # upwelling = color del agua profunda; underwater = niebla submarina
    "Halum": dict(wind=4, amp=0.6, up=(0.004, 0.008, 0.020), under=(0.35, 0.50, 0.72), clear=120, n=1.09,
                  caps=0.1, foam=0.6),     # neón líquido: transparente, n = 1.09, mar en calma
    "Scarch": dict(wind=10, amp=1.0, up=(0.012, 0.010, 0.004), under=(0.30, 0.28, 0.14), clear=15, n=1.34,
                   caps=0.4, foam=1.5),    # agua ácida con gas: turbia y espumosa
    "Tenebris": dict(wind=7, amp=1.0, up=(0.0010, 0.0012, 0.0018), under=(0.04, 0.055, 0.07), clear=40, n=1.33,
                     caps=0.2, foam=1.2),
    "Salus": dict(wind=9, amp=1.0, up=(0.0025, 0.0070, 0.0080), under=(0.12, 0.30, 0.30), clear=50, n=1.38,
                  caps=0.25, foam=1.6),    # salmuera: espuma de sal en las costas
    "Norh": dict(wind=6, amp=0.8, up=(0.004, 0.009, 0.010), under=(0.12, 0.24, 0.26), clear=30, n=1.36,
                 caps=0.3, foam=1.0),      # agua con un 25 % de amoníaco a −40 °C: espesa y verdosa
    "Skolta": dict(wind=5, amp=0.7, up=(0.004, 0.003, 0.002), under=(0.23, 0.19, 0.16), clear=60, n=1.35,
                   caps=0.15, foam=0.8),   # NH3 con hidracina: incoloro; casi negro en lo profundo, refleja el cielo
    "Termos": dict(wind=4, amp=0.6, up=(0.006, 0.020, 0.022), under=(0.20, 0.45, 0.45), clear=25, n=1.33,
                   caps=0.1, foam=1.2),    # agua a 140 °C con sílice: turquesa lechosa; espuma mineral en la orilla
}

# ------------------------------------------------------------------ EVE
# altura de la capa, rango de nubes volumétricas, color, fades de escala
EVE = {
    "Halum": dict(alt=20000, lo=20000, hi=26000, color=(230, 236, 245), fade=(230000, 280000), swap=True),
    "Salus": dict(alt=2000, lo=2000, hi=8000, color=(228, 228, 224), fade=(120000, 160000), swap=True),
    "Scarch": dict(alt=3000, lo=3000, hi=12000, color=(140, 110, 100), fade=(130000, 170000), swap=False,
                   cover=0.30),    # neblina en degradado (ya no bandas): se fija la cobertura media
    "Creus": dict(alt=60000, lo=60000, hi=78000, color=(240, 244, 246), fade=(450000, 550000), swap=False),
    "Norh": dict(alt=4000, lo=4000, hi=12000, color=(214, 178, 138), fade=(150000, 200000), swap=False,
                 cover=0.45),      # aire saturado de NH3: muchas nubes
    "Skolta": dict(alt=3000, lo=3000, hi=10000, color=(222, 206, 180), fade=(140000, 190000), swap=False,
                   cover=0.35),    # nubes de NH3 crema (menos que el 60 % inicial: tapaban el contraste mar/tierra)
    "Termos": dict(alt=2500, lo=2500, hi=7000, color=(238, 238, 234), fade=(70000, 100000), swap=True),   # vapor
    # Titanus: cubierta baja de nubes de agua, espesa y parda (la vista lejana sigue siendo la de bandas: swap=False)
    "Titanus": dict(alt=9000, lo=9000, hi=24000, color=(200, 158, 124), fade=(900000, 1200000), swap=False, dens=3.0),
}
# Capas volumétricas extra (mismo cuerpo, otra altura y otro mapa de cobertura): en Titanus, torres de tormenta
# de 26 a 44 km sobre los bordes de los cinturones, las tormentas y los brazos de El Ojo (Titanus_Tormentas.png).
# Dos capas separadas por un hueco dan la sensación de profundidad: se ve la cubierta baja entre las torres.
EVE_EXTRA = {
    "Titanus": dict(nombre="tormentas", src="Tormentas", alt=26000, lo=26000, hi=44000, color=(150, 100, 80),
                    fade=(900000, 1200000), dens=1.5),
}
OCEAN_SCALED = {"Halum": "#6b94cc", "Salus": "#24484a", "Termos": "#4f9aa6"}   # color del mar visto desde órbita

# ------------------------------------------------------------------ PlanetShine (albedo -> intensidad de luz reflejada)
ALBEDO = {"Creus": 0.70, "Halum": 0.55, "Ocrea": 0.85, "Pastora": 0.05, "Prima": 0.15, "Secunda": 0.60,
          "Heraldo": 0.04, "Krax": 0.03, "Scarch": 0.35, "Tenebris": 0.10, "Salus": 0.30, "Vestigia": 0.12,
          "Nox": 0.02, "Lumen": 0.35, "Ignea": 0.15, "Fuligo": 0.01, "Caligo": 0.015, "Atra": 0.012,
          "Azabache": 0.02, "Brea": 0.015, "Tizne": 0.012, "Escoria": 0.02, "Hollin": 0.01, "Norh": 0.40, "Skolta": 0.35, "Ceniza": 0.09,
          "Termos": 0.50, "Tyrna": 0.60, "Karmen": 0.15, "Talia": 0.12, "Akira": 0.65, "Titanus": 0.50}
THICK = {"Creus": 1.0, "Halum": 1.0, "Scarch": 1.0, "Tenebris": 0.15, "Salus": 0.6, "Norh": 1.0, "Skolta": 1.0,
         "Termos": 1.0, "Akira": 0.8, "Titanus": 1.0}
HAZE = {"Scarch": 0.65, "Norh": 0.70, "Skolta": 0.40}   # peso de la neblina horneada en _Color (generar_texturas)


def img(body, kind, mode="RGB"):
    return np.asarray(Image.open(GD_TEX / body / f"{body}_{kind}.png").convert(mode), np.float32)


def height(body, shape):
    hm = HEIGHTMAPS[body]
    g = Image.fromarray(height_unit(GD_TEX / body / f"{body}_Height.png"), "F").resize(shape[::-1], Image.BILINEAR)
    return hm["offset"] + np.asarray(g, np.float32) * hm["deformity"]


def coverage(body):
    """Cobertura de nubes 0..1 (2048×1024) reconstruida de las texturas del pack."""
    col = img(body, "Color")
    if body in ("Halum", "Termos", "Titanus"):   # capa de nubes propia de generar_texturas
        cov = img(body, "Clouds", "RGBA")[..., 3] / 255
    elif body == "Salus":
        surf = img(body, "Surface")
        diff = np.abs(col - surf).sum(axis=2)
        lum = col.mean(axis=2)
        cov = np.where(diff > 6, np.clip((lum - 60) / 150, 0.35, 1.0), 0.0)
        if body == "Salus":   # el hielo polar no es nube
            ice = img(body, "Color", "RGBA")[..., 3] == ICE_ALPHA   # alfa exacto del hielo (generar_texturas)
            cov = np.where(ice, 0.0, cov)
    elif body in HAZE:       # celdas de tormenta a partir de la neblina horneada
        haze = (col - (1 - HAZE[body]) * img(body, "Surface")) / HAZE[body]
        lum = haze.mean(axis=2)
        hi = np.quantile(lum, 0.95)
        ramp = lambda f: np.clip((lum - np.quantile(lum, f)) / (hi - np.quantile(lum, f)), 0, 1)
        cov = ramp(0.55)
        if "cover" in EVE[body]:            # fracción media de cielo cubierto (por área): umbral por bisección
            w = np.cos(np.radians(90 - (np.arange(lum.shape[0]) + 0.5) / lum.shape[0] * 180))[:, None]
            lo_f, hi_f = 0.0, 0.94
            for _ in range(30):
                mid = (lo_f + hi_f) / 2
                cov = ramp(mid)
                if (cov * w).sum() / (w * np.ones_like(cov)).sum() > EVE[body]["cover"]:
                    lo_f = mid
                else:
                    hi_f = mid
    else:                    # Creus: las nubes de metano son lo más brillante
        lum = col.mean(axis=2)
        cov = np.clip((lum - np.quantile(lum, 0.3)) / (lum.max() - np.quantile(lum, 0.3)), 0, 1)
    im = Image.fromarray((cov * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(2))
    return np.asarray(im, np.float32) / 255


def eve_textures(body, cfg):
    cov = coverage(body)
    Image.fromarray((cov * 255).astype(np.uint8), "L").save(GD_TEX / body / f"{body}_EVECoverage.png", optimize=True)
    rgba = np.zeros(cov.shape + (4,), np.uint8)
    rgba[..., :3] = cfg["color"]
    if body == "Creus" and (ROOT / "arte" / "Creus" / "nubes-artista.png").exists():   # nubes con el color del artista
        rgba[..., :3] = img(body, "Color").astype(np.uint8)
    rgba[..., 3] = (cov * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(GD_TEX / body / f"{body}_EVEClouds.png", optimize=True)
    if cfg["swap"]:          # vista lejana sin nubes: mar del color del océano, tierra = terreno real
        surf = img(body, "Surface")
        h = height(body, surf.shape[:2])
        sea = np.array([int(OCEAN_SCALED[body][i:i + 2], 16) for i in (1, 3, 5)], np.float32)
        out = np.where((h < 0)[..., None], sea, surf)
        gloss = np.where(h < 0, round(GLOSS_SEA * 255), 0)       # alfa = brillo especular, como en _Color
        if body == "Salus":  # conserva el hielo salobre polar
            col = img(body, "Color")
            ice = img(body, "Color", "RGBA")[..., 3] == ICE_ALPHA   # alfa exacto del hielo (generar_texturas)
            out = np.where(ice[..., None], col, out)
            gloss = np.where(ice, ICE_ALPHA, gloss)
        rgba = np.dstack([out, gloss]).astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(GD_TEX / body / f"{body}_ScaledEVE.png", optimize=True)


def eve_extra_textures(body, cfg):
    """Cobertura y capa 2D de una capa extra a partir de <Cuerpo>_<src>.png (alfa = cobertura)."""
    a = img(body, cfg["src"], "RGBA")[..., 3] / 255
    cov = np.asarray(Image.fromarray((a * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(2)), np.float32) / 255
    suf = cfg["src"]
    Image.fromarray((cov * 255).astype(np.uint8), "L").save(GD_TEX / body / f"{body}_EVECoverage{suf}.png", optimize=True)
    rgba = np.zeros(cov.shape + (4,), np.uint8)
    rgba[..., :3] = cfg["color"]
    rgba[..., 3] = (cov * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(GD_TEX / body / f"{body}_EVEClouds{suf}.png", optimize=True)


def eve_object(body, cfg, nombre="nubes", suf=""):
    tex = f"{S.TEX}/{body}/{body}"
    r, g, b = cfg["color"]
    dens = cfg.get("dens", 1.0)
    return f"""	OBJECT
	{{
		name = {body}-{nombre}
		body = {body}
		altitude = {cfg["alt"]}
		detailSpeed = 0,6,0
		settings
		{{
			_DetailTex = {SVC}/detail1
			_DetailScale = 30
			_UVNoiseTex = {SVC}/uvnoise1
			_UVNoiseStrength = 0.0002
			_Lambertian = 0.5
			_MainTex
			{{
				value = {tex}_EVEClouds{suf}
			}}
			_FlowMap
			{{
			}}
		}}
		layer2D
		{{
			shadowMaterial
			{{
			}}
			macroCloudMaterial
			{{
				_DetailDist = 2E-06
			}}
		}}
		layerRaymarchedVolumeV5
		{{
			color = {r}, {g}, {b}, 255
			upwardsCloudSpeed = 5
			scaledFadeStartAltitude = {cfg["fade"][0]}
			scaledFadeEndAltitude = {cfg["fade"][1]}
			skylightTintMultiplier = 0.7
			raymarchingSettings
			{{
				lightMarchDistance = 1900
				baseStepSize = 120
				maxStepSize = 1000
				adaptiveStepSizeFactor = 0.0044
			}}
			noise
			{{
				erosionDepth = 0.65
				worley
				{{
					persistence = 0.57
					spherical = 1
				}}
			}}
			coverageMap
			{{
				value = {tex}_EVECoverage{suf}
				type = AlphaMap
				alphaMask = ALPHAMAP_R
			}}
			cloudTypeMap
			{{
				value = {SVC}/Eve/PerlinPillars
				type = AlphaMap
				alphaMask = ALPHAMAP_R
			}}
			cloudTypes
			{{
				Item
				{{
					typeName = Capa
					minAltitude = {cfg["lo"]}
					maxAltitude = {cfg["hi"]}
					interpolateCloudHeights = true
					density = {0.0001 * dens:g}
					noiseEdgeHardness = 0.8
					baseNoiseTiling = 3000
					coverageCurve
					{{
						key = 0.00321579 0.01443481 -0.03297058 19.57472
						key = 0.1271144 1.0 0.01987062 0.01987062
						key = 0.6785794 -0.1662257 0.0343262 0.0343262
						key = 0.9048536 0.9638001 0.06266714 0.06266714
						key = 1.0052 -0.006964087 -14.69716 -14.69716
					}}
					densityCurve
					{{
					}}
				}}
				Item
				{{
					typeName = Torres
					minAltitude = {cfg["lo"]}
					maxAltitude = {int(cfg["lo"] + 0.7 * (cfg["hi"] - cfg["lo"]))}
					density = {0.02 * dens:g}
					noiseEdgeHardness = 0.9
					baseNoiseTiling = 3000
					coverageCurve
					{{
						key = 0.00321579 0.01443481 -0.03297058 19.57472
						key = 0.1271144 0.9584956 0.01987062 0.01987062
						key = 0.5853482 2.2663 0.0343262 0.0343262
						key = 0.9048536 1 0.06266714 0.06266714
						key = 1.0052 -0.006964087 -14.69716 -14.69716
					}}
					densityCurve
					{{
					}}
				}}
			}}
			lightVolumeSettings
			{{
			}}
			phaseFunctions
			{{
			}}
		}}
	}}
"""


def v3(t):
    return ",".join(f"{x:g}" for x in t)


# ------------------------------------------------------------------ destello de Elara (Scatterer, texturas propias)
DESTELLO = GD_TEX / "Elara" / "Destello"                     # construir.py los deja en PNG (DXT1 rompería los degradados)


def _png(name, rgb):
    """Guarda un destello aditivo: RGB lineal 0..1 (lo que pase de 1 se recorta), con tramado contra las bandas."""
    rng = np.random.default_rng(len(name))
    a = np.clip(rgb, 0, 1) ** (1 / 1.6) * 255 + rng.uniform(-0.5, 0.5, rgb.shape)
    DESTELLO.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGB").save(DESTELLO / f"{name}.png", optimize=True)


def _polar(N):
    y, x = (np.mgrid[0:N, 0:N] + 0.5) / N * 2 - 1
    return x, y, np.hypot(x, y), np.arctan2(y, x)


def _mezcla(c0, c1, t):
    t = np.clip(t, 0, 1)[..., None]
    return np.array(c0) * (1 - t) + np.array(c1) * t


def destello_texturas():
    """Núcleo, estallido, raya anamórfica, halo y tres fantasmas, con el color de una K4 V (4 600 K)."""
    rng = np.random.default_rng(4600)
    naranja, blanco = (1.0, 0.60, 0.28), (1.0, 0.97, 0.92)
    edge = lambda r: np.clip((1 - r) / 0.12, 0, 1) ** 2               # nada llega al borde de la textura
    # Núcleo: disco saturado, resplandor 1/r² y corona ciliar (las «pestañas» finas que deja la lente)
    x, y, r, th = _polar(1024)
    lash = 1 + 0.45 * sum(np.sin(th * k + rng.uniform(0, 6)) for k in rng.integers(150, 420, 7)) / 7 * (r > 0.03)
    inten = 3.0 * np.exp(-(r / 0.025) ** 2) + 0.9 / (1 + (r / 0.045) ** 2) ** 1.15 * lash + 0.18 * np.exp(-r / 0.3)
    _png("Elara_Nucleo", inten[..., None] * _mezcla(blanco, naranja, r / 0.18) * edge(r)[..., None])
    # Estallido: 6 picos de difracción (diafragma hexagonal) con bandas irisadas, 6 secundarios y rayos finos
    x, y, r, th = _polar(2048)
    acc = np.zeros(r.shape + (3,))
    for k in range(12):
        a = np.radians(15 + 30 * k)
        along, perp = x * np.cos(a) + y * np.sin(a), np.abs(-x * np.sin(a) + y * np.cos(a))
        main = k % 2 == 0
        w = (0.0022 if main else 0.0011) * (1 + 3 * np.clip(along, 0, 1))
        line = np.exp(-(perp / w) ** 2) * (along > 0) / (1 + (np.clip(along, 0, None) / (0.09 if main else 0.05)) ** 1.3)
        disp = np.stack([0.5 + 0.5 * np.cos(along * 70 + ph) for ph in (0, 2.1, 4.2)], -1)
        acc += (1.0 if main else 0.35) * line[..., None] * (0.7 * np.array(naranja) + 0.3 * disp)
    for _ in range(260):
        a, ln, w = rng.uniform(0, 2 * np.pi), rng.uniform(0.08, 0.7), rng.uniform(0.0005, 0.0016)
        along, perp = x * np.cos(a) + y * np.sin(a), np.abs(-x * np.sin(a) + y * np.cos(a))
        c = _mezcla(blanco, naranja, rng.uniform(0.2, 1.0) * np.ones(1))[0]
        acc += rng.uniform(0.04, 0.22) * (np.exp(-(perp / w) ** 2) * (along > 0) * np.exp(-along / ln))[..., None] * c
    _png("Elara_Rayos", acc * edge(r)[..., None])
    # Raya anamórfica: cálida en el centro, cian en los extremos (el toque extraño)
    core = np.exp(-(y / 0.0035) ** 2) * np.exp(-np.abs(x) / 0.33)
    soft = 0.35 * np.exp(-(y / 0.018) ** 2) * np.exp(-np.abs(x) / 0.18)
    _png("Elara_Raya", (core + soft)[..., None] * _mezcla((1.0, 0.82, 0.62), (0.45, 0.80, 1.0), np.abs(x) / 0.6)
         * np.clip((1 - np.abs(x)) / 0.1, 0, 1)[..., None])
    # Halo: anillo de 22° con dispersión (rojo fuera, azul dentro) y otro más tenue
    x, y, r, th = _polar(1024)
    ring = lambda r0, w, k: np.exp(-((r - r0 - k) / w) ** 2)
    acc = np.stack([ring(0.62, 0.035, 0.02), ring(0.62, 0.035, 0.0), ring(0.62, 0.035, -0.02)], -1) * 0.8
    acc += np.stack([ring(0.82, 0.05, 0.015), ring(0.82, 0.05, 0.0), ring(0.82, 0.05, -0.015)], -1) * 0.25
    _png("Elara_Halo", acc * (0.85 + 0.15 * np.cos(th * 6))[..., None] * edge(r)[..., None])
    # Fantasmas: hexágono (la forma del diafragma) con borde brillante y franja cromática; anillo irisado; disco ámbar
    x, y, r, th = _polar(256)
    hexr = r * np.cos(((th + np.pi / 6) % (np.pi / 3)) - np.pi / 6) / np.cos(np.pi / 6)   # «radio» hexagonal
    fill = lambda s: np.clip((s - hexr) / 0.04, 0, 1)
    rim = lambda s: np.exp(-((hexr - s) / 0.035) ** 2)
    acc = np.stack([0.30 * fill(0.80) + 0.9 * rim(0.80), 0.32 * fill(0.78) + 0.8 * rim(0.78),
                    0.40 * fill(0.76) + 1.0 * rim(0.76)], -1)
    _png("Elara_FantasmaHex", acc * np.array([0.55, 0.85, 1.0]))
    acc = np.stack([np.exp(-((r - r0) / 0.05) ** 2) for r0 in (0.74, 0.70, 0.66)], -1)
    _png("Elara_FantasmaAnillo", acc * np.array([1.0, 0.75, 0.95]))
    _png("Elara_FantasmaDisco", np.exp(-(r / 0.45) ** 2)[..., None] * np.array([1.0, 0.62, 0.25]))


def _bloque(nombre, keys, ind):
    pad = "\t" * ind
    return [f"{pad}{nombre}", f"{pad}{{"] + [f"{pad}\tkey = {k}" for k in keys] + [f"{pad}}}"]


def destello_cfg():
    """Nodo Scatterer_sunflare de Elara. Las curvas van por distancia a la estrella y son planas en un margen amplio:
    Termos y Titanus quedan dentro tanto si Scatterer mide en radios de la estrella como en Gm."""
    t = f"{S.TEX}/Elara/Destello/Elara_"
    scale = ["1 6 0 -0.2", "30 1.5 -0.01 -0.001", "500 1.1 0 0", "3000 0.7 0 0", "20000 0.3 0 0"]
    inten = lambda pk: ["2 0 0 0", f"12 {pk} 0 0", f"3000 {pk} 0 0", f"20000 {pk * 0.4:g} 0 0"]
    ghost_i = ["2 0 0 0", "12 1 0 0", "3000 1 0 0", "9000 0 0 0"]
    L = ["// Destello de Elara: texturas propias (generar_visuales.destello_texturas): núcleo con corona ciliar,",
         "// 12 picos de difracción irisados y 260 rayos, raya anamórfica, halo con dispersión y 14 fantasmas",
         "// (hexágonos del diafragma, anillos irisados y discos ámbar)",
         "Scatterer_sunflare", "{", "\tElara", "\t{", "\t\tsyntaxVersion = 2", "\t\tflareColor = 1.0,1.0,1.0",
         "\t\tflares", "\t\t{"]
    for tex, pk in (("Nucleo", 1.0), ("Rayos", 0.9), ("Raya", 0.7), ("Halo", 0.35)):
        L += ["\t\t\tItem", "\t\t\t{", f"\t\t\t\ttexture = {t}{tex}.png", "\t\t\t\tdisplayAspectRatio = 1"]
        L += _bloque("scaleCurve", scale, 4) + _bloque("intensityCurve", inten(pk), 4) + ["\t\t\t}"]
    L += ["\t\t}", "\t\tghosts", "\t\t{"]
    for tex, inst in (("FantasmaHex", [(0.35, 0.10, 0.25), (0.22, 0.22, 0.55), (0.16, 0.06, 0.72),
                                        (0.30, 0.22, 1.25), (0.10, 0.30, 1.6), (0.12, 0.12, -0.3)]),
                      ("FantasmaAnillo", [(0.20, 0.30, 0.9), (0.12, 0.48, 1.45), (0.08, 0.6, 0.35)]),
                      ("FantasmaDisco", [(0.35, 0.08, 0.4), (0.5, 0.03, 1.05), (0.2, 0.14, 1.9), (0.25, 0.05, 1.35),
                                         (0.15, 0.2, -0.15)])):
        L += ["\t\t\tItem", "\t\t\t{", f"\t\t\t\ttexture = {t}{tex}.png"] + _bloque("intensityCurve", ghost_i, 4)
        L += ["\t\t\t\tinstances", "\t\t\t\t{"]
        for m, sc, pos in inst:
            L += ["\t\t\t\t\tItem", "\t\t\t\t\t{", f"\t\t\t\t\t\tintensityMultiplier = {m}",
                  "\t\t\t\t\t\tdisplayAspectRatio = 1", f"\t\t\t\t\t\tscale = {sc}",
                  f"\t\t\t\t\t\tsunToScreenCenterPosition = {pos}", "\t\t\t\t\t}"]
        L += ["\t\t\t\t}", "\t\t\t}"]
    L += ["\t\t}", "\t}", "}"]
    return "\n".join(L) + "\n"


def scatterer_cfg():
    items, atmos, oceans = [], [], []
    for body, c in SCATTERER.items():
        ecl = "".join(f"\t\t\t\tItem = {e}\n" for e in c["eclipse"])
        items.append(f"""		Item
		{{
			celestialBodyName = {body}
			transformName = {body}
			loadDistance = {c["load"]:g}
			unloadDistance = {c["unload"]:g}
			hasOcean = {body in OCEANS}
			flatScaledSpaceModel = {c["flat"]}
			usesCloudIntegration = True
			cloudIntegrationUsesScattererSunColors = False
			mainSunCelestialBody = {c["sun"]}
			sunsUseIntensityCurves = False
			eclipseCasters
			{{
{ecl}			}}
		}}
""")
        atmos.append(f"""Scatterer_atmosphere
{{
	Atmo
	{{
		name = {body}
		atmosphereStartRadiusScale = {c["start"]}
		HR = {c["HR"]}
		HM = {c["HM"]}
		m_betaR = {v3(c["betaR"])}
		BETA_MSca = {v3((c["mie"],) * 3)}
		m_mieG = {c["mieG"]}
		ozoneAbsorption = 0.000493593689,0.00142889097,6.45468826E-05
		ozoneHeight = 0
		ozoneFalloff = 10
		useOzone = {c["ozone"]}
		averageGroundReflectance = 0.1
		multipleScattering = True
		godrayStrength = 0.8
		flattenScaledSpaceMesh = 0
		rimBlend = 20
		rimpower = 600
		specR = 40
		specG = 40
		specB = 40
		shininess = 50
		noonSunlightExtinctionStrength = 1
		cloudColorMultiplier = 3
		cloudScatteringMultiplier = 0.2
		cloudSkyIrradianceMultiplier = 0
		volumetricsColorMultiplier = 1
		EVEIntegration_preserveCloudColors = False
		adjustScaledTexture = True
		scaledLandBrightnessAdjust = 1
		scaledLandContrastAdjust = 1
		scaledLandSaturationAdjust = 1
		scaledOceanBrightnessAdjust = 1
		scaledOceanContrastAdjust = 1
		scaledOceanSaturationAdjust = 1
		configPoints
		{{
			Item
			{{
				altitude = 0
				skyExposure = 0.12
				skyAlpha = 1
				skyExtinctionTint = 1
				scatteringExposure = 0.12
				extinctionThickness = 1
				postProcessAlpha = 1
				postProcessDepth = 0
				extinctionTint = 1
			}}
		}}
	}}
}}
""")
    for body, o in OCEANS.items():
        g = S.BODIES[body]["gee"] * S.G0
        oceans.append(f"""Scatterer_ocean
{{
	Ocean
	{{
		name = {body}
		AMP = {o["amp"]}
		m_windSpeed = {o["wind"]}
		m_omega = 0.84
		m_gravity = {g:.3f}
		maxWaveInteractionShipAltitude = 500
		m_whiteCapStr = {o["caps"]}
		shoreFoam = {o["foam"]}
		m_farWhiteCapStr = -0.18
		m_oceanUpwellingColor = {v3(o["up"])}
		m_UnderwaterColor = {v3(o["under"])}
		offScreenVertexStretch = 1.25
		alphaRadius = 1000
		transparencyDepth = {o["clear"]}
		darknessDepth = 1000
		refractionIndex = {o["n"]}
		skyReflectionStrength = 1
		causticsTexturePath = {CAUSTICS}
		causticsLayer1Scale = 0.2,0.2
		causticsLayer1Speed = 0.0612,-0.1512
		causticsLayer2Scale = 0.2771,0.2671
		causticsLayer2Speed = -0.07487,0.17487
		causticsMultiply = 1
		causticsUnderwaterLightBoost = 2
		causticsMinBrightness = 0.5
		causticsBlurDepth = 200
		lightRaysStrength = 1
	}}
}}
""")
    # Destello de Kraken: el de Kerbol, en rojo apagado y más tenue. El de Elara es propio (destello_cfg)
    sun = (KSP / "StockScattererConfigs/Sunflares/Sun.cfg").read_text(encoding="utf-8").lstrip("\ufeff")
    flare = sun.replace("\n    Sun\n", "\n    Kraken\n", 1).replace("flareColor = 1.0,1.0,1.0", "flareColor = 0.6,0.32,0.28", 1)
    flare += "\n" + destello_cfg()
    head = ["// GENERADO por herramientas/generar_visuales.py — no editar a mano.",
            "// Scatterer: atmósferas, océanos y destellos de Kraken y Elara. Usa las cáusticas y destellos de StockScattererConfigs."]
    patch = ["@Scatterer_planetsList:NEEDS[Scatterer]:FOR[MundosLejanos]", "{", "\t@scattererCelestialBodies", "\t{",
             "".join(items).rstrip("\n"), "\t}", "}"]
    return "\n".join(head + patch) + "\n\n" + "\n".join(atmos) + "\n" + "\n".join(oceans) + "\n" + flare


def eve_cfg():
    head = ["// GENERADO por herramientas/generar_visuales.py — no editar a mano.",
            "// EVE: nubes 2D + volumétricas V5 (requiere el EVE de Blackrack y StockVolumetricClouds para el ruido).",
            "EVE_CLOUDS", "{"]
    body = "".join(eve_object(b, c) for b, c in EVE.items())
    body += "".join(eve_object(b, c, c["nombre"], c["src"]) for b, c in EVE_EXTRA.items())
    swap = ["", "// Con EVE las nubes ya las pone EVE: la vista lejana pasa a la textura sin nubes horneadas.",
            "@Kopernicus:AFTER[MundosLejanos]:NEEDS[EnvironmentalVisualEnhancements]", "{"]
    for b, c in EVE.items():
        if c["swap"]:
            swap += [f"\t@Body[{b}]", "\t{", "\t\t@ScaledVersion", "\t\t{", "\t\t\t@Material", "\t\t\t{",
                     f"\t\t\t\t@texture = {S.TEX}/{b}/{b}_ScaledEVE.png", "\t\t\t}", "\t\t}", "\t}"]
    swap.append("}")
    return "\n".join(head) + "\n" + body + "}\n" + "\n".join(swap) + "\n"


def planetshine_cfg():
    out = ["// GENERADO por herramientas/generar_visuales.py — no editar a mano.",
           "// PlanetShine: luz que cada cuerpo refleja sobre las naves (color medio de su textura, intensidad ∝ albedo).",
           "PlanetshineCelestialBody:NEEDS[PlanetShine]", "{", "\tname = Kraken", "\tisSun = True",
           "\tcolor = 255,140,122", "\tintensity = 2", "\tatmosphereAmbient = 0", "\tgroundAmbientOverride = 1", "}",
           "PlanetshineCelestialBody:NEEDS[PlanetShine]", "{", "\tname = Elara", "\tisSun = True",
           "\tcolor = 255,204,158", "\tintensity = 2", "\tatmosphereAmbient = 0", "\tgroundAmbientOverride = 1", "}"]
    for body, alb in ALBEDO.items():
        col = img(body, "Color").reshape(-1, 3).mean(axis=0)
        rgb = ",".join(str(int(round(c))) for c in col)
        inten = round(min(2.0, max(0.03, alb / 0.35)), 2)
        amb = THICK.get(body, 0.2)
        out += ["PlanetshineCelestialBody:NEEDS[PlanetShine]", "{", f"\tname = {body}", f"\tcolor = {rgb}",
                f"\tintensity = {inten}", f"\tatmosphereAmbient = {amb}", "\tgroundAmbientOverride = 1", "}"]
    return "\n".join(out) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for b, c in EVE.items():
        eve_textures(b, c)
    for b, c in EVE_EXTRA.items():
        eve_extra_textures(b, c)
    destello_texturas()
    (OUT / "Scatterer.cfg").write_text(scatterer_cfg(), encoding="utf-8")
    (OUT / "EVE.cfg").write_text(eve_cfg(), encoding="utf-8")
    (OUT / "PlanetShine.cfg").write_text(planetshine_cfg(), encoding="utf-8")
    print(f"Scatterer: {len(SCATTERER)} atmósferas, {len(OCEANS)} océanos, destellos de Kraken y Elara")
    print(f"EVE: {len(EVE) + len(EVE_EXTRA)} capas (2D + volumétricas V5); texturas sin nubes para "
          f"{', '.join(b for b, c in EVE.items() if c['swap'])}")
    print(f"PlanetShine: {len(ALBEDO) + 2} cuerpos")


if __name__ == "__main__":
    main()
