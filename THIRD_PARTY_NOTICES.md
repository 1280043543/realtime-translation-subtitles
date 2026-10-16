# 第三方与模型许可说明

核对日期：2026-10-17。客户端源码与第三方模型、运行库分别适用各自许可证。

## 模型的分发方式

| 组件 | 官方许可依据 | 本项目的操作 |
| --- | --- | --- |
| Qwen3-ASR-0.6B | [官方模型卡](https://huggingface.co/Qwen/Qwen3-ASR-0.6B) 标注 Apache-2.0；[ASR 代码许可](https://github.com/QwenLM/Qwen3-ASR/blob/main/LICENSE) | 安装时从 Qwen 在 ModelScope 的官方模型库下载至 `.models/Qwen3-ASR-0.6B`；提供许可证全文与来源，不将权重提交 Git |
| Qwen3-4B-Instruct-2507 | [官方 LICENSE](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507/blob/main/LICENSE) 为 Apache-2.0 | 通过 Ollama 官方库下载指定 Q4_K_M 版本；保留该实际模型版本的许可文本，不重新上传权重 |

Apache-2.0 允许使用、修改和再分发（包括商业使用），条件包含提供许可证、保留适用的版权与归属声明、标明修改，以及保留原有适用 NOTICE。它不授予商标或官方背书权利。模型并非因为许可禁止分发而被排除；此处采用首次下载方式，以控制包体积并保留明确来源。

相应全文位于 `licenses/`。若后续制作含权重或第三方二进制的完整离线包，需要将实际分发版本的全部许可与通知一起附带；不能只保留客户端 LICENSE。

## 运行依赖

本次发布的是客户端源码、图标与安装脚本，不重新分发下面软件的二进制或源码。安装后的包保留它们自己的许可文件。

| 组件 | 主要许可证与来源 |
| --- | --- |
| qwen-asr、Transformers、Accelerate、ModelScope、Requests | Apache-2.0；各项目 / PyPI 包中的许可文件 |
| Ollama | [MIT](https://github.com/ollama/ollama/blob/main/LICENSE)，全文附于 `licenses/Ollama-MIT.txt`；与模型许可证不同 |
| PySide6 / Qt | [LGPLv3 / GPL / 商业许可](https://doc.qt.io/qtforpython-6/licenses.html)；本项目以独立安装的动态库方式使用，不打包锁定 Qt 库 |
| PyTorch、SoundCard、NumPy | BSD 类许可；NumPy 等二进制包还可能附带其他依赖的许可通知 |
| Python | [PSF 许可及相关声明](https://docs.python.org/3/license.html)；由用户从官网单独安装 |

本项目保留来源归属，不把第三方项目或模型宣称为自行训练或官方联合产品。感谢所有上游贡献者。
