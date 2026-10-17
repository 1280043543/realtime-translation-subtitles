param([string]$InstallRoot)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
Set-Location -LiteralPath $InstallRoot
$downloads = Join-Path $InstallRoot 'downloads'
New-Item -ItemType Directory -Force -Path $downloads | Out-Null

function Download($url, $path) {
    if (-not (Test-Path -LiteralPath $path)) {
        Write-Host "正在下载 $url"
        Invoke-WebRequest -Uri $url -OutFile $path -UseBasicParsing
    }
}

$pythonInstaller = Join-Path $downloads 'python-3.11.9-amd64.exe'
Download 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' $pythonInstaller
$pythonExe = Join-Path $env:LOCALAPPDATA 'Programs\Python\Python311\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) {
    Start-Process $pythonInstaller -ArgumentList '/quiet InstallAllUsers=0 PrependPath=0 Include_launcher=1' -Wait
}
$ollama = Join-Path $downloads 'OllamaSetup.exe'
Download 'https://ollama.com/download/OllamaSetup.exe' $ollama
$ollamaExe = Join-Path $env:LOCALAPPDATA 'Programs\Ollama\ollama.exe'
if (-not (Test-Path -LiteralPath $ollamaExe)) {
    Start-Process $ollama -ArgumentList '/silent' -Wait
}
if (-not (Test-Path -LiteralPath $pythonExe)) { throw 'Python 安装未完成。' }
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $InstallRoot 'install.ps1') -Python $pythonExe
if ($LASTEXITCODE -ne 0) { throw '项目依赖或模型安装失败。' }
