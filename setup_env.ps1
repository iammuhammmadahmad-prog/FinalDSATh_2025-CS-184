# setup_env.ps1 - builds ONE virtual environment at the project root.
# Every folder under apps/ (and modules/, dsa_lib/) uses this same interpreter,
# so a library installed once is visible everywhere.
#
# Run from the project root (PowerShell):
#   powershell -ExecutionPolicy Bypass -File .\setup_env.ps1
#
# Switches:
#   -FromGlobal   Freeze the libraries already installed in your GLOBAL Python
#                 into requirements.txt first (use this if you installed
#                 libraries with a plain "pip install" outside a venv).
#   -Recreate     Delete and rebuild .venv from scratch.

param(
    [switch]$FromGlobal,
    [switch]$Recreate
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$Venv = Join-Path $Root ".venv"
$Py   = Join-Path $Venv "Scripts\python.exe"
$Req  = Join-Path $Root "requirements.txt"

# 1. Optionally capture what is installed globally (must run BEFORE the venv is active).
if ($FromGlobal -or -not (Test-Path $Req) -or ((Get-Item $Req).Length -eq 0)) {
    Write-Host "Freezing global Python packages into requirements.txt ..."
    python -m pip freeze | Set-Content $Req -Encoding ascii
    Write-Host "Review requirements.txt and delete anything you do not need."
}


# 2. Create the single root venv.
if ($Recreate -and (Test-Path $Venv)) { Remove-Item $Venv -Recurse -Force }
if (-not (Test-Path $Py)) {
    Write-Host "Creating .venv ..."
    python -m venv $Venv
}

# 3. Install libraries into it.
& $Py -m pip install --upgrade pip
if ((Test-Path $Req) -and ((Get-Item $Req).Length -gt 0)) {
    & $Py -m pip install -r $Req
} else {
    Write-Host "requirements.txt is empty - nothing to install."
}

# 4. Make the project root and every folder under apps/ importable from anywhere.
$Site = & $Py -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"
$Paths = @($Root)
$AppsDir = Join-Path $Root "apps"
if (Test-Path $AppsDir) {
    $Paths += $AppsDir
    $Paths += (Get-ChildItem $AppsDir -Directory | ForEach-Object { $_.FullName })
}
foreach ($extra in @("modules", "dsa_lib")) {
    $p = Join-Path $Root $extra
    if (Test-Path $p) { $Paths += $p }
}
$Paths | Set-Content (Join-Path $Site "project_paths.pth") -Encoding ascii
Write-Host "Registered import paths:"
$Paths | ForEach-Object { Write-Host "  $_" }

# 5. Sanity check.
& $Py -c "import sys; print('Interpreter:', sys.executable)"
& $Py -m pip list

Write-Host ""
Write-Host "Done. Activate with:  .\.venv\Scripts\Activate.ps1"
Write-Host "Then run the app with: python manage.py runserver"
