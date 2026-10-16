@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1"
if errorlevel 1 (
    echo 安装失败。请查看上方提示；需要先安装 Python 3.11/3.12 和 Ollama。
    pause
    exit /b 1
)
echo 安装完成，可关闭窗口并双击“启动.cmd”。
pause
