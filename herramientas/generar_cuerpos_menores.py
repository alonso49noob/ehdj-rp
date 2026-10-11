"""Genera los .cfg de los cuerpos menores (lunas y Cinturón Oscuro de Kraken, Ceniza de Skolta, Tyrna y Karmen de
Termos) a partir de sistema.py.

Salida: GameData/<pack>/Configs/Kraken/Lunas.cfg, Kraken/CinturonOscuro.cfg, Skolta/Ceniza.cfg y Termos/Lunas.cfg
Fades de PQS/escala y límites de warp escalados desde Tal (OPM, R = 22 km), como en CuerposMenores.cfg.
Uso:  python herramientas/generar_cuerpos_menores.py
"""
import pathlib

import sistema as S
from generar_texturas import BIOMES, HEIGHTMAPS

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "GameData" / S.PACK / "Configs"

# cuerpo: (descripción, rotación s o None = síncrona, ciencia (aterrizado, espacio bajo, alto, recuperación), brillo)
# brillo: especular de la vista lejana (0 = mate). _Color es opaco (el PQS también lo usa): el brillo va en specColor.
INFO = {
    "Vestigia": ("Vestigia es lo que quedó del impacto que hundió los continentes de Salus: roca fundida que salió despedida y volvió a juntarse en órbita. Luego recibió su propio golpe: una cuenca de tres anillos concéntricos, con el fondo de vidrio oscuro, ocupa casi un hemisferio. Gira tan cerca de Salus que las mareas la frenan, y describe una espiral lentísima que algún día terminará en un segundo choque.",
                 None, (12, 10, 9, 11), 0.05),
    "Nox": ("Una roca casi negra del Cinturón Oscuro que Salus atrapó al pasar. Un impacto casi la parte en dos: el cráter que dejó ocupa media cara, y los surcos paralelos que la cruzan son las grietas de aquel golpe. Gira al revés que Vestigia y refleja menos del 2 % de la luz: desde Salus solo se nota cuando tapa las estrellas.",
            9000, (16, 12, 10, 14), 0.0),
    "Lumen": ("La lámpara de Tenebris. Las mareas de Tenebris la calientan por dentro, y en su polo sur se abren cuatro grietas paralelas, las franjas de tigre, por las que salen géiseres de vapor que vuelven a caer como nieve fresca. El resto de su hielo está sucio del polvo oscuro del disco de Kraken y solo refleja un 35 % de la luz: poco, pero el triple que Tenebris. Las noches de Tenebris duran 18 horas, y Lumen es lo único que las alumbra con un reflejo tenue y rojizo. Los colonos extraen agua de su superficie.",
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
    "Ceniza": ("La luna de Skolta: una roca parda de 350 km de diámetro, capturada del cinturón de asteroides, que gira en una órbita inclinada 18°. Su superficie es de arcillas con amonio, como la de Ceres. Cerca del ecuador se alza el Monte Solitario, un domo de hielo y sales de 3 km de altura con las laderas surcadas de vetas claras: un criovolcán que se apagó hace poco. Desde el suelo de Skolta casi no se ve: la bruma la reduce a una mancha borrosa.",
               None, (8, 6, 5, 7), 0.1),
    "Tyrna": ("La mayor luna de Termos: una bola de hielo de 117 km con la superficie salpicada de metales. Su órbita es algo excéntrica, así que las mareas de Termos la estiran y la aprietan en cada vuelta; ese calor abre fisuras por las que sube salmuera del interior. Al congelarse, la salmuera deja vetas oscuras de hierro, níquel y cobre sobre el hielo claro, y los impactos del cinturón sembraron el resto de fragmentos metálicos. Metales a la vista y casi sin gravedad: es una mina ideal.",
              None, (9, 7, 6, 8), 0.12),
    "Karmen": ("Una luna diminuta, del tamaño de un asteroide, que gira mucho más allá de Tyrna en una órbita excéntrica e inclinada: Termos la capturó del cinturón. Es un fragmento del núcleo metálico de un cuerpo que se rompió en una colisión. Una de sus caras es plana y lisa, la superficie de la fractura, y brilla como acero pulido cuando le da la luz.",
               31000, (10, 8, 7, 9), 0.4),
    "Hollin": ("El cuerpo más pequeño y el más oscuro del cinturón: refleja apenas el 1 % de la luz. Y no está vacío: en su ecuador hay una plataforma nivelada con una estructura metálica encima. Las máquinas estuvieron aquí.", 20000, (22, 15, 12, 20), 0.0),
}
FILES = {"Kraken/Lunas.cfg": ["Vestigia", "Nox", "Lumen"],
         "Kraken/CinturonOscuro.cfg": ["Fuligo", "Caligo", "Atra", "Azabache", "Brea", "Tizne", "Escoria", "Hollin"],
         "Skolta/Ceniza.cfg": ["Ceniza"],
         "Termos/Lunas.cfg": ["Tyrna", "Karmen"]}
HEADERS = {
    "Kraken/Lunas.cfg": "LUNAS de Salus (Vestigia, Nox) y de Tenebris (Lumen)",
    "Kraken/CinturonOscuro.cfg": "CINTURÓN OSCURO (450 000–820 000 km): planetas enanos y asteroides con albedo 0.01–0.02",
    "Skolta/Ceniza.cfg": "CENIZA, la luna de Skolta (propuesta de la ficha: una luna mediana, capturada)",
    "Termos/Lunas.cfg": "LUNAS de Termos: Tyrna (helada, criovolcánica y llena de metales) y Karmen (asteroide capturado)",
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
				specColor = {g(round(0.6 * shine, 3))},{g(round(0.6 * shine, 3))},{g(round(0.6 * shine, 3))},1
				shininess = 0.3
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
