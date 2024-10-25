;由 Inno Setup Script Wizard 生成的脚本。
;有关创建 INNO SETUP 脚本文件的详细信息，请参阅文档
; 将Inno Setup 的安装目录添加到环境变量中 在命令行使用 ISCC "{xxx.iss}" 全路径 进行编译
; 或者 cd 到Inno Setup 的安装目录，然后在命令行中使用 iscc "{xxx.iss}" 进行编译
; 安装程序生成在该脚本的根目录下的Output目录下 
; 程序名称
#define MyAppName "Metaminesweeper"
; 程序版本
#define MyAppVersion "3.1.11"
; 发行商
#define MyAppPublisher "eee555"
; 官网
#define MyAppURL "https://github.com/eee555/Solvable-Minesweeper"
; 运行主程序名称
#define MyAppExeName "metaminesweeper.exe"
; 程序目录
#define AppPath "metaminesweeper"
; 根目录
#define RootPath "Metaminesweeper-v3.1.11"
; 图标
#define IconPath "Metaminesweeper-v3.1.11\media\cat.ico"
[Setup]
;注意：AppId 的值唯一标识此应用程序。不要在其他应用程序的安装程序中使用相同的 AppId 值。
;（要生成新的 GUID，请单击 Tools |在 IDE 中生成 GUID
AppId={{A5BFCE55-30E5-4A1D-8849-E6372D2CF9D4}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
;默认按照路径
DefaultDirName={autopf}\{#MyAppName}
;“ArchitecturesAllowed=x64compatible” 指定安装程序无法运行
;在 Arm 上的 x64 和 Windows 11 以外的任何设备上。
ArchitecturesAllowed=x64compatible
;“ArchitecturesInstallIn64BitMode=x64compatible” 请求
;在 x64 或 Arm 上的 Windows 11 上以“64 位模式”完成安装，
;这意味着它应该使用本机 64 位 Program Files 目录和
;注册表的 64 位视图。
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
;取消注释以下行以在非管理安装模式下运行（仅为当前用户安装）。
PrivilegesRequired=admin
OutputBaseFilename=Metaminesweeper-{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile={#IconPath}
UninstallDisplayIcon={#IconPath}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
; 中文语言包，需要下载对应的中文.isl文件放到InnoSetup目录下的languages目录下
Name: "chinese"; MessagesFile: "compiler:Languages\Chinese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkablealone

[Files]
Source: {#RootPath}\{#AppPath}\{#MyAppExeName}; DestDir: "{app}\{#AppPath}"; Flags: ignoreversion
Source: {#RootPath}\*; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
;注意：不要在任何共享系统文件上使用 “Flags： ignoreversion”

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#AppPath}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#AppPath}\{#MyAppExeName}"; Tasks: desktopicon;

[Run]
Filename: "{app}\{#AppPath}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent runascurrentuser

