"""Construye la versión instalable del pack en build/GameData/MundosLejanos (con texturas DDS).

Las fuentes (GameData/MundosLejanos) siguen en PNG: es lo que escriben los generadores y lo que pinta el artista.
Aquí se convierten a DDS con mipmaps las texturas que van a la GPU: las de ScaledVersion (texture, normals),
anillos, shader de la estrella y texturas de detalle del terreno. KSP las carga más rápido, ocupan menos memoria
y no parpadean al verse pequeñas. Se quedan en PNG los mapas que KSP lee en la CPU (alturas, biomas y
VertexColorMap, incluidos los _Color que el PQS usa a la vez): los biomas necesitan colores exactos y las alturas
no admiten pérdida.

- Fuente RGBA -> DXT5: el alfa es la máscara especular de los _Color, o la X de las normales DXT5nm.
- Fuente RGB o gris -> DXT1.
- Los DDS se guardan VOLTEADOS en vertical: KSPTextureLoader sube los datos del DDS tal cual (fila 0 abajo,
  como Unity), mientras que a los PNG los voltea Unity al cargarlos.
- En la copia de build se reescriben las rutas .png -> .dds de los .cfg. Las fuentes no se tocan.

Uso:  python herramientas/construir.py              construye (incremental: solo recodifica lo que cambió)
      python herramientas/construir.py --instalar   construye y copia a GameData de KSP (robocopy /MIR)
"""
import io
import pathlib
import re
import shutil
import struct
import subprocess
import sys

from PIL import Image

import sistema as S

ROOT = pathlib.Path(__file__).resolve().parents[1]
SRC = ROOT / "GameData" / S.PACK
OUT = ROOT / "build" / "GameData" / S.PACK
KSP = pathlib.Path(r"C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program/GameData")
GPU_KEYS = {"texture", "normals", "sunspotTex", "noiseMap", "rampMap",
            "lowTex", "midTex", "highTex", "steepTex", "lowBumpMap", "midBumpMap", "highBumpMap", "steepBumpMap"}
REF = re.compile(r"^\s*@?(\w+)\s*=\s*(" + re.escape(S.PACK) + r"/\S+?\.png)\b", re.M)


def references():
    """{ruta relativa a GameData: {claves que la usan}} en todos los .cfg de la fuente."""
    refs = {}
    for p in SRC.rglob("*.cfg"):
        for key, path in REF.findall(p.read_text(encoding="utf-8")):
            refs.setdefault(path, set()).add(key)
    return refs


def encode_dds(src, dst):
    """PNG -> DDS DXT1/DXT5 con cadena de mipmaps hasta 4 px, volteado en vertical."""
    im = Image.open(src)
    alpha = im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info
    im = im.convert("RGBA" if alpha else "RGB").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    fmt = "DXT5" if alpha else "DXT1"
    header, levels, cur = None, [], im
    while True:
        buf = io.BytesIO()
        cur.save(buf, format="DDS", pixel_format=fmt)
        data = buf.getvalue()
        header = header or bytearray(data[:128])
        levels.append(data[128:])
        if min(cur.size) <= 4:
            break
        cur = cur.resize((cur.width // 2, cur.height // 2), Image.Resampling.BOX)
    struct.pack_into("<I", header, 28, len(levels))                                   # dwMipMapCount
    struct.pack_into("<I", header, 8, struct.unpack_from("<I", header, 8)[0] | 0x20000)  # DDSD_MIPMAPCOUNT
    struct.pack_into("<I", header, 108, struct.unpack_from("<I", header, 108)[0] | 0x401008)  # COMPLEX|MIPMAP|TEXTURE
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(bytes(header) + b"".join(levels))
    return fmt, len(levels)


def build():
    refs = references()
    convert = {path for path, keys in refs.items() if keys <= GPU_KEYS}   # solo GPU: ningún uso en CPU
    wanted, encoded = set(), 0
    for src in SRC.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(SRC.parent).as_posix()                      # MundosLejanos/...
        if rel in convert:
            dst = OUT.parent / rel[:-4]
            dst = dst.with_name(dst.name + ".dds")
            wanted.add(dst)
            if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
                encode_dds(src, dst)
                encoded += 1
            continue
        dst = OUT.parent / rel
        wanted.add(dst)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.suffix == ".cfg":                                          # rutas .png -> .dds
            text = src.read_text(encoding="utf-8")
            text = REF.sub(lambda m: m.group(0)[:-4] + ".dds" if m.group(2) in convert else m.group(0), text)
            if not dst.exists() or dst.read_text(encoding="utf-8") != text:
                dst.write_text(text, encoding="utf-8")
        elif not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime or dst.stat().st_size != src.stat().st_size:
            shutil.copy2(src, dst)
    for old in [p for p in OUT.rglob("*") if p.is_file() and p not in wanted]:  # espejo: fuera lo que ya no existe
        old.unlink()

    # Comprobación: toda textura que citan los .cfg de build existe en build
    missing = []
    for p in OUT.rglob("*.cfg"):
        for path in re.findall(re.escape(S.PACK) + r"/\S+?\.(?:png|dds)\b", p.read_text(encoding="utf-8")):
            if not (OUT.parent / path).exists():
                missing.append(f"{p.name}: {path}")
    if missing:
        sys.exit("Faltan texturas en build:\n  " + "\n  ".join(missing))
    size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"{OUT.relative_to(ROOT)}: {len(convert)} texturas en DDS ({encoded} recodificadas), "
          f"{size / 2**20:.0f} MB en total")
    return OUT


def install():
    if subprocess.run(["tasklist", "/FI", "IMAGENAME eq KSP_x64.exe"], capture_output=True, text=True).stdout.count("KSP_x64"):
        print("AVISO: KSP está abierto; los cambios se verán al reiniciarlo.")
    r = subprocess.run(["robocopy", str(OUT), str(KSP / S.PACK), "/MIR", "/NJH", "/NJS", "/NDL", "/NP", "/R:1", "/W:1"],
                       capture_output=True, text=True)
    if r.returncode >= 8:
        sys.exit(f"robocopy falló ({r.returncode}):\n{r.stdout}")
    print(f"Instalado en {KSP / S.PACK}")


if __name__ == "__main__":
    build()
    if "--instalar" in sys.argv:
        install()
