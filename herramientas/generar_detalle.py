"""Detalle de superficie a ras de suelo para todos los cuerpos rocosos.

1) Configs/Kraken/Parallax_Terreno.cfg (nodo ParallaxTerrain): terreno de Parallax Continued, con texturas de
   suelo, desplazamiento y oclusión. Reutiliza los juegos de texturas stock de Parallax_StockTerrainTextures (el
   más parecido a cada cuerpo); el color lo sigue poniendo el VertexColorMap del cuerpo. Las mezclas
   bajo/medio/alto se ajustan al rango de alturas de cada uno.
2) Configs/Detalle_PQS.cfg: PQSMods de Kopernicus que añaden colinas y rugosidad de varias escalas
   (VertexHeightNoise multifractal) y variación de color a ras de suelo (VertexColorNoise). Sin ellos, el terreno
   cercano es la interpolación suave del mapa de altura: "lomas lisas".
Uso:  python herramientas/generar_detalle.py
"""
import copy
import math
import pathlib

import sistema as S
from generar_scatters import parse
from generar_texturas import HEIGHTMAPS

ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG = ROOT / "GameData" / S.PACK / "Configs"
STOCK = pathlib.Path(r"C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program/GameData"
                     r"/Parallax_StockTerrainTextures/Terrain.cfg")
SETS = {"Kerbin", "Mun", "Duna", "Gilly", "Eve", "Moho", "Ike", "Eeloo", "Minmus", "Laythe", "Dres", "Vall", "Tylo",
        "Bop", "Pol"}
# Juego de texturas de Parallax por cuerpo (si no está aquí, el de su plantilla)
TERRAIN_SET = {"Skolta": "Duna", "Norh": "Tylo", "Tenebris": "Moho", "Salus": "Laythe", "Scarch": "Duna",
               "Halum": "Eeloo", "Termos": "Laythe", "Ignea": "Moho", "Lumen": "Vall", "Secunda": "Eeloo",
               "Fuligo": "Dres", "Caligo": "Dres", "Atra": "Dres", "Ceniza": "Mun", "Vestigia": "Mun", "Akira": "Eeloo",
               "Titanus": "Moho"}
OCEAN = {"Halum", "Norh", "Skolta", "Scarch", "Tenebris", "Salus", "Termos", "Titanus"}
# Cuerpos con zonas que deben quedar planas (plataforma de la colonia, baliza): menos ruido de altura
# Halum: continentes de hielo flotante a +160 m que el ruido no debe hundir bajo el neón
FLAT = {"Tenebris": 0.3, "Hollin": 0.3, "Halum": 0.4}


def stock_blocks():
    root = parse(STOCK.read_text(encoding="utf-8-sig"))
    return {b.get("name"): b for b in root.node("ParallaxTerrain").nodes("Body")}


def rocky():
    return [b for b, r in S.BODIES.items() if b in HEIGHTMAPS and r.get("kind") != "star"]


def terrain_cfg():
    blocks = stock_blocks()
    out = ["// GENERADO por herramientas/generar_detalle.py — no editar a mano.",
           "// Terreno de Parallax Continued con los juegos de texturas stock (Parallax_StockTerrainTextures).",
           "ParallaxTerrain", "{"]
    for body in rocky():
        src = TERRAIN_SET.get(body, S.BODIES[body]["template"])
        if src not in SETS:
            src = "Mun"
        b = copy.deepcopy(blocks[src])
        b.set("name", body)
        hm = HEIGHTMAPS[body]
        lo, span = hm["offset"], hm["deformity"]
        props = b.node("ShaderProperties")
        if props.get("_LowMidBlendStart") and float(props.get("_LowMidBlendStart")) > -9000:
            low_mid = max(30.0, lo + 0.30 * span) if body in OCEAN else lo + 0.30 * span
            mid_high = lo + 0.70 * span
            for k, v in (("_LowMidBlendStart", low_mid), ("_LowMidBlendEnd", low_mid + 0.05 * span),
                         ("_MidHighBlendStart", mid_high), ("_MidHighBlendEnd", mid_high + 0.08 * span)):
                props.set(k, f"{v:.0f}")
        out.append(f"\t// {body}: texturas de {src}")
        out += b.dump(1)
    out.append("}")
    (CFG / "Kraken" / "Parallax_Terreno.cfg").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Parallax_Terreno.cfg: {len(rocky())} cuerpos")


