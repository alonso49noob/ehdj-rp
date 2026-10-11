"""Valida el pack sin abrir KSP. Uso:  python herramientas/validar_pack.py

Comprueba: sintaxis de los .cfg (llaves, claves), que los cuerpos coinciden con sistema.py,
que existen todas las texturas referenciadas, que los colores de bioma del .cfg están en el
mapa de biomas (y viceversa), que las curvas de atmósfera son coherentes y que las esferas
de influencia no se solapan ni chocan con el anillo/la atmósfera del padre.
"""
import math
import pathlib
import re
import sys

import numpy as np
from PIL import Image

import sistema as S
from generar_texturas import HEIGHTMAPS

ROOT = pathlib.Path(__file__).resolve().parents[1]
GAMEDATA = ROOT / "GameData"
KSP_GAMEDATA = pathlib.Path(r"C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program/GameData")
errors, warnings = [], []


class Node:
    def __init__(self, name):
        self.name, self.values, self.nodes = name, [], []

    def get(self, key, default=None):
        return next((v for k, v in self.values if k == key), default)

    def node(self, name):
        return next((n for n in self.nodes if n.name == name), None)

    def all(self, name):
        return [n for n in self.nodes if n.name == name]


def parse(path):
    root, stack, pending = Node(path.name), [], None
    stack.append(root)
    for ln, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("//", 1)[0].strip()
        while line:
            if line.startswith("{"):
                if pending is None:
                    errors.append(f"{path.name}:{ln}: '{{' sin nombre de nodo")
                n = Node(pending or "?")
                stack[-1].nodes.append(n)
                stack.append(n)
                pending, line = None, line[1:].strip()
            elif line.startswith("}"):
                if len(stack) == 1:
                    errors.append(f"{path.name}:{ln}: '}}' de más")
                else:
                    stack.pop()
                line = line[1:].strip()
            elif "=" in line and not re.match(r"^[@+$!%-]?[A-Za-z_]\w*(\[.*\])?(:\w+\[.*?\])*\s*\{", line):
                k, v = line.split("=", 1)
                if pending:
                    errors.append(f"{path.name}:{ln}: nodo '{pending}' sin '{{'")
                    pending = None
                stack[-1].values.append((k.strip(), v.strip()))
                line = ""
            else:
                m = re.match(r"^([^{}]+?)\s*(\{.*)?$", line)
                if pending:
                    errors.append(f"{path.name}:{ln}: nodo '{pending}' sin '{{'")
                pending, line = m.group(1).strip(), (m.group(2) or "").strip()
    if len(stack) != 1:
        errors.append(f"{path.name}: {len(stack) - 1} llave(s) sin cerrar")
    return root


def num(x):
    return float(str(x).split()[0])


def check_texture(path, where):
    if path.startswith("CTTP/"):
        if KSP_GAMEDATA.exists() and not (KSP_GAMEDATA / path).exists():
            errors.append(f"{where}: no existe {path} en tu GameData (¿falta CTTP?)")
        return
    if not (GAMEDATA / path).exists():
        errors.append(f"{where}: no existe la textura {path}")


def biome_check(body, props):
    bm = props.get("biomeMap")
    biomes = props.node("Biomes")
    if not bm or not biomes:
        errors.append(f"{body}: sin biomeMap/Biomes")
        return
    img = np.asarray(Image.open(GAMEDATA / bm).convert("RGB")).reshape(-1, 3)
    present = {"#%02x%02x%02x" % tuple(c) for c in np.unique(img, axis=0)}
    cfg = {b.get("color").lower(): b.get("name") for b in biomes.all("Biome")}
    for col, name in cfg.items():
        if col not in present:
            errors.append(f"{body}: el bioma '{name}' ({col}) no aparece en {bm}")
    for col in present - set(cfg):
        errors.append(f"{body}: el mapa {bm} tiene el color {col} sin bioma en el .cfg")


