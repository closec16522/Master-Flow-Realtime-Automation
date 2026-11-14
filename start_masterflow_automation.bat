@echo off
setlocal
set ANDROID_ADB_SERVER_PORT=5038

echo ============================================================
echo   Master Flow Realtime Automation Suite (Auto-Supervisor)
echo ============================================================
echo.

echo [*] Starting MasterFlow Supervisor Watchdog...
start "MasterFlow Supervisor" /min "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" "C:\SmartHome\MasterFlow-AutoSuite\supervisor.py"
if errorlevel 1 (
    start "MasterFlow Supervisor" /min python "C:\SmartHome\MasterFlow-AutoSuite\supervisor.py"
)

echo [*] Opening Realtime Dashboard...
start "" "https://preserve-near-firms-blank.trycloudflare.com"

echo.
echo [*] System running automatically in background.
echo.
ping 127.0.0.1 -n 3 >nul
exit /b 0
