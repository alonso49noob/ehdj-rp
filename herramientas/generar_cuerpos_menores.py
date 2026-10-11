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
    "Vestigia": ("Vestigia es lo que quedó del impacto que hundió los continentes de Salus: roca fundida que salió despedida y volvió a juntarse en órbita. Luego recibió su propio golpe: una cuenca de tres anillos concéntricos, con el fondo de vidrio oscuro, ocupa casi un hemisferio. Gira tan cerca de Salus que las mareas la frenan, y describe una espiral lentísima que algún día terminará en un segundo choque.",
                 None, (12, 10, 9, 11), 0.05),
    "Nox": ("Una roca casi negra del Cinturón Oscuro que Salus atrapó al pasar. Un impacto casi la parte en dos: el cráter que dejó ocupa media cara, y los surcos paralelos que la cruzan son las grietas de aquel golpe. Gira al revés que Vestigia y refleja menos del 2 % de la luz: desde Salus solo se nota cuando tapa las estrellas.",
            9000, (16, 12, 10, 14), 0.0),
    "Lumen": ("La lámpara de Tenebris. Las mareas de Tenebris la calientan por dentro, y en su polo sur se abren cuatro grietas paralelas, las franjas de tigre, por las que salen géiseres de vapor que vuelven a caer como nieve fresca. El resto de su hielo está sucio del polvo oscuro del disco de Kraken y solo refleja un 35 % de la luz: poco, pero el triple que Tenebris. Tenebris siempre da la misma cara a la enana, así que su hemisferio nocturno vive a oscuras salvo cuando pasa Lumen y lo alumbra con un reflejo tenue y rojizo. Los colonos extraen agua de su superficie.",
              None, (10, 8, 7, 9), 0.15),
    "Fuligo": ("El mayor del Cinturón Oscuro: un planeta enano cubierto de hollín orgánico que refleja solo el 1 % de la luz. Casi no se ve, salvo por el Ojo: un cráter cuyo fondo está cubierto de sales brillantes que subieron del interior. Es lo único que delata a Fuligo desde lejos.", 30000, (20, 15, 12, 18), 0.0),
    "Caligo": ("Su nombre significa niebla oscura. Su polvo de carbono es tan fino que cada impacto levanta una nube que tarda semanas en volver a posarse. Lo cruza una catena: una cadena de doce cráteres alineados que dejó un cometa al que las mareas de Kraken partieron en pedazos justo antes del choque.", 40000, (20, 15, 12, 18), 0.0),
    "Atra": ("Atra no se parece a nada del cinturón: es un puro tres veces más largo que ancho, con los extremos rojizos. Su composición no coincide con la de los demás cuerpos de Kraken, así que tuvo que venir del espacio interestelar y quedar atrapada en el cinturón. Es casi invisible incluso desde cerca.", 22000, (20, 15, 12, 18), 0.0),
    "Azabache": ("Un asteroide de carbono vítreo tallado en facetas planas, como una gema mal pulida. Cuando la luz de Kraken lo roza, los bordes de las facetas destellan en azul.",
                 11000, (22, 15, 12, 20), 0.15),
    "Brea": ("Un asteroide liso y redondeado, sin apenas cráteres: los compuestos orgánicos que lo cubren fluyen muy despacio y borran las cicatrices. En las depresiones forman charcos de brea, negros y planos. Las patas de aterrizaje salen manchadas.", 14000, (22, 15, 12, 20), 0.0),
    "Tizne": ("Un montón de escombros que apenas se mantiene unido: su superficie está sembrada de bloques sueltos del tamaño de edificios, cubiertos de un polvo tan fino y oscuro que mancha todo lo que toca.", 8000, (22, 15, 12, 20), 0.0),
    "Escoria": ("Los restos fundidos de una colisión antigua. Al enfriarse, el gas atrapado dejó cientos de vesículas: es una esponja de escoria vítrea, negra con vetas pardas.",
                17000, (22, 15, 12, 20), 0.05),
    "Hollin": ("El cuerpo más pequeño y el más oscuro del cinturón: refleja apenas el 1 % de la luz. Y no está vacío: en su ecuador hay una plataforma nivelada con una estructura metálica encima. Las máquinas estuvieron aquí.", 20000, (22, 15, 12, 20), 0.0),
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
    table = BIOMES.get(name, BIOMES["_pequeno"])          # 3 biomas comunes + el del rasgo único
    biomes = "\n".join(f"\t\t\t\tBiome\n\t\t\t\t{{\n\t\t\t\t\tname = {n}\n\t\t\t\t\tvalue = {v}\n\t\t\t\t\tcolor = {c}\n\t\t\t\t}}"
                       for (n, c), v in zip(table.items(), (1.0, 1.0, 1.1, 1.6)))
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
