# Local dev workflow: ensure venv+deps, verify the database connection, apply any pending
# migrations, then run the API with auto-reload.
# Usage: ./start_dev.ps1

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

Write-Host "=== 3/4 Testing database connection ===" -ForegroundColor Cyan
& $VenvPython scripts\check_db_connection.py
if ($LASTEXITCODE -ne 0) {
    Write-Error "Could not connect to the database. Is Postgres running? Try: docker-compose up -d"
    exit 1
}

Write-Host "=== 4/4 Applying any pending migrations ===" -ForegroundColor Cyan
& $VenvPython -m alembic upgrade head
if ($LASTEXITCODE -ne 0) { Write-Error "Migration failed."; exit 1 }

Write-Host ""
Write-Host "=== Starting API at http://127.0.0.1:8000 (Ctrl+C to stop) ===" -ForegroundColor Cyan
& $VenvPython -m uvicorn app.main:app --reload
