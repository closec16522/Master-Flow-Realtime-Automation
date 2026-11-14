import os
import sys
import time
import datetime
import subprocess
import socket
import json

ADB_PATH = r"C:\Users\Administrator\AppData\Roaming\flow-automation\phone-tools\scrcpy-win64-v4.1\adb_real.exe"
ADB_PORT = "5038"
MASTER_FLOW_EXE = r"C:\Users\Administrator\AppData\Local\Programs\flow-automation\Master Flow.exe"
BACKEND_SCRIPT = r"C:\Users\Administrator\.gemini\antigravity\brain\d1568b5b-90b0-480a-b56a-6691372d4e53\scratch\backend_server.py"
CLOUDFLARED_EXE = r"C:\Users\Administrator\.gemini\antigravity\brain\d1568b5b-90b0-480a-b56a-6691372d4e53\scratch\cloudflared.exe"
DEVICES = ["9T9PTC4LTOY9BQ75", "OR7LHALZSCKNZPDA", "RCV4R8FAV8UWRKPZ", "RS9POV8XPRPZ4XE6"]

def log(msg):
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] [SUPERVISOR] {msg}", flush=True)

def is_within_working_hours():
    now = datetime.datetime.now()
    weekday = now.weekday()  # 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    hour = now.hour

    # Weekend spillover (Sun night into Mon 00:00-01:00 or Sat night into Sun 00:00-01:00)
    if weekday == 0 and hour < 1:
        return True
    if weekday == 6 and hour < 1:
        return True

    # Weekend (Sat / Sun): 07:00 to 01:00 (of next day)
    if weekday in (5, 6):
        return hour >= 7
    else:
        # Weekday (Mon - Fri): 07:00 to 22:00
        return 7 <= hour < 22

def adb_shell(serial, cmd):
    try:
        res = subprocess.run([ADB_PATH, "-P", ADB_PORT, "-s", serial, "shell"] + cmd.split(" "),
                             capture_output=True, text=True, timeout=10)
        return res.stdout.strip()
    except Exception as e:
        return ""

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        return s.connect_ex(('127.0.0.1', port)) == 0

def is_process_running(process_name):
    try:
        out = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}" /NH', shell=True, text=True)
        return process_name.lower() in out.lower()
    except:
        return False

def ensure_master_flow():
    if not is_process_running("Master Flow.exe"):
        log("Master Flow ไม่ได้เปิดอยู่ -> สั่งเปิดโปรแกรมอัตโนมัติ...")
        try:
            subprocess.Popen([MASTER_FLOW_EXE], shell=True)
            time.sleep(5)
        except Exception as e:
            log(f"ไม่สามารถเปิด Master Flow: {e}")

def ensure_backend_server():
    if not is_port_open(3333):
        log("Backend Server (Port 3333) ออฟไลน์ -> สั่งเริ่มทำงาน...")
        try:
            subprocess.Popen([sys.executable, BACKEND_SCRIPT], creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            time.sleep(3)
        except Exception as e:
            log(f"ไม่สามารถเปิด Backend Server: {e}")

def ensure_cloudflared():
    if not is_process_running("cloudflared.exe"):
        log("Cloudflare Tunnel ออฟไลน์ -> สั่งเปิด Tunnel อัตโนมัติ...")
        try:
            subprocess.Popen([CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:3333"],
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            time.sleep(3)
        except Exception as e:
            log(f"ไม่สามารถเปิด Cloudflared: {e}")

def recover_phone(serial):
    # Check if device is attached
    try:
        out = subprocess.check_output([ADB_PATH, "-P", ADB_PORT, "devices"], text=True)
        if serial not in out or "device" not in out:
            return
    except:
        return

    # Check screen state
    pwr = adb_shell(serial, "dumpsys power")
    is_asleep = "mHoldingDisplaySuspendBlocker=false" in pwr or "mWakefulness=Asleep" in pwr or "Display Power: state=OFF" in pwr

    if is_asleep:
        log(f"มือถือ {serial} หน้าจอดับ -> ปลุกหน้าจอและปลดล็อคอัตโนมัติ...")
        adb_shell(serial, "input keyevent 224") # Wakeup
        adb_shell(serial, "wm dismiss-keyguard") # Unlock
        adb_shell(serial, "settings put global stay_on_while_plugged_in 7")
        time.sleep(1)

    # Ensure ADBKeyboard is current
    ime = adb_shell(serial, "settings get secure default_input_method")
    if "com.android.adbkeyboard" not in ime:
        adb_shell(serial, "ime enable com.android.adbkeyboard/.AdbIME")
        adb_shell(serial, "ime set com.android.adbkeyboard/.AdbIME")

    # Ensure Shopee is running
    win = adb_shell(serial, "dumpsys window")
    if "com.shopee.th" not in win:
        log(f"มือถือ {serial} ยังไม่ได้เปิด Shopee -> สั่งเปิดแอปอัตโนมัติ...")
        adb_shell(serial, "monkey -p com.shopee.th -c android.intent.category.LAUNCHER 1")
        time.sleep(4)
        adb_shell(serial, "input tap 429 1503") # Live & Video

def sleep_phones():
    log("หมดเวลาทำงาน -> ปรับมือถือทุกเครื่องเข้าสู่โหมดพักผ่อน (Sleep)...")
    for d in DEVICES:
        adb_shell(d, "am force-stop com.shopee.th")
        adb_shell(d, "settings put system screen_brightness 0")
        adb_shell(d, "input keyevent 26") # Power button to turn off screen

def main():
    log("=====================================================")
    log("เริ่มต้นระบบ Master Flow Auto-Supervisor & Keep-Alive")
    log("ตารางทำงาน: จ.-ศ. 07:00-22:00 | ส.-อ. 07:00-01:00")
    log("=====================================================")

    was_active = False

    while True:
        try:
            active = is_within_working_hours()

            if active:
                if not was_active:
                    log("เข้าสู่ช่วงเวลาทำงาน (Working Hours Active) -> เริ่มการทำงานอัตโนมัติทุกส่วน!")
                    was_active = True

                # 1. Watchdog processes
                ensure_master_flow()
                ensure_backend_server()
                ensure_cloudflared()

                # 2. Watchdog phones (4x Redmi 14C)
                for d in DEVICES:
                    recover_phone(d)

            else:
                if was_active:
                    log("หมดช่วงเวลาทำงาน (Off-Hours) -> สั่งปิดระบบชั่วคราวเพื่อประหยัดพลังงาน...")
                    sleep_phones()
                    was_active = False

            # Wait 30 seconds before next health check
            time.sleep(30)

        except Exception as e:
            log(f"Error in supervisor loop: {e}")
            time.sleep(15)

if __name__ == "__main__":
    main()
