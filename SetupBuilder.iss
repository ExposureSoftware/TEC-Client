; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Centurion Client"
#define MyAppVersion "0.6"
#define MyAppPublisher "Exposure Software"
#define MyAppURL "https://github.com/ExposureSoftware/TEC-Client"
#define MyAppExeName "Centurion Client.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{0AABC3EC-82D6-4CFE-A8CD-E6CA4371AE3C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=D:\Marshall\Documents\Code\Python Code\TEC Client\dist
OutputBaseFilename=CenturionSetup-{#MyAppVersion}
SetupIconFile=D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\resources\images\centurion.ico
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\Centurion Client.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\config.ini"; DestDir: "{localappdata}\{#MyAppPublisher}\{#MyAppName}"; Flags: ignoreversion
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\resources\images\*"; DestDir: "{localappdata}\{#MyAppPublisher}\{#MyAppName}\resources\images"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\resources\notes\*"; DestDir: "{localappdata}\{#MyAppPublisher}\{#MyAppName}\resources\notes"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\plugins\*"; DestDir: "{app}\plugins"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\plugins\plugin_config.json"; DestDir: "{localappdata}\{#MyAppPublisher}\{#MyAppName}"; Flags: ignoreversion
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\tcl\*"; DestDir: "{app}\tcl"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\tk\*"; DestDir: "{app}\tk"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\Marshall\Documents\Code\Python Code\TEC Client\build\exe.win-amd64-3.3\*"; DestDir: "{app}"; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Dirs]
Name: "{localappdata}\{#MyAppPublisher}\{#MyAppName}\Logs"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
