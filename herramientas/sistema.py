"""Parámetros de los sistemas Creus–Halum y Kraken (fuente única de verdad).

Los .cfg de Kopernicus repiten estos números a mano; `validar_pack.py` comprueba
que coincidan y `generar_atmosferas.py` / `generar_texturas.py` los usan.
"""
import math

G0 = 9.80665
KAU = 13_599_840_256.0            # semieje mayor de Kerbin (m)
MU_SUN = 1.1723328e18             # parámetro gravitatorio de Kerbol
KERBIN_YEAR = 9_203_544.6         # s
ATM = 101.325                     # kPa
KLY = 63_241.077 * KAU            # año luz kerbal: 63 241 KAU = 8.60e14 m

PACK = "MundosLejanos"
TEX = f"{PACK}/PluginData"        # ruta de texturas relativa a GameData

# --------------------------------------------------------------------------
# Cuerpos. radius (m), gee (g), orbit: a (m), e, i (deg), lan, argpe, M0 (rad)
# --------------------------------------------------------------------------
BODIES = {
    "Creus": dict(
        system="CreusHalum", parent="Sun", radius=2_100_000, gee=0.80, template="Jool",
        orbit=dict(a=800 * KAU, e=0.03, i=3.1, lan=47, argpe=120, M0=2.1),
    ),
    "Halum": dict(
        system="CreusHalum", parent="Creus", radius=690_000, gee=0.55, template="Eve",
        orbit=dict(a=5 * KAU, e=0.04, i=2.5, lan=110, argpe=30, M0=0.9),
    ),
    "Ocrea": dict(  # luna capturada retrógrada cubierta de hidrógeno y neón sólidos (~6 K)
        system="CreusHalum", parent="Creus", radius=380_000, gee=0.18, template="Vall",
        orbit=dict(a=22_000_000, e=0.05, i=152, lan=20, argpe=40, M0=0.0),
    ),
    "Pastora": dict(  # luna pastora del anillo (borde exterior)
        system="CreusHalum", parent="Creus", radius=10_000, gee=0.03, template="Gilly", soi=40_000,
        orbit=dict(a=3_700_000, e=0.0005, i=0, lan=0, argpe=0, M0=1.3),
    ),
    "Prima": dict(  # troyano L4 de Halum (+60°)
        system="CreusHalum", parent="Creus", radius=28_000, gee=0.012, template="Gilly",
        orbit=dict(a=5 * KAU, e=0.04, i=2.5, lan=110, argpe=30, M0=0.9 + math.pi / 3),
    ),
    "Secunda": dict(  # troyano L5 de Halum (−60°)
        system="CreusHalum", parent="Creus", radius=18_000, gee=0.009, template="Gilly",
        orbit=dict(a=5 * KAU, e=0.04, i=2.5, lan=110, argpe=30,
                   M0=(0.9 - math.pi / 3) % (2 * math.pi)),
    ),
    "Heraldo": dict(  # cometa de periodo largo: afelio en la región de Creus
        system="CreusHalum", parent="Sun", radius=5_000, gee=0.002, template="Gilly",
        orbit=None,  # se calcula abajo
    ),
    # ------------------------------------------------------------------ sistema Kraken
    # Enana marrón T2 (~1 250 K, ~400 Myr) a 2 años luz kerbales. 22 masas de Jool, 1.05 R_Jool.
    "Kraken": dict(
        system="Kraken", kind="star", parent="Sun", radius=6_300_000, gee=15.97, template="Sun",
        orbit=dict(a=2 * KLY, e=0.0, i=14, lan=300, argpe=0, M0=1.0),
    ),
    "Krax": dict(  # mundo de carbono tipo Mercurio, albedo 0.03; fundición de las máquinas
        system="Kraken", parent="Kraken", radius=260_000, gee=0.45, template="Moho",
        orbit=dict(a=28_400_000, e=0.01, i=0.5, lan=0, argpe=0, M0=0.3),
    ),
    "Scarch": dict(  # sauna de CO2/CH4 a 25 atm y 50 °C; minas de las máquinas
        system="Kraken", parent="Kraken", radius=650_000, gee=0.80, template="Eve",
        orbit=dict(a=58_000_000, e=0.02, i=1.2, lan=40, argpe=10, M0=1.7),
    ),
    "Tenebris": dict(  # mundo oscuro (basalto) a 5 °C con agua líquida: inhabitable, pero fácil de colonizar
        system="Kraken", parent="Kraken", radius=560_000, gee=0.85, template="Laythe",
        orbit=dict(a=76_000_000, e=0.015, i=0.8, lan=80, argpe=60, M0=3.1),
    ),
    "Salus": dict(  # océano hipersalino casi global (97 %), inundado por impactos
        system="Kraken", parent="Kraken", radius=750_000, gee=1.00, template="Laythe",
        orbit=dict(a=95_000_000, e=0.03, i=1.6, lan=150, argpe=100, M0=4.4),
    ),
    "Vestigia": dict(  # luna de Salus, nacida del gran impacto; cae en espiral hacia él
        system="Kraken", parent="Salus", radius=120_000, gee=0.12, template="Ike",
        orbit=dict(a=3_000_000, e=0.01, i=4, lan=0, argpe=0, M0=0.5),
    ),
    "Nox": dict(  # segunda luna de Salus: objeto del Cinturón Oscuro capturado (retrógrada, casi negra)
        system="Kraken", parent="Salus", radius=35_000, gee=0.02, template="Gilly",
        orbit=dict(a=4_600_000, e=0.08, i=160, lan=50, argpe=0, M0=2.0),
    ),
    "Lumen": dict(  # luna de hielo sucio de Tenebris: alumbra su cara nocturna eterna
        system="Kraken", parent="Tenebris", radius=90_000, gee=0.08, template="Minmus",
        orbit=dict(a=2_200_000, e=0.01, i=3, lan=0, argpe=0, M0=1.0),
    ),
    "Ignea": dict(  # protoplaneta con océano de magma dentro del disco protoplanetario
        system="Kraken", parent="Kraken", radius=180_000, gee=0.15, template="Dres",
        orbit=dict(a=250_000_000, e=0.06, i=3, lan=200, argpe=0, M0=5.0),
    ),
    # ---- Cinturón Oscuro (450 000–820 000 km): albedo 0.01–0.02, más negro que Krax
    "Fuligo": dict(system="Kraken", parent="Kraken", radius=140_000, gee=0.07, template="Dres",
                   orbit=dict(a=520_000_000, e=0.015, i=4.0, lan=30, argpe=50, M0=0.5)),
    "Caligo": dict(system="Kraken", parent="Kraken", radius=95_000, gee=0.05, template="Bop",
                   orbit=dict(a=605_000_000, e=0.02, i=7.5, lan=140, argpe=200, M0=2.4)),
    "Atra": dict(system="Kraken", parent="Kraken", radius=70_000, gee=0.04, template="Bop",
                 orbit=dict(a=690_000_000, e=0.02, i=2.2, lan=260, argpe=90, M0=4.1)),
    "Azabache": dict(system="Kraken", parent="Kraken", radius=12_000, gee=0.008, template="Gilly",
                     orbit=dict(a=480_000_000, e=0.02, i=9, lan=80, argpe=10, M0=1.1)),
    "Brea": dict(system="Kraken", parent="Kraken", radius=8_000, gee=0.006, template="Gilly",
                 orbit=dict(a=560_000_000, e=0.02, i=3, lan=200, argpe=120, M0=3.3)),
    "Tizne": dict(system="Kraken", parent="Kraken", radius=6_000, gee=0.005, template="Gilly",
                  orbit=dict(a=645_000_000, e=0.015, i=12, lan=320, argpe=300, M0=5.2)),
    "Escoria": dict(system="Kraken", parent="Kraken", radius=10_000, gee=0.007, template="Gilly",
                    orbit=dict(a=735_000_000, e=0.015, i=6, lan=20, argpe=240, M0=0.2)),
    "Hollin": dict(system="Kraken", parent="Kraken", radius=4_000, gee=0.003, template="Gilly",
                   orbit=dict(a=780_000_000, e=0.01, i=1.5, lan=170, argpe=30, M0=2.9)),
}

