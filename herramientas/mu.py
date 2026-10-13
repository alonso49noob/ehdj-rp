"""Lectura y escritura de modelos .mu de KSP, en el formato mínimo de los scatters de Parallax.

Los modelos de Parallax_StockScatterTextures (p. ej. Models/Laythe/iceberg0.mu) solo llevan una malla:
    int 76543 (MODEL_BINARY), int 5 (versión), string nombre
    transform: string nombre, posición (3 f), rotación (4 f, cuaternión), escala (3 f)
    24 (TAG_AND_LAYER): string "Untagged", int capa 0
    7 (MESH_FILTER), 13 (MESH_START): int nº de vértices, int nº de submallas (1)
        14 vértices (3 f), 15 UV (2 f), 17 normales (3 f), 18 tangentes (4 f), 19 triángulos (int n + n índices)
    22 (MESH_END) y fin del archivo: Parallax pone su propio material, así que no hay renderer ni materiales.
Las cadenas llevan la longitud en 7 bits por byte (BinaryWriter de .NET). Coordenadas de Unity: Y arriba, levógiro;
un triángulo (a, b, c) mira hacia donde apunta cross(b − a, c − a), como en los modelos stock.
Unity usa índices de 16 bits por defecto: cada malla debe tener menos de 65 536 vértices.
"""
import struct

import numpy as np

MAGIC, VERSION = 76543, 5
TAG, MESH_FILTER, MESH_START = 24, 7, 13
VERTS, UV, NORMALS, TANGENTS, TRIS, MESH_END = 14, 15, 17, 18, 19, 22


def _string(s):
    data = s.encode("utf-8")
    n, out = len(data), bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        out.append(byte | (0x80 if n else 0))
        if not n:
            return bytes(out) + data


def tangents(v, n, uv, tri):
    """Tangentes por vértice (xyz + w = ±1) a partir de las UV, como las calcula Unity."""
    t = np.zeros_like(v)
    b = np.zeros_like(v)
    p0, p1, p2 = v[tri[:, 0]], v[tri[:, 1]], v[tri[:, 2]]
    w0, w1, w2 = uv[tri[:, 0]], uv[tri[:, 1]], uv[tri[:, 2]]
    e1, e2 = p1 - p0, p2 - p0
    d1, d2 = w1 - w0, w2 - w0
    r = d1[:, 0] * d2[:, 1] - d2[:, 0] * d1[:, 1]
    r = np.where(np.abs(r) < 1e-12, 1e-12, r)[:, None]
    sdir = (e1 * d2[:, 1:2] - e2 * d1[:, 1:2]) / r
    tdir = (e2 * d1[:, 0:1] - e1 * d2[:, 0:1]) / r
    for k in range(3):
        np.add.at(t, tri[:, k], sdir)
        np.add.at(b, tri[:, k], tdir)
    t = t - n * np.sum(n * t, axis=1, keepdims=True)              # Gram-Schmidt
    bad = np.linalg.norm(t, axis=1) < 1e-9
    t[bad] = np.cross(n[bad], [0.0, 1.0, 0.3])                     # UV degeneradas: cualquier perpendicular
    t /= np.linalg.norm(t, axis=1, keepdims=True)
    w = np.where(np.sum(np.cross(n, t) * b, axis=1) < 0, -1.0, 1.0)
    return np.hstack([t, w[:, None]]).astype(np.float32)


def write(path, name, v, n, uv, tri):
    v, n, uv = (np.ascontiguousarray(a, np.float32) for a in (v, n, uv))
    tri = np.ascontiguousarray(tri, np.int32)
    nv = len(v)
    if nv >= 65536:
        raise ValueError(f"{name}: {nv} vértices (máximo 65 535 con índices de 16 bits)")
    if tri.min() < 0 or tri.max() >= nv:
        raise ValueError(f"{name}: índices fuera de rango")
    tan = tangents(v, n, uv, tri)
    out = [struct.pack("<ii", MAGIC, VERSION), _string(name),
           _string(name), struct.pack("<10f", 0, 0, 0, 0, 0, 0, 1, 1, 1, 1),
           struct.pack("<i", TAG), _string("Untagged"), struct.pack("<i", 0),
           struct.pack("<iiii", MESH_FILTER, MESH_START, nv, 1),
           struct.pack("<i", VERTS), v.tobytes(), struct.pack("<i", UV), uv.tobytes(),
           struct.pack("<i", NORMALS), n.tobytes(), struct.pack("<i", TANGENTS), tan.tobytes(),
           struct.pack("<ii", TRIS, tri.size), tri.tobytes(), struct.pack("<i", MESH_END)]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"".join(out))


def read(path):
    """Lee un .mu de una sola malla (el formato de arriba). Devuelve dict con v, uv, n, t, tri; lanza si no encaja."""
    b = path.read_bytes()
    o = 0

    def i32():
        nonlocal o
        o += 4
        return struct.unpack_from("<i", b, o - 4)[0]

    def string():
        nonlocal o
        n = shift = 0
        while True:
            c = b[o]
            o += 1
            n |= (c & 0x7F) << shift
            shift += 7
            if not c & 0x80:
                break
        o += n
        return b[o - n:o].decode("utf-8")

    def arr(dtype, count):
        nonlocal o
        a = np.frombuffer(b, dtype, count, o)
        o += a.nbytes
        return a

    if (i32(), i32()) != (MAGIC, VERSION):
        raise ValueError("no es un .mu de versión 5")
    string()
    string()
    o += 40
    if i32() != TAG:
        raise ValueError("falta TAG_AND_LAYER")
    string()
    i32()
    if (i32(), i32()) != (MESH_FILTER, MESH_START):
        raise ValueError("falta la malla")
    nv, nsub = i32(), i32()
    d = {}
    while True:
        t = i32()
        if t == VERTS:
            d["v"] = arr(np.float32, 3 * nv).reshape(-1, 3)
        elif t == UV:
            d["uv"] = arr(np.float32, 2 * nv).reshape(-1, 2)
        elif t == NORMALS:
            d["n"] = arr(np.float32, 3 * nv).reshape(-1, 3)
        elif t == TANGENTS:
            d["t"] = arr(np.float32, 4 * nv).reshape(-1, 4)
        elif t == TRIS:
            d["tri"] = arr(np.int32, i32()).reshape(-1, 3)
        elif t == MESH_END:
            break
        else:
            raise ValueError(f"entrada desconocida {t}")
    if o != len(b):
        raise ValueError(f"{len(b) - o} bytes de más al final")
    return d
