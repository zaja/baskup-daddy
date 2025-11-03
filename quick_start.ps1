# Backup Daddy - Quick Start (PowerShell)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Backup Daddy - Quick Start" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host ""
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Run the application
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Green
Write-Host ""
python main.py

Read-Host -Prompt "Press Enter to exit"
