@echo off
cd /d "%~dp0.."
py -m pip install -r backend\requirements.txt
if errorlevel 1 (
  echo Could not install advanced dependencies. Check Python and your internet connection.
  pause
  exit /b 1
)
py -m uvicorn backend.main:app --host 127.0.0.1 --port 8765
pause
