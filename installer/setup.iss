#ifndef Payload
  #error Payload must point to the prepared application directory
#endif
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
SetupIconFile={#Payload}\qwen_local_subtitles\assets\app-icon.ico
UninstallDisplayIcon={app}\qwen_local_subtitles\assets\app-icon.ico
LicenseFile={#Payload}\LICENSE
OutputDir=..\dist\windows
OutputBaseFilename=RealtimeTranslationSubtitles-1.0.0-Setup
Compression=lzma2/fast
SolidCompression=yes
DiskSpanning=yes
DiskSliceSize=500000000
SlicesPerDisk=1
CloseApplications=yes
AppMutex=RealtimeTranslationSubtitlesSetup

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "{#Payload}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\实时翻译字幕"; Filename: "{app}\runtime\python\pythonw.exe"; Parameters: """{app}\launch.pyw"""; WorkingDir: "{app}"; IconFilename: "{app}\qwen_local_subtitles\assets\app-icon.ico"; AppUserModelID: "RealtimeTranslationSubtitles.Desktop"
Name: "{autodesktop}\实时翻译字幕"; Filename: "{app}\runtime\python\pythonw.exe"; Parameters: """{app}\launch.pyw"""; WorkingDir: "{app}"; IconFilename: "{app}\qwen_local_subtitles\assets\app-icon.ico"; AppUserModelID: "RealtimeTranslationSubtitles.Desktop"

[Run]
Filename: "{app}\runtime\python\pythonw.exe"; Parameters: """{app}\launch.pyw"""; WorkingDir: "{app}"; Description: "启动实时翻译字幕 / Start"; Flags: nowait postinstall skipifsilent
