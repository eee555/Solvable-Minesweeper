param(
    [Parameter(Mandatory = $true)][string]$PackageDir,
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$package = (Resolve-Path $PackageDir).Path
$qtRuntime = $package
$qmlRoot = Join-Path $package 'PySide6\qml'
if (Test-Path -LiteralPath (Join-Path $package '_internal\PySide6')) {
    $qtRuntime = Join-Path $package '_internal\PySide6'
    $qmlRoot = Join-Path $qtRuntime 'qml'
}
$dumpbin = Get-Command dumpbin.exe -ErrorAction SilentlyContinue
if (-not $dumpbin) {
    throw 'dumpbin.exe not found. Run from the Visual Studio developer environment.'
}
$unusedModules = @('QtQuick3D', 'Qt3D', 'QtGraphs', 'QtDataVisualization', 'QtLocation', 'QtMultimedia', 'QtPositioning', 'QtTest', 'QtTextToSpeech', 'QtSensors', 'QtRemoteObjects', 'QtScxml', 'QtWebEngine', 'QtWebChannel', 'QtWebSockets', 'QtWebView')
$unusedDirectories = @($unusedModules | ForEach-Object {
    $directory = Join-Path $qmlRoot $_
    if (Test-Path -LiteralPath $directory -PathType Container) { $directory }
})
$excludedFiles = @{}
foreach ($directory in $unusedDirectories) {
    Get-ChildItem -LiteralPath $directory -Recurse -File | ForEach-Object { $excludedFiles[$_.FullName] = $true }
}
$files = @(Get-ChildItem $package -Recurse -File | Where-Object {
    $_.Extension -in '.exe', '.dll', '.pyd' -and -not $excludedFiles.ContainsKey($_.FullName)
})
$candidates = @{}
foreach ($file in $files) {
    if ($file.DirectoryName -eq $qtRuntime -and $file.Name -match '^qt6(3d|quick3d|graphs|datavisualization|pdf|multimedia|location|positioning|remoteobjects|scxml|sensors|texttospeech|spatialaudio|quicktest|test|webengine|webchannel|websockets|webview).*\.dll$') {
        $candidates[$file.Name.ToLowerInvariant()] = $file
    }
}
$imports = @{}
foreach ($file in $files) {
    $output = & $dumpbin.Source /NOLOGO /DEPENDENTS $file.FullName 2>&1
    if ($LASTEXITCODE -ne 0) { throw "Cannot inspect $($file.FullName): $output" }
    $imports[$file.FullName] = @($output | ForEach-Object {
            if ($_ -match '^\s+([\w.\-]+\.dll)\s*$') { $Matches[1].ToLowerInvariant() }
        })
}
$removable = @{}
foreach ($name in $candidates.Keys) { $removable[$name] = $true }
do {
    $changed = $false
    foreach ($file in $files) {
        if ($file.DirectoryName -eq $qtRuntime -and $removable.ContainsKey($file.Name.ToLowerInvariant())) { continue }
        foreach ($dependency in $imports[$file.FullName]) {
            if ($removable.ContainsKey($dependency)) {
                $removable.Remove($dependency)
                $changed = $true
            }
        }
    }
} while ($changed)
$removedBytes = 0L
foreach ($directory in $unusedDirectories) {
    $removedBytes += (Get-ChildItem -LiteralPath $directory -Recurse -File | Measure-Object Length -Sum).Sum
    Write-Output ('Unused QML module: {0}' -f $directory)
    if ($Apply) { Remove-Item -LiteralPath $directory -Recurse -Force }
}
foreach ($name in @($removable.Keys | Sort-Object)) {
    $file = $candidates[$name]
    $removedBytes += $file.Length
    Write-Output ('{0} {1:N2} MiB' -f $file.Name, ($file.Length / 1MB))
    if ($Apply) { Remove-Item -LiteralPath $file.FullName -Force }
}
Write-Output ('Removable Qt DLLs: {0}; QML modules: {1}; total size: {2:N2} MiB; applied: {3}' -f $removable.Count, $unusedDirectories.Count, ($removedBytes / 1MB), $Apply.IsPresent)