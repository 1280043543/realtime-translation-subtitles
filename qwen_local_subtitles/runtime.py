"""Shared local Ollama startup for installation and the desktop launcher."""
from pathlib import Path
import os
import shutil
import subprocess
import time
from urllib.request import urlopen


def ensure_ollama(log_dir: Path) -> None:
    try:
        with urlopen("http://127.0.0.1:11434/api/tags", timeout=2):
            return
    except OSError:
        pass
    bundled = Path(__file__).resolve().parent.parent / "runtime/ollama/ollama.exe"
    executable = str(bundled) if bundled.is_file() else shutil.which("ollama")
    if not executable:
        candidate = Path(os.environ.get("LOCALAPPDATA", "")) / "Programs/Ollama/ollama.exe"
        if candidate.is_file():
            executable = str(candidate)
    if not executable:
        raise RuntimeError("请先从 https://ollama.com/download/windows 安装 Ollama。")
    log_dir.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    if bundled.is_file():
        environment["OLLAMA_MODELS"] = str(bundled.parents[2] / ".models/ollama")
        environment["OLLAMA_HOST"] = "127.0.0.1:11434"
    with (log_dir / "ollama.log").open("a", encoding="utf-8") as log:
        subprocess.Popen([executable, "serve"], stdout=log, stderr=log,
                         env=environment, creationflags=subprocess.CREATE_NO_WINDOW)
    for _ in range(40):
        time.sleep(0.25)
        try:
            with urlopen("http://127.0.0.1:11434/api/tags", timeout=1):
                return
        except OSError:
            continue
    raise RuntimeError("本地 Ollama 服务启动超时，请稍后重试。")
