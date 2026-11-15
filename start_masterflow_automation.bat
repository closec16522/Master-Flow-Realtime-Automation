@echo off
chcp 65001 >nul
setlocal
set ANDROID_ADB_SERVER_PORT=5038
set "PY_EXE=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe"

echo ============================================================
echo   Master Flow Realtime Automation Suite (Auto-Supervisor)
echo ============================================================
echo.

if exist "%PY_EXE%" (
    echo [*] Starting Backend Server ^& Auto-Supervisor Watchdog via Python 3.11...
    start "MasterFlow Backend Server" /min "%PY_EXE%" "C:\SmartHome\MasterFlow-AutoSuite\backend_server.py"
    ping 127.0.0.1 -n 3 >nul
    start "MasterFlow Supervisor" /min "%PY_EXE%" "C:\SmartHome\MasterFlow-AutoSuite\supervisor.py"
) else (
    echo [*] Starting Backend Server ^& Auto-Supervisor Watchdog via system PATH python...
    start "MasterFlow Backend Server" /min python "C:\SmartHome\MasterFlow-AutoSuite\backend_server.py"
    ping 127.0.0.1 -n 3 >nul
    start "MasterFlow Supervisor" /min python "C:\SmartHome\MasterFlow-AutoSuite\supervisor.py"
)

echo [*] Waiting 2 seconds for Local Realtime Dashboard on Port 3333...
ping 127.0.0.1 -n 3 >nul

echo [*] Opening Realtime Dashboard (http://127.0.0.1:3333)...
start "" "http://127.0.0.1:3333"

echo.
echo [*] All systems launched and running automatically in background!
echo.
ping 127.0.0.1 -n 3 >nul
exit /b 0
