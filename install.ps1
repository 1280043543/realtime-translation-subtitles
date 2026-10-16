param(
    [string]$Python = '',
    [switch]$Cpu
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot

if (-not $Python -and (Get-Command py -ErrorAction SilentlyContinue)) {
    foreach ($version in @('-3.12', '-3.11')) {
        try {
            $candidate = & py $version -c 'import sys; print(sys.executable)' 2>$null
            if ($LASTEXITCODE -eq 0) { $Python = $candidate; break }
        } catch { continue }
    }
}
if (-not $Python) {
    foreach ($version in @('Python312', 'Python311')) {
        $candidate = Join-Path $env:LOCALAPPDATA "Programs\Python\$version\python.exe"
        if (Test-Path -LiteralPath $candidate) { $Python = $candidate; break }
    }
}
if (-not $Python) { throw 'Please install 64-bit Python 3.11 / 3.12, or run install.ps1 -Python <python.exe path>.' }
& $Python -c 'import sys,struct; sys.exit(0 if (3,11) <= sys.version_info[:2] < (3,13) and struct.calcsize("P")==8 else 1)'
if ($LASTEXITCODE -ne 0) { throw '64-bit Python 3.11 or 3.12 is required.' }

Write-Host 'Creating local Python environment...'
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    & $Python -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Unable to create the Python environment.' }
}
$venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
& $venvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw 'Unable to update pip.' }
$torchIndex = 'https://download.pytorch.org/whl/cpu'
if (-not $Cpu -and (Get-Command nvidia-smi -ErrorAction SilentlyContinue)) {
    & nvidia-smi --query-gpu=name --format=csv,noheader
    if ($LASTEXITCODE -eq 0) { $torchIndex = 'https://download.pytorch.org/whl/cu126' }
}
& $venvPython -m pip install torch==2.6.0 torchaudio==2.6.0 --index-url $torchIndex
if ($LASTEXITCODE -ne 0) { throw 'Unable to install PyTorch; check your network and NVIDIA driver.' }
& $venvPython -m pip install -e '.[setup]'
if ($LASTEXITCODE -ne 0) { throw 'Unable to install the desktop dependencies.' }
& $venvPython scripts\download_models.py
if ($LASTEXITCODE -ne 0) { throw 'Model download failed; rerun installation to resume.' }
& (Join-Path $PSScriptRoot 'create-shortcuts.ps1')
Write-Host 'Installation complete. Use the desktop shortcut or the start script.'
