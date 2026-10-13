"""Genera los scatters de Parallax Continued del pack (rocas nativas, hielo y las máquinas de Kraken).

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

# cuerpo: [(cuerpo de origen, scatter de origen, nombre nuevo, tinte RGB, densidad×, solo_biomas, sin_biomas,
#           minAlt o (minAlt, maxAlt))]
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
        ("Tylo", "SmallSlabs", "LosasOscuras", (0.30, 0.30, 0.33), 1.0, None,
         ["Mar Ecuatorial", "Oceanos Helados", "Asentamiento Kerbal"], 2),
        ("Dres", "MedRocksVar1", "BloquesOscuros", (0.16, 0.15, 0.15), 1.0, ["Llanuras Oscuras", "Tierras Altas"], None, 2),
        ("Dres", "SmallRocksVar1", "RocasOscuras", (0.15, 0.14, 0.14), 1.0, ["Llanuras Oscuras"], None, 2),
        ("Tylo", "SmallRocksVar1", "BloquesHielo", (0.85, 0.88, 0.92), 1.0, ["Oceanos Helados", "Casquetes Polares"], None, 2),
        ("Moho", "MetalSpireWide", "MaquinaDerribada", (0.60, 0.35, 0.25), 15.0, ["Restos de la Maquina"], None, None),
        ("Moho", "SmallMetalCluster", "RestosMaquina", (0.60, 0.35, 0.25), 1.0, ["Restos de la Maquina"], None, None),
    ],
    "Salus": [
        ("Duna", "SlabsSmall", "CostrasSal", (1.40, 1.35, 1.25), 1.0, ["Arcos de Islas"], None, 2),
    ],
    "Norh": [  # basalto escarchado, coladas de lava y bloques de hielo polar
        ("Duna", "SmallRocksVar1", "RocasVolcanicas", (0.62, 0.46, 0.38), 1.0, None,
         ["Mar Ecuatorial", "Casquetes Polares"], 2),
        ("Duna", "SlabsMed", "LosasLava", (0.45, 0.35, 0.30), 1.0, ["Llanuras de Lava", "Volcanes", "Gran Volcan"], None, 2),
        ("Tylo", "SmallRocksVar1", "BloquesHielo", (1.25, 1.28, 1.32), 1.0, ["Casquetes Polares", "Tundra de Amoniaco"], None, 2),
    ],
    "Skolta": [  # todos los biomas de tierra: rocas, bloques y objetos propios de cada uno
        # rocas sueltas: costas, salinas, llanuras y dunas (arena ocre / orgánica oscura)
        ("Duna", "SmallRocksVar1", "RocasCosta", (0.80, 0.62, 0.46), 1.0, ["Costas", "Salinas", "Llanuras"], None, 2),
        ("Duna", "SmallRocksVar2", "GuijarrosOrganicos", (0.38, 0.30, 0.25), 1.0, ["Dunas"], None, 2),
        ("Duna", "MedRocksVar2", "BloquesLlanura", (0.82, 0.64, 0.44), 1.0, ["Llanuras", "Costas"], None, 2),
        # anortosita blanca de las tierras altas y montañas
        ("Tylo", "SmallRocksVar1", "RocasAnortosita", (1.30, 1.28, 1.22), 1.0, ["Tierras Altas", "Montanas"], None, 2),
        ("Tylo", "LargeRocksVar1", "BloquesAnortosita", (1.25, 1.22, 1.18), 1.0, ["Tierras Altas", "Montanas"], None, 2),
        # campos volcánicos: losas de basalto con azufre y agujas de toba
        ("Duna", "SlabsSmall", "LosasBasalto", (0.70, 0.60, 0.40), 1.0, ["Campos Volcanicos", "Llanuras"], None, 2),
        ("Dres", "Spire", "AgujasVolcanicas", (0.62, 0.50, 0.30), 1.0, ["Campos Volcanicos"], None, 2),
        # salinas: cristales de sales de amonio
        ("Pol", "MedCluster", "CristalesSal", (1.45, 1.40, 1.30), 1.0, ["Salinas"], None, 2),
        # yacimientos de cobre y níquel: rocas y vetas metálicas azules y violetas
        ("Duna", "SmallRocksVar1", "RocasCobre", (0.45, 0.60, 1.20), 1.0, ["Yacimientos Metalicos"], None, 2),
        ("Moho", "SmallMetalCluster", "VetasCobre", (0.40, 0.55, 1.25), 1.0, ["Yacimientos Metalicos"], None, 2),
        # casquetes: escarcha de amoníaco y sales
        ("Eeloo", "IceSlabsTinySlabs", "EscarchaPolar", (1.05, 1.02, 0.95), 1.0, ["Casquetes Polares"], None, 2),
    ],
    "Termos": [  # losas de basalto, costras de sílice blanca, toba y costras de azufre en los pozos ácidos
        ("Duna", "SlabsSmall", "LosasBasalto", (0.55, 0.50, 0.46), 1.0, ["Llanuras Basalticas", "Campos Volcanicos"], None, 2),
        ("Tylo", "SmallRocksVar1", "CostrasSilice", (1.30, 1.28, 1.20), 1.0, ["Orillas de Silice"], None, 2),
        ("Duna", "SmallRocksVar1", "RocasToba", (0.95, 0.85, 0.70), 1.0, ["Tierras Altas", "Montanas"], None, 2),
        ("Duna", "SlabsSmall", "CostrasAzufre", (1.30, 1.20, 0.45), 1.0, ["Pozos Acidos"], None, 2),
    ],
    "Talia": [  # regolito, bloques de eyecta y metal nativo en los afloramientos
        ("Dres", "SmallRocksVar1", "Regolito", (0.70, 0.67, 0.63), 1.0, None, ["Afloramientos Metalicos"], None),
        ("Dres", "MedRocksVar1", "BloquesEyecta", (0.75, 0.72, 0.68), 1.0,
         ["Crateres Jovenes", "Gran Cuenca", "Tierras Altas"], None, None),
        ("Moho", "SmallMetalCluster", "MetalNativo", (0.70, 0.72, 0.78), 1.0, ["Afloramientos Metalicos"], None, None),
    ],
    "Tyrna": [  # cristales de hielo y vetas metálicas en las fisuras
        ("Ike", "SmallCrystals", "CristalesHielo", (1.10, 1.12, 1.15), 1.0, None, None, None),
        ("Moho", "SmallMetalCluster", "VetasMetalicas", (0.65, 0.58, 0.50), 1.0, ["Fisuras Criovolcanicas"], None, None),
    ],
    "Akira": [  # bloques de hielo de agua, cuchillas de metano y rocas de tolinas
        ("Tylo", "SmallRocksVar1", "BloquesHielo", (1.20, 1.18, 1.25), 1.0, ["Montanas de Hielo", "Crestas de Metano"], None, None),
        ("Ike", "TallCrystals", "CuchillasMetano", (1.05, 0.98, 1.15), 1.0, ["Crestas de Metano"], None, None),
        ("Dres", "SmallRocksVar1", "RocasTolinas", (0.60, 0.40, 0.33), 1.0, ["Tierras de Tolinas"], None, None),
    ],
    "Vestigia": [
        ("Tylo", "SmallRocksVar1", "RocasVitrificadas", (0.90, 0.88, 0.86), 1.0, None, None, None),
        ("Tylo", "MedRocksVar1", "RocasVitrificadasMed", (0.90, 0.88, 0.86), 1.0, None, None, None),
    ],
    "Lumen": [  # cristales de hielo de Ike, grises de polvo
        ("Ike", "SmallCrystals", "CristalesHielo", (0.80, 0.78, 0.76), 1.0, None, None, None),
        ("Ike", "TallCrystals", "CristalesAltos", (0.80, 0.78, 0.76), 1.0, None, None, None),
        ("Tylo", "SmallRocksVar1", "BloquesHielo", (0.85, 0.83, 0.80), 1.0, None, None, None),
    ],
    # Cinturón Oscuro: rocas casi negras (albedo 0.01–0.02)
    "Fuligo": [("Dres", "SmallRocksVar1", "RocasHollin", (0.12, 0.12, 0.13), 1.0, None, None, None),
               ("Dres", "MedRocksVar1", "BloquesHollin", (0.12, 0.12, 0.13), 1.0, None, None, None)],
    "Caligo": [("Dres", "SmallRocksVar1", "RocasCarbono", (0.11, 0.10, 0.12), 1.0, None, None, None)],
    "Atra": [("Dres", "MedRocksVar1", "BloquesNegros", (0.10, 0.10, 0.10), 1.0, None, None, None)],
    # La baliza de Hollín: las máquinas estuvieron en el Cinturón Oscuro (registro en inglés en Ciencia.cfg)
    "Hollin": [("Moho", "MetalSpire", "BalizaMaquinas", MACHINE, 50.0, ["Baliza"], None, None)],
    # ---- Creus–Halum (Creus es un gigante gaseoso: sin superficie, sin scatters)
    "Halum": [  # islas de hielo a la deriva y nieve de hidrógeno sobre el mar de neón
        ("Eeloo", "IceSlabsTinySlabs", "LosasHielo", (1.00, 1.03, 1.08), 1.0, ["Islas a la Deriva", "Nieves de Hidrogeno"], None, 2),
        ("Eeloo", "IceSlabsMedSlabs", "BloquesHielo", (1.00, 1.03, 1.08), 1.0, ["Islas a la Deriva"], None, 2),
        ("Eeloo", "IceSlabsLarge", "IcebergsGrandes", (0.92, 0.98, 1.08), 2.0, ["Islas a la Deriva"], None, 2),
        ("Eeloo", "IceSlabsGiant", "IcebergsGigantes", (0.92, 0.98, 1.08), 2.0, ["Islas a la Deriva"], None, 2),
        # Hielo flotante frente a los continentes de hielo y en sus grietas: icebergs del mar frío de Kerbin, que
        # Parallax pone a nivel del mar (placementAltitude) sobre cualquier fondo de neón (altitud del terreno < 0)
        ("Kerbin", "GiantBerg", "TempanosGigantes", (0.95, 1.00, 1.08), 4.0, ["Islas a la Deriva"], None, (-3500, -5)),
        ("Kerbin", "Icebergs", "Tempanos", (0.95, 1.00, 1.08), 3.0, ["Islas a la Deriva"], None, (-3500, -5)),
        ("Kerbin", "SmallIcebergs", "TempanosMedianos", (0.95, 1.00, 1.08), 2.0, ["Islas a la Deriva"], None, (-3500, -5)),
        ("Kerbin", "TinyIcebergs", "TempanosPequenos", (0.95, 1.00, 1.08), 1.0, ["Islas a la Deriva"], None, (-3500, -5)),
    ],
    # ---- Elara
    # Titanus: formaciones propias (generar_modelos.py, en CUSTOM); aquí solo la espuma suelta entre ellas
    "Titanus": [
        ("Kerbin", "TinyIcebergs", "Espuma", (0.78, 0.66, 0.54), 1.5, ["Balsas Minerales", "Dorsales de Disolucion"], None, (-180000, -5)),
    ],
    "Ocrea": [  # lecho violeta, mantos de H2 plateados y glaciares de neón
        ("Mun", "SmallRocks", "RocasLecho", (0.62, 0.58, 0.80), 1.0, ["Lecho Desnudo", "Campos de Fumarolas"], None, None),
        ("Vall", "TinyCrystals", "EscarchaHidrogeno", (1.05, 1.03, 1.10), 1.0, ["Mantos de Hidrogeno", "Polos de Escarcha"], None, None),
        ("Vall", "IceSlabsMedSlabs", "LosasNeon", (0.85, 1.00, 1.05), 1.0, ["Glaciares de Neon"], None, None),
    ],
    "Pastora": [("Gilly", "SmallRocksVar1", "RocasHollinAnillo", (0.35, 0.35, 0.37), 1.0, None, None, None)],
    "Prima": [  # tolinas rojizas
        ("Gilly", "SmallRocksVar1", "RocasTolinas", (0.75, 0.62, 0.52), 1.0, None, None, None),
        ("Gilly", "MedRocksVar1", "BloquesTolinas", (0.75, 0.62, 0.52), 1.0, None, ["Cuello Brillante"], None),
    ],
    "Secunda": [  # hielo de agua; bloques caídos al pie del acantilado de Verona
        ("Eeloo", "IceSlabsTinySlabs", "LosasHielo", (1.08, 1.10, 1.12), 1.0, None, None, None),
        ("Eeloo", "IceSlabsMedSlabs", "BloquesVerona", (1.08, 1.10, 1.12), 3.0, ["Acantilado Verona"], None, None),
    ],
    "Heraldo": [  # costra negra; hielo fresco en los pozos activos
        ("Gilly", "SmallRocksVar1", "CostraCometa", (0.25, 0.23, 0.22), 1.0, None, ["Pozos Activos"], None),
        ("Vall", "TinyCrystals", "HieloFresco", (1.05, 1.08, 1.12), 2.0, ["Pozos Activos"], None, None),
    ],
    # ---- Kraken
    "Nox": [  # casi negra; bloques del gran impacto
        ("Gilly", "SmallRocksVar1", "RocasNegras", (0.12, 0.12, 0.13), 1.0, None, None, None),
        ("Gilly", "MedRocksVar1", "BloquesImpacto", (0.12, 0.12, 0.13), 1.5, ["Gran Crater"], None, None),
    ],
    "Azabache": [  # carbono vítreo: esquirlas que destellan en azul
        ("Bop", "SmallRocksVar1", "RocasVitreas", (0.15, 0.16, 0.20), 1.0, None, ["Facetas Vitreas"], None),
        ("Ike", "TinyCrystals", "EsquirlasVitreas", (0.20, 0.25, 0.35), 2.0, ["Facetas Vitreas"], None, None),
    ],
    "Brea": [("Gilly", "SmallRocksVar1", "GrumosOrganicos", (0.14, 0.12, 0.10), 0.3, None, ["Charcos de Brea"], None)],
    "Tizne": [  # montón de escombros: bloques por todas partes
        ("Gilly", "SmallRocksVar1", "Escombros", (0.13, 0.13, 0.13), 1.5, None, None, None),
        ("Gilly", "LargeRocksVar1", "Bloques", (0.13, 0.13, 0.13), 1.0, None, None, None),
        ("Gilly", "HugeRocksVar1", "BloquesGigantes", (0.13, 0.13, 0.13), 2.0, ["Campos de Bloques"], None, None),
    ],
    "Escoria": [  # escoria vesicular
        ("Bop", "SmallRocksVar1", "Escoria", (0.18, 0.14, 0.12), 1.0, None, None, None),
        ("Bop", "MedRocksVar1", "EscoriaMed", (0.18, 0.14, 0.12), 1.0, None, None, None),
    ],
    # ---- Sistema de Kerbol
    "Ceniza": [  # arcillas pardas; sales claras en el Monte Solitario
        ("Mun", "SmallRocks", "RocasArcilla", (0.55, 0.52, 0.48), 1.0, None, None, None),
        ("Mun", "MedRocks", "BloquesArcilla", (0.55, 0.52, 0.48), 1.0, None, ["Monte Solitario"], None),
        ("Eeloo", "SlabsSmall", "CostrasSal", (1.10, 1.08, 1.04), 2.0, ["Monte Solitario"], None, None),
    ],
    "Karmen": [  # roca gris; losas desprendidas en la cara de fractura
        ("Gilly", "SmallRocksVar1", "RocasGrises", (0.47, 0.45, 0.42), 1.0, None, None, None),
        ("Tylo", "SmallSlabs", "LosasFractura", (0.47, 0.45, 0.42), 2.0, ["Cara de Fractura"], None, None),
    ],
    "Ignea": [
        ("Dres", "SmallRocksVar1", "CostraRota", (0.35, 0.22, 0.18), 1.0, ["Costra Enfriada"], None, None),
        ("Dres", "MedRocksVar1", "BloquesCostra", (0.35, 0.22, 0.18), 1.0, ["Costra Enfriada"], None, None),
    ],
}


# Scatters con modelos propios (herramientas/generar_modelos.py). Se clona el iceberg gigante de Kerbin (shader
# biplanar, LOD y optimizaciones) y se cambian modelo, textura, tinte, escala y reparto. Flotan: el origen del modelo
# es la línea de flotación y Parallax lo pone a nivel del mar (placementAltitude 0) sobre fondos de −180 a −8 km.
# (nombre, modelo, tinte RGB, spawnChance, escala mín–máx, alcance m, LOD1/LOD2 desde m, biomas, tiling)
ROCA = f"{S.PACK}/PluginData/Titanus/Titanus_Roca.png"
CUSTOM = {
    "Titanus": [
        ("ContinentesA", "continente_a", (0.80, 0.58, 0.44), 0.0007, (1.0, 2.2), 30000, (4000, 12000),
         ["Balsas Minerales", "Jardines Quimicos"], 0.012),
        ("ContinentesB", "continente_b", (0.62, 0.46, 0.40), 0.0007, (0.8, 1.8), 30000, (4000, 12000),
         ["Balsas Minerales"], 0.012),
        ("Montanas", "montana", (0.52, 0.38, 0.34), 0.0009, (0.7, 1.5), 30000, (3000, 10000),
         ["Balsas Minerales", "Dorsales de Disolucion"], 0.015),
        ("AgujasSilice", "agujas", (1.05, 1.00, 0.92), 0.003, (0.6, 1.6), 14000, (1500, 5000),
         ["Balsas Minerales", "Dorsales de Disolucion", "Jardines Quimicos"], 0.03),
        ("ChimeneasMinerales", "chimeneas", (0.72, 0.62, 0.56), 0.0025, (0.6, 1.4), 12000, (1500, 5000),
         ["Dorsales de Disolucion", "Balsas Minerales"], 0.03),
        ("ChimeneasVivas", "chimeneas", (0.40, 0.92, 0.55), 0.005, (0.6, 1.5), 12000, (1500, 5000),
         ["Jardines Quimicos"], 0.03),
        ("ChimeneasNaranja", "chimeneas", (1.15, 0.58, 0.22), 0.004, (0.5, 1.2), 12000, (1500, 5000),
         ["Jardines Quimicos"], 0.03),
        ("BalsasEspuma", "balsa", (0.85, 0.74, 0.62), 0.01, (0.5, 1.6), 9000, (1000, 3500),
         ["Balsas Minerales", "Jardines Quimicos", "Mar Supercritico"], 0.03),
    ],
}


def custom_scatter(body, name, model, rgb, chance, scale, rng, lods, only, tiling):
    sc = stock_scatter("Kerbin", "GiantBerg")
    sc.set("name", f"{body}{name}")
    sc.set("model", f"{S.PACK}/Modelos/{body}/{model}0")
    opt = sc.node("Optimizations")
    opt.set("frustumCullingStartRange", str(min(rng, 12000)))
    opt.set("frustumCullingScreenMargin", str(-int(rng * 0.6)))       # objetos de kilómetros: no recortarlos antes de tiempo
    mat = sc.node("Material")
    mat.set("_MainTex", ROCA)
    mat.set("_Tiling", str(tiling))
    mat.set("_Color", tint("1,1,1,1", rgb))
    for k, v in (("_SpecularIntensity", "0.25"), ("_SpecularPower", "8"), ("_FresnelPower", "5"),
                 ("_EnvironmentMapFactor", "0.25"), ("_Hapke", "0.8")):   # roca porosa y mate, no hielo
        mat.set(k, v)
    dist = sc.node("Distribution")
    dist.set("seed", f"{(sum(map(ord, name)) % 997) / 997:.4f}")
    dist.set("spawnChance", f"{chance:g}")
    dist.set("range", str(rng))
    dist.set("minScale", ",".join([f"{scale[0]:g}"] * 3))
    dist.set("maxScale", ",".join([f"{scale[1]:g}"] * 3))
    dist.set("minAltitude", "-180000")
    dist.set("maxAltitude", "-5")
    dist.set("placementAltitude", "0")
    for lod, (node, start) in enumerate(zip(dist.node("LODs").nodes("LOD"), lods), start=1):
        node.set("model", f"{S.PACK}/Modelos/{body}/{model}{lod}")
        node.set("range", str(start))
    names = list(BIOMES[body])
    dist.remove_node("BiomeBlacklist")
    bl = Node("BiomeBlacklist")
    for n in names:
        if n not in only:
            bl.items.append(("v", "name", n))
    dist.items.append(("n", bl))
    return sc


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
          "Norh": (6, 600), "Skolta": (6, 600), "Termos": (6, 500), "Talia": (6, 500), "Tyrna": (6, 600),
          "Akira": (6, 600),
          "Ignea": (6, 500), "Lumen": (6, 700), "Fuligo": (6, 500), "Caligo": (6, 500), "Atra": (6, 500),
          "Hollin": (5, 350),
          "Halum": (6, 600), "Ocrea": (6, 500), "Ceniza": (6, 500), "Nox": (5, 350), "Prima": (5, 350),
          "Secunda": (5, 350), "Pastora": (5, 350), "Heraldo": (5, 350), "Azabache": (5, 350), "Brea": (5, 350),
          "Tizne": (5, 350), "Escoria": (5, 350), "Karmen": (5, 350), "Titanus": (6, 600)}
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
            if isinstance(min_alt, tuple):   # (mín, máx) de altitud del terreno: p. ej. solo bajo el mar
                dist.set("minAltitude", str(min_alt[0]))
                dist.set("maxAltitude", str(min_alt[1]))
            elif min_alt is not None:
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
        for spec in CUSTOM.get(body, []):
            b.items.append(("n", custom_scatter(body, *spec)))
        root.items.append(("n", b))
    write_pqs_patch()
    header = ["// GENERADO por herramientas/generar_scatters.py — no editar a mano.",
              "// Requiere Parallax Continued + Parallax_StockScatterTextures (modelos y texturas).",
              "// Máquinas = agujas/racimos metálicos de Moho, solo en los biomas de las máquinas.",
              "// Titanus: modelos propios en MundosLejanos/Modelos/Titanus (generar_modelos.py)."]
    OUT.write_text("\n".join(header + root.dump()) + "\n", encoding="utf-8")
    n = sum(len(p) for p in PLAN.values()) + sum(len(c) for c in CUSTOM.values())
    print(f"{OUT.relative_to(ROOT)}: {len(PLAN)} cuerpos, {n} scatters ({sum(len(c) for c in CUSTOM.values())} con modelos propios)")


if __name__ == "__main__":
    build()
