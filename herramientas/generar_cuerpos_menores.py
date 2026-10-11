"""Genera los .cfg de los cuerpos menores de Kraken (lunas y Cinturón Oscuro) a partir de sistema.py.

Salida: GameData/<pack>/Configs/Kraken/Lunas.cfg y CinturonOscuro.cfg
Fades de PQS/escala y límites de warp escalados desde Tal (OPM, R = 22 km), como en CuerposMenores.cfg.
Uso:  python herramientas/generar_cuerpos_menores.py
"""
import pathlib

import sistema as S
from generar_texturas import BIOMES, HEIGHTMAPS

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "GameData" / S.PACK / "Configs" / "Kraken"

# cuerpo: (descripción, rotación s o None = síncrona, ciencia (aterrizado, espacio bajo, alto, recuperación), brillo)
INFO = {
    "Vestigia": ("Vestigia es lo que quedó del impacto que hundió los continentes de Salus: roca fundida que salió "
                 "despedida y volvió a juntarse en órbita. Gira tan cerca de Salus que las mareas la frenan, y describe "
                 "una espiral lentísima que algún día terminará en un segundo choque.",
                 None, (12, 10, 9, 11), 0.05),
    "Nox": ("Una roca casi negra del Cinturón Oscuro que Salus atrapó al pasar. Gira al revés que Vestigia y refleja "
            "menos del 2 % de la luz: desde Salus solo se nota cuando tapa las estrellas.",
            9000, (16, 12, 10, 14), 0.0),
    "Lumen": ("La lámpara de Tenebris. Es hielo de agua casi puro y refleja el 85 % de la luz de Kraken. Tenebris "
              "siempre da la misma cara a la enana, así que su hemisferio nocturno vive a oscuras salvo cuando pasa "
              "Lumen, cada cuatro horas y media, y lo baña de luz rosada. Los colonos extraen agua de su superficie.",
              None, (10, 8, 7, 9), 0.3),
    "Fuligo": ("El mayor del Cinturón Oscuro: un planeta enano cubierto de hollín orgánico que refleja solo el 1 % de "
               "la luz. Desde la órbita parece un agujero en el cielo; únicamente los cráteres frescos dejan ver "
               "puntos grises.", 30000, (20, 15, 12, 18), 0.0),
    "Caligo": ("Su nombre significa niebla oscura. Su polvo de carbono es tan fino que cada impacto levanta una nube "
               "que tarda semanas en volver a posarse, en una gravedad casi nula.", 40000, (20, 15, 12, 18), 0.0),
    "Atra": ("El menor de los tres planetas enanos del cinturón: un cuerpo negro y abollado, unido por su propia "
             "gravedad a duras penas. Es casi invisible incluso desde cerca.", 22000, (20, 15, 12, 18), 0.0),
    "Azabache": ("Un asteroide de carbono vítreo, negro y con reflejos azulados cuando la luz de Kraken lo roza.",
                 11000, (22, 15, 12, 20), 0.15),
    "Brea": ("Un asteroide cubierto de compuestos orgánicos pegajosos, de un pardo casi negro. Las patas de "
             "aterrizaje salen manchadas.", 14000, (22, 15, 12, 20), 0.0),
    "Tizne": ("Un asteroide de polvo tan fino y oscuro que mancha todo lo que lo toca.", 8000, (22, 15, 12, 20), 0.0),
    "Escoria": ("Los restos fundidos de una colisión antigua: escoria vítrea y porosa, negra con vetas pardas.",
                17000, (22, 15, 12, 20), 0.05),
    "Hollin": ("El cuerpo más pequeño y el más oscuro del cinturón: refleja apenas el 1 % de la luz. Encontrarlo es "
               "más difícil que aterrizar en él.", 20000, (22, 15, 12, 20), 0.0),
}
FILES = {"Lunas.cfg": ["Vestigia", "Nox", "Lumen"],
         "CinturonOscuro.cfg": ["Fuligo", "Caligo", "Atra", "Azabache", "Brea", "Tizne", "Escoria", "Hollin"]}
