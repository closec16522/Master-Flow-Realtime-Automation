@echo off
setlocal
echo ============================================================
echo   Phone Auto-Recovery Configuration (4x Redmi 14C)
echo ============================================================
echo.

set ADB_PATH=C:\Users\Administrator\AppData\Roaming\flow-automation\phone-tools\scrcpy-win64-v4.1\adb_real.exe
set ANDROID_ADB_SERVER_PORT=5037

for %%D in (9T9PTC4LTOY9BQ75 OR7LHALZSCKNZPDA RCV4R8FAV8UWRKPZ RS9POV8XPRPZ4XE6) do (
    echo [*] Configuring device %%D...
    "%ADB_PATH%" -P 5037 -s %%D shell settings put global stay_on_while_plugged_in 7
    "%ADB_PATH%" -P 5037 -s %%D shell svc power stayon true
    "%ADB_PATH%" -P 5037 -s %%D shell ime set com.android.adbkeyboard/.AdbIME
    "%ADB_PATH%" -P 5037 -s %%D shell input keyevent 224
    "%ADB_PATH%" -P 5037 -s %%D shell wm dismiss-keyguard
)

echo.
echo [*] All devices configured for Auto-Recovery!
ping 127.0.0.1 -n 3 >nul
