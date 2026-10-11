"""Genera los scatters de Parallax Continued del sistema Kraken (rocas nativas, máquinas y flora negra).

Clona bloques `Scatter` de las configs de Parallax_StockScatterTextures instaladas (modelos,
LODs y materiales que ya funcionan) y solo cambia el nombre, el tinte (_Color), la densidad,
la altitud mínima y la lista negra de biomas. Las máquinas usan las agujas y racimos metálicos
de Moho, restringidas a los biomas de las máquinas.

Uso:  python herramientas/generar_scatters.py
Salida: GameData/<pack>/Configs/Kraken/Parallax_Scatters.cfg
"""
import copy
import pathlib

import sistema as S
from generar_texturas import BIOMES

ROOT = pathlib.Path(__file__).resolve().parents[1]
STOCK = pathlib.Path(r"C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program/GameData"
                     r"/Parallax_StockScatterTextures/Configs")
OUT = ROOT / "GameData" / S.PACK / "Configs" / "Kraken" / "Parallax_Scatters.cfg"

MACHINE = (0.45, 0.40, 0.42)   # acero oscuro de las máquinas

# cuerpo: [(cuerpo de origen, scatter de origen, nombre nuevo, tinte RGB, densidad×, solo_biomas, sin_biomas, minAlt)]
PLAN = {
    "Krax": [
        ("Tylo", "SmallCluster", "RocasGrafito", (0.30, 0.30, 0.33), 1.0, None, ["Fundicion de las Maquinas"], None),
        ("Tylo", "LargeCluster", "BloquesGrafito", (0.30, 0.30, 0.33), 1.0, None, ["Fundicion de las Maquinas"], None),
        ("Moho", "MetalSpire", "MaquinaTorre", MACHINE, 25.0, ["Fundicion de las Maquinas"], None, None),
        ("Moho", "MetalSpireWide", "MaquinaRefineria", MACHINE, 25.0, ["Fundicion de las Maquinas"], None, None),
        ("Moho", "SmallMetalCluster", "MaquinaChatarra", MACHINE, 1.0, ["Fundicion de las Maquinas"], None, None),
        ("Moho", "LargeMetalCluster", "MaquinaModulo", MACHINE, 1.0, ["Fundicion de las Maquinas"], None, None),
    ],
    "Scarch": [
        ("Duna", "SlabsSmall", "LosasBasalto", (0.85, 0.70, 0.66), 1.0, None, ["Mar Acido", "Campos de Extraccion"], 2),
        ("Duna", "SlabsMed", "LosasBasaltoMed", (0.85, 0.70, 0.66), 1.0, None, ["Mar Acido", "Campos de Extraccion"], 2),
        ("Duna", "SmallRocksVar1", "RocasVolcanicas", (0.55, 0.45, 0.43), 1.0, None, ["Mar Acido"], 2),
        ("Moho", "MetalSpireWider", "MaquinaExtractora", MACHINE, 25.0, ["Campos de Extraccion"], None, 2),
        ("Moho", "MetalSpire", "MaquinaTorre", MACHINE, 25.0, ["Campos de Extraccion"], None, 2),
        ("Moho", "HugeMetalCluster", "MaquinaPlanta", MACHINE, 1.0, ["Campos de Extraccion"], None, 2),
        ("Moho", "LargeMetalCluster", "MaquinaModulo", MACHINE, 1.0, ["Campos de Extraccion"], None, 2),
    ],
    "Tenebris": [
        ("Tylo", "SmallSlabs", "LosasBasalto", (0.35, 0.35, 0.40), 1.0, None,
         ["Oceano Oscuro", "Asentamiento Kerbal"], 2),
        ("Eve", "Flora", "FloraNegra", (0.10, 0.10, 0.11), 1.0, ["Bosques Negros"], None, 2),
        ("Laythe", "LaytheFern", "HelechoNegro", (0.10, 0.10, 0.11), 1.0, ["Bosques Negros"], None, 2),
        ("Laythe", "LaytheShrub", "ArbustoNegro", (0.10, 0.10, 0.11), 1.0, ["Bosques Negros"], None, 2),
        ("Moho", "MetalSpireWide", "MaquinaDerribada", (0.60, 0.35, 0.25), 15.0, ["Restos de la Maquina"], None, None),
        ("Moho", "SmallMetalCluster", "RestosMaquina", (0.60, 0.35, 0.25), 1.0, ["Restos de la Maquina"], None, None),
    ],
    "Salus": [
        ("Duna", "SlabsSmall", "CostrasSal", (1.40, 1.35, 1.25), 1.0, ["Arcos de Islas"], None, 2),
    ],
    "Vestigia": [
        ("Tylo", "SmallRocksVar1", "RocasVitrificadas", (0.90, 0.88, 0.86), 1.0, None, None, None),
        ("Tylo", "MedRocksVar1", "RocasVitrificadasMed", (0.90, 0.88, 0.86), 1.0, None, None, None),
    ],
    "Lumen": [  # cristales de hielo de Ike, blanqueados
        ("Ike", "SmallCrystals", "CristalesHielo", (1.30, 1.30, 1.35), 1.0, None, None, None),
        ("Ike", "TallCrystals", "CristalesAltos", (1.30, 1.30, 1.35), 1.0, None, None, None),
        ("Tylo", "SmallRocksVar1", "BloquesHielo", (1.60, 1.60, 1.70), 1.0, None, None, None),
    ],
    # Cinturón Oscuro: rocas casi negras (albedo 0.01–0.02)
    "Fuligo": [("Dres", "SmallRocksVar1", "RocasHollin", (0.12, 0.12, 0.13), 1.0, None, None, None),
               ("Dres", "MedRocksVar1", "BloquesHollin", (0.12, 0.12, 0.13), 1.0, None, None, None)],
    "Caligo": [("Dres", "SmallRocksVar1", "RocasCarbono", (0.11, 0.10, 0.12), 1.0, None, None, None)],
    "Atra": [("Dres", "MedRocksVar1", "BloquesNegros", (0.10, 0.10, 0.10), 1.0, None, None, None)],
    "Ignea": [
        ("Dres", "SmallRocksVar1", "CostraRota", (0.35, 0.22, 0.18), 1.0, ["Costra Enfriada"], None, None),
        ("Dres", "MedRocksVar1", "BloquesCostra", (0.35, 0.22, 0.18), 1.0, ["Costra Enfriada"], None, None),
    ],
}


