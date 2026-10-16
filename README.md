# 实时翻译字幕

Windows 桌面软件（预览版）：读取电脑正在播放的声音，在本机识别、翻译，并通过可拖动的悬浮窗口显示字幕。支持跟随耳机切换、暂停后快速继续，以及字幕字号、颜色、透明度和位置记忆。

## 使用方法

1. 安装 **64 位 Python 3.11 或 3.12**（[官网](https://www.python.org/downloads/windows/)）和 [Ollama](https://ollama.com/download/windows)。推荐 NVIDIA 显卡，CPU 也能运行但较慢。
2. 下载 [Releases](https://github.com/1280043543/realtime-translation-subtitles/releases) 中的源码安装包并完整解压；双击 **`安装.cmd`**，等待依赖和模型下载完成。首次需要联网和数 GB 下载空间。
3. 双击 **`启动.cmd`**，或使用安装时创建的“实时翻译字幕”桌面快捷方式。
4. 保持“跟随系统默认播放设备”，选择目标语言，点击“开始监听”和“开启悬浮字幕”，然后播放视频。

展开“字幕外观”可调整样式；“暂停”保留识别模型，“释放识别模型”可释放其占用的显存。模型下载后，识别和翻译在本机进行。

## 输入实例

输入是**视频正在播放的音频**，不是文本输入框。例如播放英文：

> We should discuss this face to face.

目标语言选择“简体中文”，参考字幕为：

> 我们应该面对面讨论这件事。

实际结果受发音、背景声和上下文影响。字幕存在延迟，后文到来时可能修正；当前不支持静音视频识别、读取视频缓存或独占全屏下的显示保证。

## 模型、许可与感谢

| 用途 | 所需模型 | 许可 |
| --- | --- | --- |
| 语音识别 | **[Qwen3-ASR-0.6B](https://huggingface.co/Qwen/Qwen3-ASR-0.6B)** | Apache-2.0 |
| 本地翻译 | [Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507)，Ollama 标签 `qwen3:4b-instruct-2507-q4_K_M` | Apache-2.0 |

感谢 **Alibaba / Qwen 团队开源 Qwen3-ASR** 和 Qwen3 模型，感谢 [Qwen3-ASR 项目](https://github.com/QwenLM/Qwen3-ASR)、Ollama、PySide6、PyTorch 与 SoundCard 的贡献者。本项目是独立客户端，不代表上述团队的官方产品。

客户端代码采用 [Apache-2.0](LICENSE)。源码包不包含模型权重、Python、Ollama 或第三方运行库；安装时从相应官方渠道下载。模型可依 Apache-2.0 使用和再分发，须保留许可证、归属及适用声明；详见 [第三方与模型许可说明](THIRD_PARTY_NOTICES.md)。

开发与手动安装见 [开发说明](DEVELOPMENT.md)。
