# Sets up the venv, installs dependencies, verifies the app builds/boots, and runs the full test suite.
# Usage: ./run_checks.ps1

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$VenvPython = Join-Path $Root ".venv\Scripts\python.exe"

Write-Host "=== 1/4 Setting up virtual environment ===" -ForegroundColor Cyan
if (-not (Test-Path $VenvPython)) {
    python -m venv .venv
}

Write-Host "=== 2/4 Installing dependencies ===" -ForegroundColor Cyan
& $VenvPython -m pip install --upgrade pip -q
& $VenvPython -m pip install -r requirements-dev.txt -q
if ($LASTEXITCODE -ne 0) { Write-Error "Dependency installation failed."; exit 1 }

Write-Host "=== 3/4 Verifying the app builds and boots ===" -ForegroundColor Cyan
& $VenvPython -c "from app.main import app; print('Import OK:', app.title)"
if ($LASTEXITCODE -ne 0) { Write-Error "App failed to import."; exit 1 }

$proc = Start-Process -FilePath $VenvPython `
    -ArgumentList "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8099" `
    -PassThru -WindowStyle Hidden

try {
    $healthy = $false
    for ($i = 0; $i -lt 10; $i++) {
        Start-Sleep -Seconds 1
        try {
            $response = Invoke-WebRequest -Uri "http://127.0.0.1:8099/health" -UseBasicParsing -TimeoutSec 2
            if ($response.StatusCode -eq 200) {
                $healthy = $true
                Write-Host "App boot check passed: $($response.Content)"
                break
            }
        } catch {
            # server likely still starting up; retry
        }
    }
    if (-not $healthy) {
        throw "App did not respond healthily on /health within the timeout."
    }
} finally {
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
}

Write-Host "=== 4/4 Running test suite ===" -ForegroundColor Cyan
& $VenvPython -m pytest -q
$testExit = $LASTEXITCODE

Write-Host ""
if ($testExit -eq 0) {
    Write-Host "ALL CHECKS PASSED" -ForegroundColor Green
} else {
    Write-Host "TESTS FAILED" -ForegroundColor Red
}
exit $testExit
