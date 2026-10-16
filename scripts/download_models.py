"""Download required models from their original providers, without redistributing weights."""
import json
from pathlib import Path

import requests
from qwen_local_subtitles.runtime import ensure_ollama

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    from modelscope import snapshot_download
    models = json.loads((ROOT / "models.json").read_text(encoding="utf-8"))
    print("下载 Qwen3-ASR-0.6B（Apache-2.0），首次需要联网和较大下载空间。", flush=True)
    snapshot_download(models["asr"]["id"], local_dir=str(ROOT / models["asr"]["local_directory"]))
    ensure_ollama(ROOT / ".local/logs")
    tag = models["translation"]["ollama_tag"]
    print(f"通过本机 Ollama 下载 {tag}（Apache-2.0）…", flush=True)
    with requests.post("http://127.0.0.1:11434/api/pull", json={"model": tag, "stream": True},
                       stream=True, timeout=(5, 300)) as response:
        response.raise_for_status()
        for line in response.iter_lines():
            if not line:
                continue
            item = json.loads(line)
            if item.get("error"):
                raise RuntimeError(item["error"])
            progress = f" {item.get('completed', 0) * 100 // item['total']}%" if item.get("total") else ""
            print("\r" + item.get("status", "") + progress + " " * 12, end="", flush=True)
    print("\n模型已就绪。后续识别和翻译在本机进行。")


if __name__ == "__main__":
    main()
