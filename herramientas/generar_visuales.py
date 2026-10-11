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
from generar_texturas import HEIGHTMAPS, SALUS_ICE, hexrgb

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
    "Tenebris": dict(sun="Kraken", flat=True, load=3e8, unload=5e8, start=1, HR=6, HM=1.5,
                     betaR=(0.0200, 0.0400, 0.0800), mie=0.0158, mieG=0.85, ozone=False, eclipse=["Lumen"]),
    "Salus": dict(sun="Kraken", flat=True, load=3e8, unload=5e8, start=1, HR=5.5, HM=1.5,
                  betaR=(0.0250, 0.0450, 0.0750), mie=0.0200, mieG=0.85, ozone=False, eclipse=["Vestigia", "Nox"]),
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
}

# ------------------------------------------------------------------ EVE
# altura de la capa, rango de nubes volumétricas, color, fades de escala
EVE = {
    "Halum": dict(alt=20000, lo=20000, hi=26000, color=(230, 236, 245), fade=(230000, 280000), swap=True),
    "Tenebris": dict(alt=2500, lo=2500, hi=9000, color=(150, 146, 142), fade=(140000, 180000), swap=True),
    "Salus": dict(alt=2000, lo=2000, hi=8000, color=(228, 228, 224), fade=(120000, 160000), swap=True),
    "Scarch": dict(alt=3000, lo=3000, hi=12000, color=(140, 110, 100), fade=(130000, 170000), swap=False),
    "Creus": dict(alt=60000, lo=60000, hi=78000, color=(240, 244, 246), fade=(450000, 550000), swap=False),
}
OCEAN_SCALED = {"Halum": "#6b94cc", "Tenebris": "#0d0f12", "Salus": "#24484a"}   # color del mar visto desde órbita

# ------------------------------------------------------------------ PlanetShine (albedo -> intensidad de luz reflejada)
ALBEDO = {"Creus": 0.70, "Halum": 0.55, "Ocrea": 0.85, "Pastora": 0.05, "Prima": 0.15, "Secunda": 0.60,
          "Heraldo": 0.04, "Krax": 0.03, "Scarch": 0.35, "Tenebris": 0.12, "Salus": 0.30, "Vestigia": 0.12,
          "Nox": 0.02, "Lumen": 0.35, "Ignea": 0.15, "Fuligo": 0.01, "Caligo": 0.015, "Atra": 0.012,
          "Azabache": 0.02, "Brea": 0.015, "Tizne": 0.012, "Escoria": 0.02, "Hollin": 0.01}
THICK = {"Creus": 1.0, "Halum": 1.0, "Scarch": 1.0, "Tenebris": 0.6, "Salus": 0.6}


def img(body, kind, mode="RGB"):
    return np.asarray(Image.open(GD_TEX / body / f"{body}_{kind}.png").convert(mode), np.float32)


def height(body, shape):
    hm = HEIGHTMAPS[body]
    g = Image.open(GD_TEX / body / f"{body}_Height.png").resize(shape[::-1], Image.BILINEAR)
    return hm["offset"] + np.asarray(g, np.float32) / 255 * hm["deformity"]


