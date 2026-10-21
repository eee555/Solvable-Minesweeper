param(
    [Parameter(Mandatory = $true)][string]$PackageDir,
    [switch]$Apply
)

$ErrorActionPreference = 'Stop'
$package = (Resolve-Path $PackageDir).Path
$dumpbin = Get-Command dumpbin.exe -ErrorAction SilentlyContinue
if (-not $dumpbin) {
    throw 'dumpbin.exe not found. Run from the Visual Studio developer environment.'
}
$files = @(Get-ChildItem $package -Recurse -File | Where-Object Extension -In '.exe', '.dll', '.pyd')
$candidates = @{}
foreach ($file in $files) {
    if ($file.DirectoryName -eq $package -and $file.Name -match '^qt6(3d|quick3d|graphs|datavisualization|pdf|multimedia|location|positioning|remoteobjects|scxml|sensors|texttospeech|spatialaudio|quicktest|test).*\.dll$') {
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
        if ($file.DirectoryName -eq $package -and $removable.ContainsKey($file.Name.ToLowerInvariant())) { continue }
        foreach ($dependency in $imports[$file.FullName]) {
            if ($removable.ContainsKey($dependency)) {
                $removable.Remove($dependency)
                $changed = $true
            }
        }
    }
} while ($changed)
$removedBytes = 0L
foreach ($name in @($removable.Keys | Sort-Object)) {
    $file = $candidates[$name]
    $removedBytes += $file.Length
    Write-Output ('{0} {1:N2} MiB' -f $file.Name, ($file.Length / 1MB))
    if ($Apply) { Remove-Item -LiteralPath $file.FullName -Force }
}
Write-Output ('Removable Qt DLLs: {0}; size: {1:N2} MiB; applied: {2}' -f $removable.Count, ($removedBytes / 1MB), $Apply.IsPresent)