HEADERS = {
    "Lunas.cfg": "LUNAS de Salus (Vestigia, Nox) y de Tenebris (Lumen)",
    "CinturonOscuro.cfg": "CINTURÓN OSCURO (450 000–820 000 km): planetas enanos y asteroides con albedo 0.01–0.02",
}


def g(x):
    return f"{x:.10g}"


def body_cfg(name):
    b, (desc, rot, sci, shine) = S.BODIES[name], INFO[name]
    k = b["radius"] / 22000                                    # escala respecto a Tal (OPM)
    warp = " ".join(str(round(v * k)) for v in (0, 1238, 2475, 4950, 9900, 19800, 39600, 79200))
    o, hm = b["orbit"], HEIGHTMAPS[name]
    tex = f"{S.TEX}/{name}/{name}"
    landed, low, high, rec = sci
    rotation = "\t\t\ttidallyLocked = true" if rot is None else f"\t\t\trotationPeriod = {rot}\n\t\t\ttidallyLocked = false"
    biomes = "\n".join(f"\t\t\t\tBiome\n\t\t\t\t{{\n\t\t\t\t\tname = {n}\n\t\t\t\t\tvalue = {v}\n\t\t\t\t\tcolor = {c}\n\t\t\t\t}}"
                       for (n, c), v in zip(BIOMES["_pequeno"].items(), (1.0, 1.0, 1.1)))
    display = "Hollín" if name == "Hollin" else name
    return f"""	Body
	{{
		name = {name}
		Template
		{{
			name = {b["template"]}
			removeAllPQSMods = true
		}}
		Properties
		{{
			displayName = {display}^N
			description = {desc}
			radius = {b["radius"]}
			geeASL = {g(b["gee"])}
			rotates = true
{rotation}
			initialRotation = 0
			isHomeWorld = false
			timewarpAltitudeLimits = {warp}
			ScienceValues
			{{
				landedDataValue = {landed}
				splashedDataValue = 1
				flyingLowDataValue = 1
				flyingHighDataValue = 1
				inSpaceLowDataValue = {low}
				inSpaceHighDataValue = {high}
				recoveryValue = {rec}
				flyingAltitudeThreshold = 1000
				spaceAltitudeThreshold = {round(b["radius"] * 0.5, -3):.0f}
			}}
			biomeMap = {tex}_Biomes.png
			Biomes
			{{
{biomes}
			}}
		}}
		Orbit
		{{
			referenceBody = {b["parent"]}
			semiMajorAxis = {g(o["a"])}
			eccentricity = {g(o["e"])}
			inclination = {g(o["i"])}
			longitudeOfAscendingNode = {g(o["lan"])}
			argumentOfPeriapsis = {g(o["argpe"])}
			meanAnomalyAtEpoch = {g(o["M0"])}
			epoch = 0
		}}
		ScaledVersion
		{{
			type = Vacuum
			fadeStart = {round(34400 * k)}
			fadeEnd = {round(68800 * k)}
			Material
			{{
				texture = {tex}_Color.png
				normals = {tex}_Normal.png
				shininess = {g(shine)}
			}}
		}}
		PQS
		{{
			fadeStart = {round(68800 * k)}
			fadeEnd = {round(137600 * k)}
			deactivateAltitude = {round(138288 * k)}
			Mods
			{{
				VertexHeightMap
				{{
					map = {tex}_Height.png
					offset = {hm["offset"]}
					deformity = {hm["deformity"]}
					scaleDeformityByRadius = false
					order = 10
					enabled = true
				}}
				VertexColorMap
				{{
					map = {tex}_Color.png
					order = 50
					enabled = true
				}}
			}}
		}}
	}}
"""


def main():
    for fname, names in FILES.items():
        head = ["// " + "=" * 77,
                f"//  {HEADERS[fname]}",
                "//  GENERADO por herramientas/generar_cuerpos_menores.py desde sistema.py: no editar a mano.",
                "// " + "=" * 77,
                "@Kopernicus:FOR[MundosLejanos]", "{"]
        text = "\n".join(head) + "\n" + "".join(body_cfg(n) for n in names) + "}\n"
        (OUT / fname).write_text(text, encoding="utf-8")
        print(f"{fname}: {', '.join(names)}")


if __name__ == "__main__":
    main()
