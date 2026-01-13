# Start MksU Clearance System Backend Server
Write-Host "Starting MksU Clearance System Backend Server..." -ForegroundColor Green
Write-Host ""

# Set environment variables
$env:DB_ENGINE = "sqlite"
$env:SQLITE_DB_PATH = "$PSScriptRoot\db.sqlite3"

# Change to BACKEND directory
Set-Location $PSScriptRoot

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Starting Django development server on http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "Available endpoints:" -ForegroundColor White
Write-Host "  - Health: http://127.0.0.1:8000/api/health/" -ForegroundColor Gray
Write-Host "  - API Docs: http://127.0.0.1:8000/api/docs/" -ForegroundColor Gray
Write-Host "  - Admin: http://127.0.0.1:8000/admin/" -ForegroundColor Gray
Write-Host ""

& python manage.py runserver 8000
