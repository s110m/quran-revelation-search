$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $projectRoot

$buildPython = Join-Path $projectRoot ".build-venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $buildPython)) {
    py -3.13 -m venv .build-venv
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create the isolated Python build environment."
    }
}

& $buildPython -m pip install --disable-pip-version-check -r requirements-build.txt
if ($LASTEXITCODE -ne 0) {
    throw "Could not install the build dependencies."
}

$oldOneFileExecutable = Join-Path $projectRoot "dist\QuranSearch.exe"
if (Test-Path -LiteralPath $oldOneFileExecutable) {
    Remove-Item -LiteralPath $oldOneFileExecutable -Force
}

& $buildPython -m PyInstaller --noconfirm --clean QuranSearch.spec
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller could not build the Windows application."
}

$portableDirectory = Join-Path $projectRoot "dist\QuranSearch"
$executable = Join-Path $portableDirectory "QuranSearch.exe"
$archive = Join-Path $projectRoot "dist\QuranSearch-Windows.zip"

if (-not (Test-Path -LiteralPath $executable)) {
    throw "The executable was not created at $executable"
}

if (Test-Path -LiteralPath $archive) {
    Remove-Item -LiteralPath $archive -Force
}

$archiveCreated = $false
for ($attempt = 1; $attempt -le 3; $attempt++) {
    try {
        Compress-Archive -Path $portableDirectory -DestinationPath $archive -CompressionLevel Optimal
        $archiveCreated = $true
        break
    }
    catch {
        if (Test-Path -LiteralPath $archive) {
            Remove-Item -LiteralPath $archive -Force
        }
        if ($attempt -eq 3) {
            throw
        }
        Start-Sleep -Seconds 2
    }
}

if (-not $archiveCreated) {
    throw "The portable ZIP archive could not be created."
}

Write-Host "Windows application and portable ZIP created successfully:"
Write-Host $executable
Write-Host $archive
