"""Compila el plugin del pack (plugin/*.cs) -> GameData/MundosLejanos/Plugins/MundosLejanos.dll

Usa el compilador Roslyn del SDK de .NET instalado y las librerías de la propia instalación de KSP
(KSP_x64_Data/Managed): no descarga nada. El plugin solo dibuja la coma y las colas de los cometas
(nodos MUNDOSLEJANOS_COMETA en los .cfg).
Uso:  python herramientas/compilar_plugin.py
"""
import glob
import pathlib
import subprocess
import sys

import sistema as S

ROOT = pathlib.Path(__file__).resolve().parents[1]
MANAGED = pathlib.Path(r"C:/Program Files (x86)/Steam/steamapps/common/Kerbal Space Program/KSP_x64_Data/Managed")
OUT = ROOT / "GameData" / S.PACK / "Plugins" / f"{S.PACK}.dll"
REFS = ["mscorlib.dll", "System.dll", "System.Core.dll", "UnityEngine.dll", "UnityEngine.CoreModule.dll",
        "UnityEngine.ParticleSystemModule.dll", "Assembly-CSharp.dll", "Assembly-CSharp-firstpass.dll"]


def csc():
    sdks = sorted(glob.glob(r"C:/Program Files/dotnet/sdk/*/Roslyn/bincore/csc.dll"))
    if not sdks:
        sys.exit("No encuentro el SDK de .NET (dotnet). Instálalo o compila plugin/*.cs con otro csc.")
    return ["dotnet", sdks[-1]]


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    refs = [f"-r:{MANAGED / r}" for r in REFS if (MANAGED / r).exists()]
    srcs = sorted(str(p) for p in (ROOT / "plugin").glob("*.cs"))
    cmd = csc() + ["-nologo", "-target:library", "-optimize+", "-nostdlib+", "-noconfig", "-langversion:7.3",
                   "-deterministic", "-warn:4", f"-out:{OUT}"] + refs + srcs
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout.strip() or "(sin avisos)")
    if r.returncode:
        sys.exit(f"Error de compilación ({r.returncode})")
    print(f"{OUT.relative_to(ROOT)}  ({OUT.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