def coverage(body):
    """Cobertura de nubes 0..1 (2048×1024) reconstruida de las texturas del pack."""
    col = img(body, "Color")
    if body == "Halum":
        cov = img(body, "Clouds", "RGBA")[..., 3] / 255
    elif body in ("Tenebris", "Salus"):
        surf = img(body, "Surface")
        diff = np.abs(col - surf).sum(axis=2)
        lum = col.mean(axis=2)
        cov = np.where(diff > 6, np.clip((lum - 60) / 150, 0.35, 1.0), 0.0)
        if body == "Salus":   # el hielo polar no es nube
            ice = np.abs(col - hexrgb(SALUS_ICE)).sum(axis=2) < 6
            cov = np.where(ice, 0.0, cov)
    elif body == "Scarch":   # celdas de tormenta a partir de la neblina
        haze = (col - 0.35 * img(body, "Surface")) / 0.65
        lum = haze.mean(axis=2)
        cov = np.clip((lum - np.quantile(lum, 0.55)) / (np.quantile(lum, 0.95) - np.quantile(lum, 0.55)), 0, 1)
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
    rgba[..., 3] = (cov * 255).astype(np.uint8)
    Image.fromarray(rgba, "RGBA").save(GD_TEX / body / f"{body}_EVEClouds.png", optimize=True)
    if cfg["swap"]:          # vista lejana sin nubes: mar del color del océano, tierra = terreno real
        surf = img(body, "Surface")
        h = height(body, surf.shape[:2])
        sea = np.array([int(OCEAN_SCALED[body][i:i + 2], 16) for i in (1, 3, 5)], np.float32)
        out = np.where((h < 0)[..., None], sea, surf)
        if body == "Salus":  # conserva el hielo salobre polar
            col = img(body, "Color")
            ice = np.abs(col - hexrgb(SALUS_ICE)).sum(axis=2) < 6
            out = np.where(ice[..., None], col, out)
        Image.fromarray(out.astype(np.uint8)).save(GD_TEX / body / f"{body}_ScaledEVE.png", optimize=True)


def eve_object(body, cfg):
    tex = f"{S.TEX}/{body}/{body}"
    r, g, b = cfg["color"]
    return f"""	OBJECT
	{{
		name = {body}-nubes
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
				value = {tex}_EVEClouds
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
				value = {tex}_EVECoverage
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
					density = 0.0001
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
					density = 0.02
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
    # Destello de Kraken: el de Kerbol, en rojo apagado y más tenue
    flare = (KSP / "StockScattererConfigs/Sunflares/Sun.cfg").read_text(encoding="utf-8").lstrip("\ufeff")
    flare = flare.replace("\n    Sun\n", "\n    Kraken\n", 1).replace("flareColor = 1.0,1.0,1.0", "flareColor = 0.6,0.32,0.28", 1)
    head = ["// GENERADO por herramientas/generar_visuales.py — no editar a mano.",
            "// Scatterer: atmósferas, océanos y destello de Kraken. Usa las cáusticas y destellos de StockScattererConfigs."]
    patch = ["@Scatterer_planetsList:NEEDS[Scatterer]:FOR[MundosLejanos]", "{", "\t@scattererCelestialBodies", "\t{",
             "".join(items).rstrip("\n"), "\t}", "}"]
    return "\n".join(head + patch) + "\n\n" + "\n".join(atmos) + "\n" + "\n".join(oceans) + "\n" + flare


def eve_cfg():
    head = ["// GENERADO por herramientas/generar_visuales.py — no editar a mano.",
            "// EVE: nubes 2D + volumétricas V5 (requiere el EVE de Blackrack y StockVolumetricClouds para el ruido).",
            "EVE_CLOUDS", "{"]
    body = "".join(eve_object(b, c) for b, c in EVE.items())
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
           "\tcolor = 255,140,122", "\tintensity = 2", "\tatmosphereAmbient = 0", "\tgroundAmbientOverride = 1", "}"]
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
    (OUT / "Scatterer.cfg").write_text(scatterer_cfg(), encoding="utf-8")
    (OUT / "EVE.cfg").write_text(eve_cfg(), encoding="utf-8")
    (OUT / "PlanetShine.cfg").write_text(planetshine_cfg(), encoding="utf-8")
    print(f"Scatterer: {len(SCATTERER)} atmósferas, {len(OCEANS)} océanos, destello de Kraken")
    print(f"EVE: {len(EVE)} capas (2D + volumétricas V5); texturas sin nubes para "
          f"{', '.join(b for b, c in EVE.items() if c['swap'])}")
    print(f"PlanetShine: {len(ALBEDO) + 1} cuerpos")


if __name__ == "__main__":
    main()