# ------------------------------------------------------------------ ConfigNode mínimo con orden
class Node:
    def __init__(self, name):
        self.name, self.items = name, []      # items: ("v", key, value) | ("n", Node)

    def get(self, key):
        return next((v for t, k, v in (i for i in self.items if i[0] == "v") if k == key), None)

    def set(self, key, value):
        for i, it in enumerate(self.items):
            if it[0] == "v" and it[1] == key:
                self.items[i] = ("v", key, value)
                return
        self.items.append(("v", key, value))

    def node(self, name):
        return next((it[1] for it in self.items if it[0] == "n" and it[1].name == name), None)

    def nodes(self, name):
        return [it[1] for it in self.items if it[0] == "n" and it[1].name == name]

    def remove_node(self, name):
        self.items = [it for it in self.items if not (it[0] == "n" and it[1].name == name)]

    def dump(self, depth=0):
        tab = "\t" * depth
        out = [f"{tab}{self.name}", f"{tab}{{"]
        for it in self.items:
            if it[0] == "v":
                out.append(f"{tab}\t{it[1]} = {it[2]}")
            else:
                out += it[1].dump(depth + 1)
        out.append(f"{tab}}}")
        return out


def parse(text):
    root, stack, pending = Node("root"), [], None
    stack.append(root)
    for raw in text.lstrip("\ufeff").splitlines():
        line = raw.split("//", 1)[0].strip()
        if not line:
            continue
        if line == "{":
            n = Node(pending)
            stack[-1].items.append(("n", n))
            stack.append(n)
            pending = None
        elif line == "}":
            stack.pop()
        elif "=" in line:
            k, v = line.split("=", 1)
            stack[-1].items.append(("v", k.strip(), v.strip()))
        else:
            pending = line
    return root


_cache = {}


