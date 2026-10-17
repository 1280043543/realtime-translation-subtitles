# Adapted for the standalone project, 2026-10-17. See NOTICE.
"""Windowed launcher used by the installed desktop shortcut."""
from __future__ import annotations

import ctypes
import logging
import os
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / ".local" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)
if sys.stdout is None or sys.stderr is None:
    output_log = open(LOG_DIR / "output.log", "a", encoding="utf-8", buffering=1)
    sys.stdout = output_log
    sys.stderr = output_log
logging.basicConfig(
    filename=LOG_DIR / "client.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


def launch() -> None:
    os.chdir(ROOT)
    from qwen_local_subtitles.windows_shell import set_process_app_id
    set_process_app_id()
    if (ROOT / "runtime/python/pythonw.exe").is_file():
        from qwen_local_subtitles.first_run import prepare_models
        if not prepare_models(ROOT):
            return
    model_dir = ROOT / ".models" / "Qwen3-ASR-0.6B"
    if (model_dir / "config.json").is_file():
        os.environ["QWEN_ASR_MODEL"] = str(model_dir)
        os.environ["HF_HUB_OFFLINE"] = "1"
    from qwen_local_subtitles.runtime import ensure_ollama
    ensure_ollama(LOG_DIR)
    from qwen_local_subtitles.app import main
    main()


if __name__ == "__main__":
    try:
        launch()
    except Exception as exc:
        logging.exception("Client startup failed")
        ctypes.windll.user32.MessageBoxW(
            None,
            f"启动失败：{exc}\n\n日志位置：{LOG_DIR / 'client.log'}",
            "实时翻译字幕",
            0x10,
        )