# Cometa: perihelio 4.2 KAU, afelio 800 KAU, paso por el perihelio en el año 4
_rp, _ra = 4.2 * KAU, 800 * KAU
_a = (_rp + _ra) / 2
_n = math.sqrt(MU_SUN / _a**3)
BODIES["Heraldo"]["orbit"] = dict(
    a=_a, e=(_ra - _rp) / (_ra + _rp), i=28, lan=210, argpe=75,
    M0=(-_n * 3 * KERBIN_YEAR) % (2 * math.pi),
)

RING = dict(inner=1485, outer=1715)   # milésimas del radio de Creus (medido en la imagen)
# Discos de Kraken (milésimas de su radio). Todos sin iluminación y sin desvanecimiento, visibles en el mapa.
def _disk(inner_km, outer_km):
    return dict(inner=round(inner_km * 1e3 / 6_300_000 * 1000), outer=round(outer_km * 1e3 / 6_300_000 * 1000))


KRAKEN_DISKS = {
    "Interior": _disk(36_000, 50_000),             # polvo caliente entre Krax y Scarch
    "Protoplanetario": _disk(150_000, 400_000),    # disco principal; hueco en la órbita de Ignea
    "CinturonOscuro": _disk(450_000, 820_000),     # polvo del Cinturón Oscuro: apenas visible
}
# Luz de Kraken: Kopernicus usa W/m² a 1 KAU (Kerbol = 1360). L = 4πR²σT⁴ = 6.9e19 W
KRAKEN_TEFF = 1250.0
KRAKEN_LUMINOSITY = 4 * math.pi * 6_300_000**2 * 5.670374e-8 * KRAKEN_TEFF**4 / (4 * math.pi * KAU**2)

