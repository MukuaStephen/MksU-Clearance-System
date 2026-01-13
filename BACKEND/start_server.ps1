param(
	[switch]$UseSQLite
)

# Start MksU Clearance System Backend Server
Write-Host "Starting MksU Clearance System Backend Server..." -ForegroundColor Green
Write-Host ""

# Change to BACKEND directory
Set-Location $PSScriptRoot

# Configure database engine
if ($UseSQLite) {
	$env:DB_ENGINE = "sqlite"
	$env:SQLITE_DB_PATH = "$PSScriptRoot\db.sqlite3"
	Write-Host "Using database: SQLite ($env:SQLITE_DB_PATH)" -ForegroundColor Yellow
} else {
	if (-not $env:DB_ENGINE) { $env:DB_ENGINE = "mysql" }
	Write-Host "Using database engine: $($env:DB_ENGINE) (configured via .env/env vars)" -ForegroundColor Yellow
}

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