def atmosphere_check(body, atm):
    alt = num(atm.get("altitude"))
    keys = [list(map(float, v.split())) for k, v in atm.node("pressureCurve").values if k == "key"]
    tkeys = [list(map(float, v.split())) for k, v in atm.node("temperatureCurve").values if k == "key"]
    if keys[-1][0] != alt or keys[-1][1] != 0:
        errors.append(f"{body}: la curva de presión debe acabar en 0 a {alt} m")
    if any(b[1] >= a[1] for a, b in zip(keys, keys[1:])):
        errors.append(f"{body}: la presión no decrece de forma monótona")
    if abs(keys[0][1] - num(atm.get("staticPressureASL"))) > 1e-3:
        errors.append(f"{body}: staticPressureASL no coincide con la primera clave")
    if min(k[1] for k in tkeys) <= 0:
        errors.append(f"{body}: temperatura <= 0 K")
    A = S.ATMOS[body]
    if abs(keys[0][1] - A["p0_atm"] * S.ATM) > 1e-2:
        errors.append(f"{body}: presión superficial distinta de sistema.py (¿falta regenerar?)")
    return alt


def scatter_check(root, kop_bodies):
    """Scatters de Parallax: cuerpos existentes, modelos instalados y biomas válidos."""
    from generar_texturas import BIOMES
    n = 0
    for top in root.all("ParallaxScatters"):
        for b in top.all("Body"):
            body = b.get("name")
            if body not in kop_bodies:
                errors.append(f"Parallax: el cuerpo {body} no existe")
                continue
            valid = set(BIOMES.get(body, BIOMES["_pequeno"]))
            for sc in b.all("Scatter"):
                n += 1
                models = [sc.get("model")] + [l.get("model") for l in sc.node("Distribution").node("LODs").all("LOD")]
                for m in models:
                    if KSP_GAMEDATA.exists() and not (KSP_GAMEDATA / f"{m}.mu").exists():
                        errors.append(f"Parallax {body}/{sc.get('name')}: no existe el modelo {m}.mu")
                bl = sc.node("Distribution").node("BiomeBlacklist")
                for _, name in (bl.values if bl else []):
                    if name not in valid:
                        errors.append(f"Parallax {body}/{sc.get('name')}: bioma '{name}' no existe")
                if bl and len(bl.values) >= len(valid):
                    errors.append(f"Parallax {body}/{sc.get('name')}: la lista negra excluye todos los biomas")
    return n