def stock_scatter(body, name):
    if body not in _cache:
        _cache[body] = parse((STOCK / f"{body}.cfg").read_text(encoding="utf-8"))
    b = _cache[body].node("ParallaxScatters").node("Body")
    sc = next((s for s in b.nodes("Scatter") if s.get("name") == name), None)
    if sc is None:
        raise SystemExit(f"No existe el scatter {name} en {body}.cfg")
    return copy.deepcopy(sc)


def tint(color, rgb):
    vals = [float(x) for x in (color or "1,1,1,1").split(",")]
    return ",".join(f"{v * t:.3f}" for v, t in zip(vals[:3], rgb)) + f",{vals[3] if len(vals) > 3 else 1:g}"


# Subdivisión de Parallax por cuerpo (nivel, radio), como en Parallax_StockTerrainTextures
SUBDIV = {"Krax": (7, 700), "Scarch": (6, 600), "Tenebris": (6, 600), "Salus": (6, 500), "Vestigia": (6, 500),
          "Ignea": (6, 500), "Lumen": (6, 700), "Fuligo": (6, 500), "Caligo": (6, 500), "Atra": (6, 500)}
PQS_OUT = OUT.with_name("Parallax_PQS.cfg")


def write_pqs_patch():
    """Parallax solo reparte scatters en cuerpos con su PQSMod `Parallax` (ver Parallax_StockTerrainTextures)."""
    missing = set(PLAN) - set(SUBDIV)
    if missing:
        raise SystemExit(f"Falta SUBDIV para: {sorted(missing)}")
    lines = ["// GENERADO por herramientas/generar_scatters.py — no editar a mano.",
             "// Añade el PQSMod de Parallax a los cuerpos con scatters (sin él, Parallax registra",
             "// \"Celestial body X is missing the Parallax PQSMod\" y no muestra ni rocas ni máquinas).",
             "@Kopernicus:AFTER[MundosLejanos]:NEEDS[ParallaxContinued]", "{"]
    for body in PLAN:
        lvl, rad = SUBDIV[body]
        lines += [f"	@Body[{body}]", "	{", "		@PQS", "		{", "			@Mods", "			{",
                  "				Parallax", "				{", f"					subdivisionLevel = {lvl}",
                  f"					subdivisionRadius = {rad}", "					order = 999999", "				}",
                  "			}", "		}", "	}"]
    lines.append("}")
    PQS_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{PQS_OUT.relative_to(ROOT)}: PQSMod Parallax en {len(PLAN)} cuerpos")


def build():
    root = Node("ParallaxScatters")
    for body, plan in PLAN.items():
        b = Node("Body")
        b.set("name", body)
        b.set("configVersion", "2")
        for src_body, src, new, rgb, dens, only, deny, min_alt in plan:
            sc = stock_scatter(src_body, src)
            sc.set("name", f"{body}{new}")
            mat = sc.node("Material")
            mat.set("_Color", tint(mat.get("_Color"), rgb))
            dist = sc.node("Distribution")
            if dens != 1:   # las agujas de Moho tienen spawnChance 0.02: en sus biomas, que abunden
                dist.set("spawnChance", f"{min(1.0, float(dist.get('spawnChance')) * dens):g}")
            if min_alt is not None:
                dist.set("minAltitude", str(min_alt))
            names = list(BIOMES[body]) if body in BIOMES else list(BIOMES["_pequeno"])
            black = [n for n in names if n not in only] if only else list(deny or [])
            dist.remove_node("BiomeBlacklist")
            if black:
                bl = Node("BiomeBlacklist")
                for n in black:
                    bl.items.append(("v", "name", n))
                dist.items.append(("n", bl))
            b.items.append(("n", sc))
        root.items.append(("n", b))
    write_pqs_patch()
    header = ["// GENERADO por herramientas/generar_scatters.py — no editar a mano.",
              "// Requiere Parallax Continued + Parallax_StockScatterTextures (modelos y texturas).",
              "// Máquinas = agujas/racimos metálicos de Moho, solo en los biomas de las máquinas."]
    OUT.write_text("\n".join(header + root.dump()) + "\n", encoding="utf-8")
    n = sum(len(p) for p in PLAN.values())
    print(f"{OUT.relative_to(ROOT)}: {len(PLAN)} cuerpos, {n} scatters")


if __name__ == "__main__":
    build()
