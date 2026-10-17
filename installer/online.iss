[Setup]
AppId={{01510D49-8462-432E-91B9-BE1D90A20126}
AppName=实时翻译字幕
AppVersion=1.0.0
AppPublisher=1280043543
AppPublisherURL=https://github.com/1280043543/realtime-translation-subtitles
DefaultDirName={localappdata}\Programs\RealtimeTranslationSubtitles
DefaultGroupName=实时翻译字幕
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.19045
WizardStyle=modern
SetupIconFile={#Source}\qwen_local_subtitles\assets\app-icon.ico
UninstallDisplayIcon={app}\qwen_local_subtitles\assets\app-icon.ico
LicenseFile={#Source}\LICENSE
OutputDir=..\dist\windows-online
OutputBaseFilename=RealtimeTranslationSubtitles-1.0.0-Online-Setup
Compression=lzma2/fast
SolidCompression=yes
PrivilegesRequiredOverridesAllowed=dialog

[Files]
Source: "{#Source}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\实时翻译字幕"; Filename: "{app}\online-install.cmd"; WorkingDir: "{app}"; IconFilename: "{app}\qwen_local_subtitles\assets\app-icon.ico"
Name: "{autodesktop}\实时翻译字幕"; Filename: "{app}\online-install.cmd"; WorkingDir: "{app}"; IconFilename: "{app}\qwen_local_subtitles\assets\app-icon.ico"

[Run]
Filename: "{app}\online-install.cmd"; WorkingDir: "{app}"; Description: "下载运行环境并完成安装"; Flags: postinstall nowait
