@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel% equ 0 (
  start "" "http://localhost:8000"
  py -3 -m http.server 8000
) else (
  where python >nul 2>nul
  if %errorlevel% equ 0 (
    start "" "http://localhost:8000"
    python -m http.server 8000
  ) else (
    echo Python 3 is required. Install Python or run with another static web server.
    pause
  )
)