def detail_cfg():
    out = ["// GENERADO por herramientas/generar_detalle.py — no editar a mano.",
           "// Relieve y color a ras de suelo: colinas multifractales y rugosidad (VertexHeightNoise) y variación",
           "// de color (VertexColorNoise). Escalas según el radio: colinas de ~60 km en planetas, ~8 km en cuerpos menores.",
           f"@Kopernicus:AFTER[{S.PACK}]", "{"]
    for i, body in enumerate(rocky()):
        R, span = S.BODIES[body]["radius"], HEIGHTMAPS[body]["deformity"]
        big = R >= 200_000
        hill = 60_000 if big else 8_000                        # longitud de onda de la octava más baja (m)
        freq = max(4.0, 2 * math.pi * R / hill)
        amp = min(400.0 if big else 150.0, (0.05 if big else 0.03) * span) * FLAT.get(body, 1.0)
        rough = min(25.0, 0.004 * span) * FLAT.get(body, 1.0)
        out += [f"\t@Body[{body}]", "\t{", "\t\t@PQS", "\t\t{", "\t\t\t@Mods", "\t\t\t{",
                "\t\t\t\tVertexHeightNoise\t// colinas y crestas",
                "\t\t\t\t{", f"\t\t\t\t\tdeformity = {amp:.0f}", f"\t\t\t\t\tfrequency = {freq:.1f}",
                "\t\t\t\t\toctaves = 8", "\t\t\t\t\tpersistence = 0.5", "\t\t\t\t\tlacunarity = 2.2",
                f"\t\t\t\t\tseed = {7100 + i}", "\t\t\t\t\tnoiseType = RidgedMultifractal", "\t\t\t\t\tmode = High",
                "\t\t\t\t\torder = 25", "\t\t\t\t\tenabled = true", "\t\t\t\t}",
                "\t\t\t\tVertexHeightNoise\t// rugosidad de cientos de metros",
                "\t\t\t\t{", f"\t\t\t\t\tdeformity = {rough:.0f}", f"\t\t\t\t\tfrequency = {freq * 40:.0f}",
                "\t\t\t\t\toctaves = 6", "\t\t\t\t\tpersistence = 0.55", "\t\t\t\t\tlacunarity = 2.0",
                f"\t\t\t\t\tseed = {7200 + i}", "\t\t\t\t\tnoiseType = Perlin", "\t\t\t\t\tmode = High",
                "\t\t\t\t\torder = 26", "\t\t\t\t\tenabled = true", "\t\t\t\t}",
                "\t\t\t\tVertexColorNoise\t// manchas de color a ras de suelo",
                "\t\t\t\t{", "\t\t\t\t\tblend = 0.12", f"\t\t\t\t\tfrequency = {freq * 25:.0f}", "\t\t\t\t\toctaves = 6",
                "\t\t\t\t\tpersistance = 0.6", "\t\t\t\t\tlacunarity = 2.1", f"\t\t\t\t\tseed = {7300 + i}",
                "\t\t\t\t\tnoiseType = Perlin", "\t\t\t\t\tmode = High", "\t\t\t\t\torder = 60",
                "\t\t\t\t\tenabled = true", "\t\t\t\t}",
                "\t\t\t}", "\t\t}", "\t}"]
    out.append("}")
    (CFG / "Detalle_PQS.cfg").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"Detalle_PQS.cfg: {len(rocky())} cuerpos")


if __name__ == "__main__":
    terrain_cfg()
    detail_cfg()
