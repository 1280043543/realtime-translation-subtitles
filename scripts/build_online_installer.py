from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parent.parent
STAGE = ROOT / 'build/online-payload'
if STAGE.exists():
    shutil.rmtree(STAGE)
STAGE.mkdir(parents=True)
for name in ('qwen_local_subtitles', 'scripts', 'licenses'):
    shutil.copytree(ROOT / name, STAGE / name,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'build_windows.py'))
for name in ('README.md', 'DEVELOPMENT.md', 'THIRD_PARTY_NOTICES.md', 'LICENSE', 'NOTICE',
             'models.json', 'pyproject.toml', 'MANIFEST.in', 'install.ps1', 'create-shortcuts.ps1',
             ):
    shutil.copy2(ROOT / name, STAGE / name)
shutil.copy2(ROOT / 'installer/online-install.ps1', STAGE / 'online-install.ps1')
shutil.copy2(ROOT / 'installer/online-install.cmd', STAGE / 'online-install.cmd')
subprocess.run([str(ROOT / 'build/tools/inno/ISCC.exe'), f'/DSource={STAGE}', str(ROOT / 'installer/online.iss')], check=True)
print(ROOT / 'dist/windows-online/RealtimeTranslationSubtitles-0.2.0-Online-Setup.exe')
