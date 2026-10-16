# 开发与手动安装

## 目录

- `qwen_local_subtitles/`：界面、系统音频采集、识别与翻译、任务栏身份、图标。
- `launch.pyw`：无控制台的桌面启动入口。
- `install.ps1`、`安装.cmd`、`启动.cmd`：Windows 安装、启动入口。
- `create-shortcuts.ps1`：创建桌面 / 开始菜单快捷方式。
- `scripts/download_models.py`：首次下载模型；`models.json` 记录模型来源。
- `scripts/package.py`：只打包分发文件，排除本机环境、权重、日志与 Git 数据。
- `tests/`：客户端回归检查；`licenses/` 与 `NOTICE`：许可和来源。

需要 Python 3.11 / 3.12（64 位），Ollama。安装脚本优先使用 NVIDIA CUDA 12.6 版 PyTorch；无 NVIDIA 设备时使用 CPU 版。可用 `install.ps1 -Cpu` 强制 CPU 版。

## 手动安装

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
# NVIDIA CUDA 版；CPU 版将 cu126 改成 cpu。
.\.venv\Scripts\python.exe -m pip install torch==2.6.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cu126
.\.venv\Scripts\python.exe -m pip install -e ".[setup]"
.\.venv\Scripts\python.exe scripts\download_models.py
.\create-shortcuts.ps1
```

随后双击 `启动.cmd` 或桌面快捷方式。`launch.pyw` 会优先使用项目内已下载的 ASR 模型，并确保本机 Ollama 服务可连接。日志位于 `.local/logs/`，用户偏好保存在 Windows 的 QSettings 存储中。

## 检查与打包

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts\package.py
# 可选：构建标准 Python wheel / sdist
.\.venv\Scripts\python.exe -m pip install build
.\.venv\Scripts\python.exe -m build
```

`dist/` 中的 ZIP 是**源码安装包**，不是内含 Python、依赖和模型的独立 EXE。首次安装需要联网；用户音频和字幕不上传到模型服务商。

原始客户端来自用户的 Qwen3-ASR fork，来源提交和本次独立化修改记录见 `NOTICE`。本项目不内嵌上游 ASR 训练代码，通过官方 `qwen-asr` 包提供识别能力。
