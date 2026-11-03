$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
New-Item -ItemType Directory -Path evidence -Force | Out-Null
$source = Join-Path $PSScriptRoot 'public\index.html'
$html = [System.IO.File]::ReadAllText($source)
if ($html.Contains('v1.0')) { $html = $html.Replace('v1.0', 'v1.1') }
elseif ($html.Contains('v1.1')) { $html = $html.Replace('v1.1', 'v1.0') }
else { throw 'Version label was not found.' }
[System.IO.File]::WriteAllText($source, $html, [System.Text.UTF8Encoding]::new($false))
& docker build --progress=plain -t intercity-lab8:1.1 . 2>&1 | Tee-Object -FilePath evidence\build-cache.txt
if ($LASTEXITCODE -ne 0) { throw 'Docker build failed. Check the output above.' }
Write-Host 'Look for CACHED at package COPY / npm ci / server.js COPY. public COPY should rebuild.'
