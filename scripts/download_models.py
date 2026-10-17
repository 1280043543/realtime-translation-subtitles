"""Download required models from their original providers, without redistributing weights."""
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

import requests
from qwen_local_subtitles.runtime import ensure_ollama

def main() -> None:
    models = json.loads((ROOT / "models.json").read_text(encoding="utf-8"))
    marker = ROOT / ".local/models-ready.json"
    model_dir = ROOT / models["asr"]["local_directory"]
    ready = marker.is_file() and marker.read_text(encoding="utf-8") == json.dumps(models)
    if not ready or not (model_dir / "config.json").is_file() or not list(model_dir.glob("*.safetensors")):
        from modelscope import snapshot_download
        print("下载 Qwen3-ASR-0.6B（Apache-2.0），首次需要联网和较大下载空间。", flush=True)
        snapshot_download(models["asr"]["id"], local_dir=str(model_dir))
    ensure_ollama(ROOT / ".local/logs")
    tag = models["translation"]["ollama_tag"]
    response = requests.get("http://127.0.0.1:11434/api/tags", timeout=(5, 30))
    response.raise_for_status()
    if any(item.get("name") == tag for item in response.json().get("models", [])):
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text(json.dumps(models), encoding="utf-8")
        print("本地模型已就绪，正在启动字幕软件。", flush=True)
        return
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
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps(models), encoding="utf-8")


if __name__ == "__main__":
    main()
