@echo off
echo Starting MksU Clearance System Backend Server...
echo.

cd /d "%~dp0"

rem Optional arg: "sqlite" to force SQLite for local quick runs
if /I "%1"=="sqlite" (
	set DB_ENGINE=sqlite
	set SQLITE_DB_PATH=%~dp0db.sqlite3
	echo Using database: SQLite at %SQLITE_DB_PATH%
) else (
	if "%DB_ENGINE%"=="" set DB_ENGINE=mysql
	echo Using database engine: %DB_ENGINE% (from .env/env vars)
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Django development server on http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.
echo Available endpoints:
echo   - Health: http://127.0.0.1:8000/api/health/
echo   - API Docs: http://127.0.0.1:8000/api/docs/
echo   - Admin: http://127.0.0.1:8000/admin/
echo.

python manage.py runserver 8000