# --------------------------------------------------------------------------
# Atmósferas: perfil T(p) por tramos -> integración hidrostática
#   adiabat: T = T0 (p/p0)^kappa hasta T_tropo; luego T sube lineal en log p
# --------------------------------------------------------------------------
ATMOS = {
    "Creus": dict(p0_atm=10.0, T0=116.0, M=0.0029, gamma=1.43, kappa=0.30,
                  T_tropo=35.0, T_top=75.0, p_top_atm=1e-6, iso_until_atm=None),
    "Halum": dict(p0_atm=7.0, T0=32.0, M=0.0035, gamma=1.62, kappa=0.25,
                  T_tropo=19.0, T_top=35.0, p_top_atm=1e-6, iso_until_atm=1e-3),
    # Scarch: 90 % CO2 + 10 % CH4; estratosfera templada por la neblina orgánica
    "Scarch": dict(p0_atm=25.0, T0=323.0, M=0.0412, gamma=1.29, kappa=0.16,
                   T_tropo=200.0, T_top=240.0, p_top_atm=1e-6, iso_until_atm=None),
    # Tenebris: 80 % N2, 18 % CO2, 2 % Ar — sin oxígeno libre: irrespirable, pero suave (1.3 atm, 5 °C)
    "Tenebris": dict(p0_atm=1.3, T0=278.0, M=0.0311, gamma=1.37, kappa=0.19,
                     T_tropo=210.0, T_top=250.0, p_top_atm=1e-6, iso_until_atm=None),
    # Salus: N2/CO2/H2O con trazas de H2 (la serpentinización lo hizo pasar por hiceano)
    "Salus": dict(p0_atm=2.0, T0=268.0, M=0.0291, gamma=1.39, kappa=0.19,
                  T_tropo=200.0, T_top=240.0, p_top_atm=1e-6, iso_until_atm=None),
}


def mu(name):
    b = BODIES[name]
    return b["gee"] * G0 * b["radius"] ** 2


def mu_parent(name):
    p = BODIES[name]["parent"]
    return MU_SUN if p == "Sun" else mu(p)


def laplace_soi(name):
    b = BODIES[name]
    return b["orbit"]["a"] * (mu(name) / mu_parent(name)) ** 0.4


def soi(name):
    return BODIES[name].get("soi") or laplace_soi(name)


def period(name):
    return 2 * math.pi * math.sqrt(BODIES[name]["orbit"]["a"] ** 3 / mu_parent(name))
