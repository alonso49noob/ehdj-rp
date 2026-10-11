"""Empaqueta el pack para los playtesters: <Descargas>/ehdj_rp-v<versión>.zip

La próxima versión está en VERSION (raíz del proyecto). Cada zip creado sube el último número
(0.0.120 -> 0.0.121). Antes de empaquetar pasa validar_pack.py: si hay errores, no crea nada.

Contenido: build/GameData/MundosLejanos (la versión con DDS que hace construir.py), LEEME_PLAYTEST.md
(con la versión en el título) y capturas/.
Uso:  python herramientas/empaquetar.py
"""
import os
import pathlib
import re
import subprocess
import sys
import winreg
import zipfile

import construir
import sistema as S

ROOT = pathlib.Path(__file__).resolve().parents[1]
VERSION = ROOT / "VERSION"
CAPTURAS = {"docs/preview_sistema.png": "capturas/creus_halum.png",
            "docs/kraken/preview_kraken.png": "capturas/kraken.png"}


def descargas():
    """Carpeta de Descargas real (puede estar redirigida a otra unidad, p. ej. D:\\Descargas)."""
    try:
        key = r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key) as k:
            ruta, _ = winreg.QueryValueEx(k, "{374DE290-123F-4565-9164-39C4925E467B}")
        return pathlib.Path(os.path.expandvars(ruta))
    except OSError:
        return pathlib.Path.home() / "Downloads"


def main():
    version = VERSION.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"VERSION no válida: {version!r}")
    if subprocess.run([sys.executable, str(ROOT / "herramientas" / "validar_pack.py")]).returncode:
        sys.exit("El validador encontró errores: no se empaqueta.")

    build = construir.build()                                   # PNG -> DDS en build/GameData/MundosLejanos
    out = descargas() / f"ehdj_rp-v{version}.zip"
    if out.exists():
        sys.exit(f"Ya existe {out}: sube VERSION o bórralo antes.")
    leeme = (ROOT / "LEEME_PLAYTEST.md").read_text(encoding="utf-8")
    leeme = re.sub(r"^# Mundos Lejanos — versión de prueba.*$", f"# Mundos Lejanos — versión de prueba v{version}",
                   leeme, count=1, flags=re.M)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for f in sorted(build.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(build.parents[1]).as_posix())     # GameData/MundosLejanos/...
        z.writestr("LEEME_PLAYTEST.md", leeme)
        for src, dst in CAPTURAS.items():
            if (ROOT / src).exists():
                z.write(ROOT / src, dst)
    with zipfile.ZipFile(out) as z:
        if z.testzip() is not None:
            out.unlink()
            sys.exit("El zip salió corrupto: borrado.")
        n = len(z.namelist())

    a, b, c = map(int, version.split("."))
    VERSION.write_text(f"{a}.{b}.{c + 1}\n", encoding="utf-8")
    print(f"{out}  ({n} archivos, {out.stat().st_size / 2**20:.1f} MB). Próxima versión: {a}.{b}.{c + 1}")


if __name__ == "__main__":
    main()
