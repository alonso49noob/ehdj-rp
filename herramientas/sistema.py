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

# Órbita stock de Jool (para el troyano Norh)
JOOL_ORBIT = dict(a=68_773_560_320.0, e=0.05, i=1.304, lan=52, argpe=0, M0=0.1)

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
    # ------------------------------------------------------------------ Norh (sistema de Kerbol)
    # Troyano de Jool (L5: lo sigue 60° por detrás, mismo semieje = mismo periodo).
    # Planeta rocoso de 0.94 masas de Kerbin, 1 207 km de diámetro, 12 bar de N2/H2/NH3.
    # Banda ecuatorial de agua con amoníaco líquida a −40 °C, polos helados, volcanes y anillos de hielo.
    "Norh": dict(
        system="Kerbol", parent="Sun", radius=603_500, gee=0.9294,   # 0.94 × μ de Kerbin (3.5316e12) / R²
        template="Laythe",
        # e e i algo distintas de las de Jool: órbita muy parecida pero separada. Mismo nodo y periapsis,
        # anomalía media 60° (π/3) menor -> va siempre 60° por detrás.
        orbit=dict(a=JOOL_ORBIT["a"], e=0.065, i=2.3, lan=JOOL_ORBIT["lan"], argpe=JOOL_ORBIT["argpe"],
                   M0=(JOOL_ORBIT["M0"] - math.pi / 3) % (2 * math.pi)),
    ),
    # Skolta: "Titán cálido" entre Duna y Dres (ficha del equipo, 2026-10-11). Año de 365.25 días de 24 h,
    # 0.75 g, 650 km, 4 bar de N2 + NH3 + CH4, mar de amoníaco con hidracina (65 % de la superficie).
    "Skolta": dict(
        system="Kerbol", parent="Sun", radius=650_000, gee=0.75, template="Laythe",
        orbit=None,  # a se calcula abajo a partir del año de 365.25 días de 24 h
    ),
    "Ceniza": dict(  # luna de Skolta (propuesta de la ficha): cuerpo del cinturón capturado, arcillas amoniacadas
        system="Kerbol", parent="Skolta", radius=175_000, gee=0.10, template="Mun",
        orbit=dict(a=13_500_000, e=0.02, i=18, lan=60, argpe=0, M0=2.0),
    ),
    # ---- Termos, Tyrna, Karmen y Talia (fichas del equipo, 28-07): las fichas dan tamaños reales (Termos mide
    # 4 258 km); en KSP se dividen entre ESCALA, como Kerbin respecto a la Tierra, y se conserva la gravedad.
    # Cinturón entre Skolta y Dres: Termos es su objeto más masivo (60 % de la masa).
    "Termos": dict(  # planeta enano activo: 5 atm de N2/CO2/H2O/NH3, lagos de agua casi hirviendo, volcanes tropicales
        system="Kerbol", parent="Sun", radius=212_900, gee=0.2702, template="Laythe",   # 2.65 m/s²
        orbit=dict(a=33_500_000_000, e=0.025, i=6.5, lan=95, argpe=150, M0=4.0),     # 2.46 KAU
    ),
    "Tyrna": dict(  # luna helada con criovulcanismo y la superficie llena de metales
        system="Kerbol", parent="Termos", radius=58_600, gee=0.0673, template="Minmus",   # 0.66 m/s²
        orbit=dict(a=3_400_000, e=0.015, i=1.2, lan=30, argpe=0, M0=0.8),
    ),
    "Karmen": dict(  # luna del tamaño de un asteroide, mucho más allá de Tyrna (capturada)
        system="Kerbol", parent="Termos", radius=4_000, gee=0.003, template="Gilly",
        orbit=dict(a=21_000_000, e=0.18, i=27, lan=150, argpe=60, M0=3.5),
    ),
    # Cinturón exterior, entre Dres y Jool: Talia, segundo objeto más masivo (35 %), sin actividad y lleno de cráteres
    "Talia": dict(
        system="Kerbol", parent="Sun", radius=146_400, gee=0.1336, template="Dres",   # 1.31 m/s²
        orbit=dict(a=53_000_000_000, e=0.07, i=9, lan=200, argpe=300, M0=1.5),       # 3.9 KAU
    ),
    # Akira (ficha del equipo): mundo transneidoniano de hielos de metano y nitrógeno a 200 KAU, excepcionalmente
    # activo y con una atmósfera densa y estable. Sus 900 km de diámetro ya están a escala de KSP (la ficha lo
    # compara con Plock, de 378 km): no se dividen.
    "Akira": dict(
        system="Kerbol", parent="Sun", radius=450_000, gee=0.20, template="Duna",
        orbit=dict(a=200 * KAU, e=0.12, i=17, lan=320, argpe=110, M0=2.2),
    ),
    # ------------------------------------------------------------------ sistema Kraken
    # Enana marrón T2 (~1 250 K, ~400 Myr) a 0.2 años luz kerbales (~12 650 KAU; antes 2). 22 masas de Jool, 1.05 R_Jool.
    "Kraken": dict(
        system="Kraken", kind="star", parent="Sun", radius=6_300_000, gee=15.97, template="Sun",
        orbit=dict(a=0.2 * KLY, e=0.0, i=14, lan=300, argpe=0, M0=1.0),
    ),
    "Krax": dict(  # mundo de carbono tipo Mercurio, albedo 0.03; fundición de las máquinas
        system="Kraken", parent="Kraken", radius=260_000, gee=0.45, template="Moho",
        orbit=dict(a=28_400_000, e=0.01, i=0.5, lan=0, argpe=0, M0=0.3),
    ),
    "Scarch": dict(  # sauna de CO2/CH4 a 25 atm y 50 °C; minas de las máquinas
        system="Kraken", parent="Kraken", radius=650_000, gee=0.80, template="Eve",
        orbit=dict(a=58_000_000, e=0.02, i=1.2, lan=40, argpe=10, M0=1.7),
    ),
    "Tenebris": dict(  # mundo frío y oscuro bajo 0.2 atm de metano: océanos helados, agua líquida solo en el ecuador
        # Referencia del equipo: 2.87 m/s² (se conserva la gravedad y el diámetro actual de 1 120 km, como en KSP)
        system="Kraken", parent="Kraken", radius=560_000, gee=0.29266, template="Laythe",   # 2.87 m/s²
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
        orbit=dict(a=1_400_000, e=0.01, i=3, lan=0, argpe=0, M0=1.0),   # más cerca: la SOI de Tenebris es de 2 214 km
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

# Skolta: el año (365.25 días de 24 h) fija el semieje: a = (μ T² / 4π²)^(1/3) ≈ 30.9 Gm
SKOLTA_YEAR = 365.25 * 86_400
BODIES["Skolta"]["orbit"] = dict(a=(MU_SUN * SKOLTA_YEAR**2 / (4 * math.pi**2)) ** (1 / 3),
                                 e=0.05, i=19, lan=230, argpe=40, M0=0.7)

RING = dict(inner=1485, outer=1715)   # milésimas del radio de Creus (medido en la imagen)
NORH_RING = dict(inner=1450, outer=2050, angle=20)   # anillos de hielo de Norh (milésimas de su radio), inclinados 20°
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
    # Tenebris: 0.2 atm de metano (97 %) con trazas de N2 y Ar. Sin efecto invernadero: 3 °C en el ecuador
    # (el único sitio con agua líquida) y ~−67 °C en los polos. Con 0.29 g y un gas tan ligero la atmósfera
    # se estiraría miles de km: se corta en 1e-4 atm y sin inversión térmica (techo por debajo de la órbita de Lumen).
    "Tenebris": dict(p0_atm=0.2, T0=276.0, M=0.01652, gamma=1.31, kappa=0.20,
                     T_tropo=190.0, T_top=200.0, p_top_atm=1e-4, iso_until_atm=None,
                     lat_bias=[(0, 0.0), (12, -4.0), (25, -16.0), (45, -40.0), (90, -70.0)]),
    # Salus: N2/CO2/H2O con trazas de H2 (la serpentinización lo hizo pasar por hiceano)
    "Salus": dict(p0_atm=2.0, T0=268.0, M=0.0291, gamma=1.39, kappa=0.19,
                  T_tropo=200.0, T_top=240.0, p_top_atm=1e-6, iso_until_atm=None),
    # Norh: 45 % N2, 23 % H2, 32 % NH3 a 12 bar. M = 0.45·28.01 + 0.23·2.016 + 0.32·17.03 = 18.5 g/mol.
    # El invernadero por colisiones H2–N2 lo mantiene a −40 °C en el ecuador a 5.06 KAU de Kerbol (órbita de Jool).
    # El amoníaco satura el aire: el gradiente es suave (kappa bajo) y hay nubes de NH3.
    # lat_bias: (latitud, ΔT en K) sobre T0, que es la temperatura del ecuador; los polos rondan −75 °C.
    "Norh": dict(p0_atm=12.0 / 1.01325, T0=233.0, M=0.01852, gamma=1.36, kappa=0.20,
                 T_tropo=105.0, T_top=160.0, p_top_atm=1e-6, iso_until_atm=None,
                 lat_bias=[(0, 0.0), (20, -4.0), (35, -14.0), (55, -28.0), (90, -36.0)]),
    # Skolta: 76 % N2, 21 % NH3, 3 % CH4 a 4 bar (M = 25.4 g/mol). Ecuador a 238 K, polos a ~212 K (media ~230 K).
    # Estratosfera templada por la bruma orgánica, como en Titán.
    "Skolta": dict(p0_atm=4.0 / 1.01325, T0=238.0, M=0.02535, gamma=1.37, kappa=0.20,
                   T_tropo=140.0, T_top=175.0, p_top_atm=1e-6, iso_until_atm=None,
                   lat_bias=[(0, 0.0), (30, -4.0), (60, -16.0), (90, -26.0)]),
    # Termos: 55 % N2, 22 % CO2, 18 % H2O, 5 % NH3 a 5 atm (M = 29.2 g/mol). Ecuador a 395 K (122 °C), polos a ~368 K.
    # A 5 atm el agua hierve a 152 °C: los lagos, calentados desde abajo, rondan los 140 °C en los trópicos volcánicos.
    # scale: el cuerpo es la ficha ÷ ESCALA; se integra el Termos real (radio × 10, misma g) y las alturas se
    # dividen igual que el radio (~45 km de atmósfera en vez de ~450).
    "Termos": dict(p0_atm=5.0, T0=395.0, M=0.02918, gamma=1.33, kappa=0.20,
                   T_tropo=215.0, T_top=250.0, p_top_atm=1e-6, iso_until_atm=None,
                   lat_bias=[(0, 0.0), (25, -2.0), (50, -12.0), (90, -27.0)], scale=10),
    # Akira: 92 % N2, 5 % CH4, 3 % CO a 1.2 atm (M = 27.4 g/mol), 62 K en el ecuador y ~56 K en los polos.
    # A 62 K el hielo de N2 solo sostendría ~0.09 bar: la atmósfera "sorprendentemente densa y estable" de la ficha
    # la mantienen los criovolcanes. Troposfera casi isoterma; estratosfera templada por el metano, como en Plutón.
    # Con 0.2 g la atmósfera es muy alta: techo en 1e-5 atm (~165 km, 0.37 radios).
    "Akira": dict(p0_atm=1.2, T0=62.0, M=0.02741, gamma=1.40, kappa=0.10,
                  T_tropo=55.0, T_top=80.0, p_top_atm=1e-5, iso_until_atm=None,
                  lat_bias=[(0, 0.0), (45, -2.0), (90, -6.0)]),
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
