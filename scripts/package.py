"""Build a source installation ZIP using a distribution allowlist."""
from pathlib import Path
import hashlib
import zipfile

ROOT = Path(__file__).resolve().parent.parent
FILES = ["README.md", "DEVELOPMENT.md", "THIRD_PARTY_NOTICES.md", "LICENSE", "NOTICE",
         "pyproject.toml", "MANIFEST.in", "models.json", "launch.pyw", "install.ps1",
         "create-shortcuts.ps1", "安装.cmd", "启动.cmd", ".gitignore", ".gitattributes"]
FOLDERS = ["qwen_local_subtitles", "scripts", "tests", "licenses", "design"]


def distribution_files(root: Path) -> list[Path]:
    paths = [root / name for name in FILES]
    for folder in FOLDERS:
        paths.extend(p for p in (root / folder).rglob("*") if p.is_file()
                     and "__pycache__" not in p.parts and p.suffix not in {".pyc", ".pyo"})
    return sorted(paths)


def main() -> None:
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    archive = output / "realtime-translation-subtitles-v0.1.0-source.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
        for path in distribution_files(ROOT):
            package.write(path, arcname="实时翻译字幕/" + path.relative_to(ROOT).as_posix())
    artifacts = [archive] + sorted(output.glob("*.whl"))
    checksums = [f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}" for path in artifacts]
    (output / "SHA256SUMS.txt").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    print(archive)
    print("\n".join(checksums))


if __name__ == "__main__":
    main()