def main():
    cdir = GAMEDATA / S.PACK / "Configs"
    cfgs = sorted(cdir.rglob("*.cfg"))
    bodies, roots = {}, {}
    for p in cfgs:
        key = p.relative_to(cdir).as_posix()
        roots[key] = parse(p)
        for top in roots[key].nodes:
            if top.name.startswith("@Kopernicus"):
                for b in top.all("Body"):
                    bodies[b.get("name")] = (b, key)

    missing = set(S.BODIES) - set(bodies)
    extra = set(bodies) - set(S.BODIES)
    for m in missing:
        errors.append(f"falta el cuerpo {m} en los .cfg")
    for m in extra:
        errors.append(f"cuerpo {m} en los .cfg pero no en sistema.py")

    atm_top = {}
    for name, (b, fname) in bodies.items():
        if name not in S.BODIES:
            continue
        ref = S.BODIES[name]
        star = ref.get("kind") == "star"
        where = f"{fname}:{name}"
        props, orbit = b.node("Properties"), b.node("Orbit")
        tmpl = b.node("Template").get("name")
        if tmpl != ref["template"]:
            errors.append(f"{where}: plantilla {tmpl} != {ref['template']}")
        for key, val in (("radius", ref["radius"]), ("geeASL", ref["gee"])):
            if abs(num(props.get(key)) - val) > 1e-9 * max(1, val):
                errors.append(f"{where}: {key} = {props.get(key)} pero sistema.py dice {val}")
        if ref.get("soi") and abs(num(props.get("sphereOfInfluence")) - ref["soi"]) > 1:
            errors.append(f"{where}: sphereOfInfluence distinto de sistema.py")
        o = ref["orbit"]
        if orbit.get("referenceBody") != ref["parent"]:
            errors.append(f"{where}: referenceBody {orbit.get('referenceBody')} != {ref['parent']}")
        for key, val, tol in (("semiMajorAxis", o["a"], 1e-6), ("eccentricity", o["e"], 1e-6),
                              ("inclination", o["i"], 1e-9), ("longitudeOfAscendingNode", o["lan"], 1e-9),
                              ("argumentOfPeriapsis", o["argpe"], 1e-9), ("meanAnomalyAtEpoch", o["M0"], 1e-6)):
            got = num(orbit.get(key))
            if abs(got - val) > tol * max(1, abs(val)):
                errors.append(f"{where}: {key} = {got} pero sistema.py dice {val}")

        sv = b.node("ScaledVersion")
        for k in ("texture", "normals", "noiseMap", "sunspotTex", "rampMap"):
            if sv.node("Material").get(k):
                check_texture(sv.node("Material").get(k), where)
        nrm = sv.node("Material").get("normals")
        if nrm and nrm.endswith(".png") and (GAMEDATA / nrm).exists():
            # Los shaders de KSP leen X del ALFA (DXT5nm). Un PNG RGB da X = +1: luz torcida y cuñas en los polos.
            im = Image.open(GAMEDATA / nrm)
            if im.mode != "RGBA" or np.asarray(im)[..., 0].mean() < 250:
                errors.append(f"{where}: {nrm} no está en formato DXT5nm (X en alfa, Y en verde, rojo = 255)")
        if star:
            light = sv.node("Light")
            if not light or abs(num(light.get("luminosity")) / S.KRAKEN_LUMINOSITY - 1) > 0.01:
                errors.append(f"{where}: luminosity no coincide con sistema.KRAKEN_LUMINOSITY")
        pqs = b.node("PQS")
        if pqs:
            for k, v in pqs.node("Material").values if pqs.node("Material") else []:
                if v.endswith((".dds", ".png")):
                    check_texture(v, where)
            mods = pqs.node("Mods")
            hm = mods.node("VertexHeightMap")
            check_texture(hm.get("map"), where)
            check_texture(mods.node("VertexColorMap").get("map"), where)
            exp = HEIGHTMAPS[name]
            if (num(hm.get("offset")), num(hm.get("deformity"))) != (exp["offset"], exp["deformity"]):
                errors.append(f"{where}: offset/deformity no coinciden con generar_texturas.HEIGHTMAPS")
        allowed = {"Creus": [S.RING], "Kraken": list(S.KRAKEN_DISKS.values())}.get(name, [])
        rings = b.node("Rings").all("Ring") if b.node("Rings") else []
        for ring in rings:
            check_texture(ring.get("texture"), where)
            if (num(ring.get("innerRadius")), num(ring.get("outerRadius"))) not in [(r["inner"], r["outer"]) for r in allowed]:
                errors.append(f"{where}: radios de anillo que no están en sistema.py")
        if len(rings) != len(allowed):
            errors.append(f"{where}: {len(rings)} anillos, sistema.py define {len(allowed)}")
        if not star:
            check_texture(props.get("biomeMap"), where)
            biome_check(name, props)
        atm = b.node("Atmosphere")
        if atm and name in S.ATMOS:
            atm_top[name] = atmosphere_check(name, atm)
        elif name in S.ATMOS:
            errors.append(f"{where}: falta el nodo Atmosphere")

    # ---- dinámica: SOI y espacio libre
    print(f"{'cuerpo':9s} {'SOI (m)':>12s} {'SOI/R':>8s} {'periodo':>16s}")
    for name, ref in S.BODIES.items():
        soi, R = S.soi(name), ref["radius"]
        T = S.period(name)
        tstr = (f"{T / S.KERBIN_YEAR:,.1f} años" if T > S.KERBIN_YEAR
                else f"{T / 21600:,.2f} días" if T > 21600 else f"{T / 3600:,.2f} h")
        print(f"{name:9s} {soi:12.4e} {soi / R:8.1f} {tstr:>16s}")
        if soi < 1.5 * R:
            errors.append(f"{name}: SOI ({soi:.0f} m) demasiado pequeña frente al radio ({R} m)")
        o, parent = ref["orbit"], ref["parent"]
        if parent == "Sun":
            continue
        rp, ra = o["a"] * (1 - o["e"]), o["a"] * (1 + o["e"])
        if ra + soi > S.soi(parent):
            errors.append(f"{name}: su órbita + SOI se sale de la SOI de {parent}")
        floor = S.BODIES[parent]["radius"] + atm_top.get(parent, 0)
        if parent == "Creus":
            floor = max(floor, S.RING["outer"] / 1000 * S.BODIES["Creus"]["radius"])
        if rp - soi < floor:
            errors.append(f"{name}: su SOI toca la atmósfera/anillo de {parent} (periapsis {rp:.0f} m)")
    parents = {r["parent"] for r in S.BODIES.values()} - {"Sun"}   # los cometas cruzan órbitas: no aplica
    for par in sorted(parents):
        sib = [n for n in S.BODIES if S.BODIES[n]["parent"] == par]
        for i, a in enumerate(sib):
            for b in sib[i + 1:]:
                oa, ob = S.BODIES[a]["orbit"], S.BODIES[b]["orbit"]
                same = all(abs(oa[k] - ob[k]) < 1e-6 for k in ("a", "e", "i", "lan", "argpe"))
                if same:  # misma órbita (troyanos): separación angular constante
                    dM = abs(oa["M0"] - ob["M0"]) % (2 * math.pi)
                    gap = 2 * oa["a"] * (1 - oa["e"]) * math.sin(min(dM, 2 * math.pi - dM) / 2)
                else:
                    gap = abs(oa["a"] - ob["a"]) - (oa["a"] * oa["e"] + ob["a"] * ob["e"])
                if gap < S.soi(a) + S.soi(b):
                    errors.append(f"SOI solapadas: {a} y {b} (separación mínima {gap:.3e} m)")

    # ---- textos de ciencia: cuerpo + situación (+ bioma existente)
    from generar_texturas import BIOMES
    sits = ("SrfLanded", "SrfSplashed", "FlyingLow", "FlyingHigh", "InSpaceLow", "InSpaceHigh")
    for key, root in roots.items():
        if not key.endswith("Ciencia.cfg"):
            continue
        for exp in root.nodes:
            for k, _ in exp.node("@RESULTS").values:
                m = re.match(rf"^({'|'.join(S.BODIES)})({'|'.join(sits)})(\w*)$", k)
                if not m:
                    errors.append(f"{key}: clave '{k}' no corresponde a cuerpo+situación")
                elif m.group(3):
                    valid = {n.replace(" ", "") for n in BIOMES.get(m.group(1), BIOMES["_pequeno"])}
                    if m.group(3) not in valid:
                        errors.append(f"{key}: '{k}' usa un bioma que {m.group(1)} no tiene")

    nsc = sum(scatter_check(r, bodies) for k, r in roots.items() if "Parallax" in k)
    # Parallax solo reparte scatters en cuerpos con su PQSMod (si falta: "missing the Parallax PQSMod")
    with_scatters = {b.get("name") for k, r in roots.items() if "Parallax" in k
                     for top in r.all("ParallaxScatters") for b in top.all("Body")}
    patched = {m.group(1) for k, r in roots.items() if "Parallax" in k for top in r.nodes
               for n in top.nodes for m in [re.match(r"@Body\[(\w+)\]", n.name)] if m}
    for body in sorted(with_scatters - patched):
        errors.append(f"Parallax: {body} tiene scatters pero no el PQSMod Parallax (Parallax_PQS.cfg)")

    for w in warnings:
        print("AVISO:", w)
    for e in errors:
        print("ERROR:", e)
    print(f"\n{len(cfgs)} archivos, {len(bodies)} cuerpos, {nsc} scatters, {len(errors)} errores, {len(warnings)} avisos")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
