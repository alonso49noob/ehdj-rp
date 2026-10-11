"""Genera las curvas de presión/temperatura de Creus y Halum y las inyecta en los .cfg.

Integra el equilibrio hidrostático dh = -(R T / (M g(h))) d(ln p) con g(h) = g0 (R/(R+h))^2
sobre el perfil T(p) definido en sistema.ATMOS, y escribe el bloque entre los marcadores
    // >>> ATMOSFERA GENERADA
    // <<< ATMOSFERA GENERADA
de GameData/MundosLejanos/Configs/<Cuerpo>.cfg. Uso:  python herramientas/generar_atmosferas.py
"""
import math
import pathlib
import re

import sistema as S

RGAS = 8.314462618
ROOT = pathlib.Path(__file__).resolve().parents[1]
CFG_DIR = ROOT / "GameData" / S.PACK / "Configs"
BEGIN, END = "// >>> ATMOSFERA GENERADA", "// <<< ATMOSFERA GENERADA"


def temperature(p, A):
    p0 = A["p0_atm"]
    p_tropo = p0 * (A["T_tropo"] / A["T0"]) ** (1 / A["kappa"])
    if p >= p_tropo:
        return A["T0"] * (p / p0) ** A["kappa"]
    p_start = p_tropo
    if A["iso_until_atm"]:
        if p >= A["iso_until_atm"]:
            return A["T_tropo"]
        p_start = A["iso_until_atm"]
    f = math.log(p_start / p) / math.log(p_start / A["p_top_atm"])
    return A["T_tropo"] + f * (A["T_top"] - A["T_tropo"])


def profile(name, steps=20000):
    """Devuelve listas (h, p_atm, T) desde la superficie hasta p_top."""
    A, B = S.ATMOS[name], S.BODIES[name]
    R, g0 = B["radius"], B["gee"] * S.G0
    s0, s1 = math.log(A["p0_atm"]), math.log(A["p_top_atm"])
    ds = (s1 - s0) / steps
    h, out = 0.0, []
    for k in range(steps + 1):
        p = math.exp(s0 + k * ds)
        T = temperature(p, A)
        out.append((h, p, T))
        g = g0 * (R / (R + h)) ** 2
        h += -(RGAS * T / (A["M"] * g)) * ds
    return out


def interp(prof, h):
    for (h0, p0, T0), (h1, p1, T1) in zip(prof, prof[1:]):
        if h0 <= h <= h1:
            f = (h - h0) / (h1 - h0)
            return math.exp(math.log(p0) + f * math.log(p1 / p0)), T0 + f * (T1 - T0)
    return prof[-1][1], prof[-1][2]


def build(name):
    A, B = S.ATMOS[name], S.BODIES[name]
    R, g0, M = B["radius"], B["gee"] * S.G0, A["M"]
    prof = profile(name)
    top = math.ceil(prof[-1][0] / 1000) * 1000
    # claves cada 0.75 de ln p (≈ 0.75 alturas de escala), redondeadas a 100 m
    alts, s = [0.0], math.log(A["p0_atm"])
    while True:
        s -= 0.75
        if s <= math.log(A["p_top_atm"]) + 0.5:
            break
        h = next(hh for hh, pp, _ in prof if pp <= math.exp(s))
        alts.append(round(h / 100) * 100)
    alts = sorted(set(alts))

    pk, tk = [], []
    for h in alts:
        p, T = interp(prof, h)
        g = g0 * (R / (R + h)) ** 2
        dpdh = -p * S.ATM * M * g / (RGAS * T)            # kPa/m, derivada exacta
        dh = 50.0
        dTdh = (interp(prof, h + dh)[1] - interp(prof, max(h - dh, 0))[1]) / (h + dh - max(h - dh, 0))
        pk.append((h, p * S.ATM, dpdh))
        tk.append((h, T, dTdh))
    pk.append((top, 0.0, 0.0))
    tk.append((top, A["T_top"], 0.0))

    f = lambda x: f"{x:.6g}"
    L = [BEGIN + " (herramientas/generar_atmosferas.py; no editar a mano)",
         f"altitude = {top}",
         f"staticPressureASL = {f(A['p0_atm'] * S.ATM)}",
         f"temperatureSeaLevel = {f(A['T0'])}",
         f"atmosphereMolarMass = {A['M']}",
         f"adiabaticIndex = {A['gamma']}",
         "pressureCurveIsNormalized = false",
         "pressureCurve", "{"]
    L += [f"\tkey = {f(h)} {f(p)} {f(d)} {f(d)}" for h, p, d in pk]
    L += ["}", "temperatureCurveIsNormalized = false", "temperatureCurve", "{"]
    L += [f"\tkey = {f(h)} {f(T)} {f(d)} {f(d)}" for h, T, d in tk]
    L += ["}"]
    # Sin variación por Sol/latitud: a 800 KAU la luz de Kerbol es despreciable
    for curve, x1 in (("temperatureSunMultCurve", top), ("temperatureLatitudeBiasCurve", 90),
                      ("temperatureLatitudeSunMultCurve", 90), ("temperatureAxialSunBiasCurve", 1),
                      ("temperatureAxialSunMultCurve", 1), ("temperatureEccentricityBiasCurve", 1)):
        L += [curve, "{", "\tkey = 0 0 0 0", f"\tkey = {x1} 0 0 0", "}"]
    L.append(END)

    rho0 = A["p0_atm"] * S.ATM * 1000 * M / (RGAS * A["T0"])
    stats = dict(top=top, keys=len(pk), rho0=rho0,
                 sound0=math.sqrt(A["gamma"] * RGAS * A["T0"] / M))
    return L, stats


def inject(name, lines):
    path = next(CFG_DIR.rglob(f"{name}.cfg"))
    text = path.read_text(encoding="utf-8")
    m = re.search(rf"^([ \t]*){re.escape(BEGIN)}.*?{re.escape(END)}[^\n]*", text, re.S | re.M)
    if not m:
        raise SystemExit(f"{path}: no encuentro los marcadores de atmósfera")
    ind = m.group(1)
    block = "\n".join(ind + ln if ln else ln for ln in lines)
    path.write_text(text[:m.start()] + block + text[m.end():], encoding="utf-8")


if __name__ == "__main__":
    for body in S.ATMOS:
        lines, st = build(body)
        inject(body, lines)
        print(f"{body}: techo {st['top']/1000:.0f} km, {st['keys']} claves, "
              f"densidad superficie {st['rho0']:.2f} kg/m3, v_sonido {st['sound0']:.0f} m/s")
