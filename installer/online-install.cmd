@echo off
title 实时翻译字幕 - 在线安装
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0online-install.ps1" -InstallRoot "%~dp0"
if errorlevel 1 pause
