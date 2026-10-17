"""Build an Inno Setup installer using a clean, relocatable embedded Python.

Build host only: Python 3.11 x64, pip and Inno Setup 6. No end-user tools needed.
Pass --site-packages to reuse a prepared dependency directory instead of pip.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata as metadata
import json
from pathlib import Path
import shutil
import subprocess
import sys
from urllib.request import urlretrieve
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def run(*args):
    subprocess.run([str(arg) for arg in args], check=True, cwd=ROOT)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--iscc", type=Path, required=True)
    parser.add_argument("--ollama", type=Path, required=True,
                        help="Extracted official Ollama standalone distribution")
    parser.add_argument("--site-packages", type=Path)
    args = parser.parse_args()
    if sys.version_info[:2] != (3, 11):
        parser.error("Use Python 3.11 x64 to match the embedded runtime")
    stage = ROOT / "build/windows-payload"
    if stage.exists():
        parser.error("build/windows-payload already exists; move it aside before rebuilding")
    cache = ROOT / "build/downloads"
    cache.mkdir(parents=True, exist_ok=True)
    archive = cache / "python-3.11.9-embed-amd64.zip"
    if not archive.exists():
        urlretrieve("https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip", archive)
    python_dir = stage / "runtime/python"
    python_dir.mkdir(parents=True)
    with zipfile.ZipFile(archive) as package:
        package.extractall(python_dir)
    site = python_dir / "Lib/site-packages"
    if args.site_packages:
        # Reuse only the dependency environment, never its editable client code.
        shutil.copytree(args.site_packages, site, ignore=shutil.ignore_patterns(
            "__pycache__", "*.pyc", "*.pyo", "__editable__*", "qwen_local_subtitles*",
            "qwen_asr*", "direct_url.json", "*.obj", "objects-*", ".qt", "build"))
        run(sys.executable, "-m", "pip", "install", "--no-deps", "--target", site, "qwen-asr==0.0.6")
    else:
        run(sys.executable, "-m", "pip", "install", "--target", site,
            "torch==2.6.0", "torchaudio==2.6.0", "--index-url", "https://download.pytorch.org/whl/cu126")
        run(sys.executable, "-m", "pip", "install", "--target", site, "--upgrade", f"{ROOT}[setup]")
    (python_dir / "python311._pth").write_text(
        "python311.zip\n.\nLib/site-packages\n../..\nimport site\n", encoding="utf-8")
    for name in ("qwen_local_subtitles", "scripts", "licenses"):
        shutil.copytree(ROOT / name, stage / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    for name in ("launch.pyw", "models.json", "README.md", "LICENSE", "NOTICE", "THIRD_PARTY_NOTICES.md"):
        shutil.copy2(ROOT / name, stage / name)
    shutil.copytree(args.ollama, stage / "runtime/ollama",
                    ignore=shutil.ignore_patterns("ollama app.exe", "unins*", "*.log"))
    inventory = []
    license_dir = stage / "licenses/python-packages"
    for dist in metadata.distributions(path=[str(site)]):
        name = dist.metadata["Name"]
        inventory.append({"name": name, "version": dist.version,
                          "license": dist.metadata.get("License-Expression") or dist.metadata.get("License"),
                          "source": f"https://pypi.org/project/{name}/{dist.version.split('+')[0]}/"})
        for item in dist.files or []:
            if any(token in item.name.lower() for token in ("license", "copying", "notice", "copyright")):
                source = Path(dist.locate_file(item))
                if source.is_file():
                    destination = license_dir / name / str(item).replace("..", "_")
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
    (stage / "licenses/runtime-inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")
    shutil.copy2(python_dir / "LICENSE.txt", stage / "licenses/Python-LICENSE.txt")
    # Original shared libraries and all distribution license files stay in place.
    run(args.iscc, f"/DPayload={stage}", ROOT / "installer/setup.iss")
    output = ROOT / "dist/windows"
    files = sorted(output.glob("RealtimeTranslationSubtitles-1.0.0-Setup*"))
    checksums = []
    for path in files:
        digest = hashlib.file_digest(path.open("rb"), "sha256").hexdigest()
        checksums.append(f"{digest}  {path.name}")
    (output / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    print(f"Installer generated: {output}")


if __name__ == "__main__":
    main()
