"""First-run model preparation for the self-contained Windows installer."""
from __future__ import annotations

from pathlib import Path
import sys

from PySide6.QtCore import QProcess
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QDialog, QLabel, QMessageBox, QProgressBar,
    QPushButton, QPlainTextEdit, QVBoxLayout,
)

def prepare_models(root: Path) -> bool:
    global _app
    app = _app = QApplication.instance() or QApplication(sys.argv)
    app.setWindowIcon(QIcon(str(root / "qwen_local_subtitles/assets/app-icon.ico")))
    app.setQuitOnLastWindowClosed(False)
    window = ModelSetup(root)
    ready = window.exec() == QDialog.DialogCode.Accepted
    app.setQuitOnLastWindowClosed(True)
    return ready


class ModelSetup(QDialog):
    def __init__(self, root: Path):
        super().__init__()
        self.root = root
        self.setWindowTitle("实时翻译字幕 · 模型准备")
        self.resize(620, 420)
        layout = QVBoxLayout(self)
        self.label = QLabel("首次使用需要联网下载识别和翻译模型（数 GB）。\n下载完成后可离线使用；中断后可重新打开继续准备。")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        self.progress = QProgressBar()
        self.progress.setRange(0, 1)
        layout.addWidget(self.progress)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setMaximumBlockCount(500)
        layout.addWidget(self.output)
        self.button = QPushButton("下载模型并启动")
        layout.addWidget(self.button)
        self.button.clicked.connect(self.start)
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.finished.connect(self.finished)
        self.process.errorOccurred.connect(self.failed_to_start)

    def showEvent(self, event):
        super().showEvent(event)
        if (self.root / ".local/models-ready.json").is_file():
            from PySide6.QtCore import QTimer
            QTimer.singleShot(0, self.start)

    def start(self):
        self.button.setEnabled(False)
        self.progress.setRange(0, 0)
        self.label.setText("正在检查模型并准备运行环境，请稍候…")
        self.process.start(str(self.root / "runtime/python/python.exe"),
                           ["-u", str(self.root / "scripts/download_models.py")])

    def read_output(self):
        text = bytes(self.process.readAllStandardOutput()).decode("utf-8", errors="replace")
        self.output.appendPlainText(text.replace("\r", "\n").strip())

    def failed_to_start(self, error):
        if error == QProcess.ProcessError.FailedToStart:
            self.label.setText("模型准备程序无法启动，请重新安装软件。")
            self.button.setEnabled(True)
            self.progress.setRange(0, 1)

    def finished(self, code, status):
        self.read_output()
        if code == 0 and status == QProcess.ExitStatus.NormalExit:
            self.accept()
            return
        self.progress.setRange(0, 1)
        self.label.setText("模型准备未完成，请检查网络或磁盘空间后重试。下载详情见下方。")
        self.button.setText("重试")
        self.button.setEnabled(True)

    def reject(self):
        if self.process.state() != QProcess.ProcessState.NotRunning:
            answer = QMessageBox.question(self, "退出模型准备", "停止本次准备并退出？下次打开可以重试。")
            if answer != QMessageBox.StandardButton.Yes:
                return
            self.process.kill()
            self.process.waitForFinished(3000)
        super().reject()
