import os
import sys
import time
import datetime
import subprocess
import socket
import json
import urllib.request

ADB_PATH = r"C:\Users\Administrator\AppData\Roaming\flow-automation\phone-tools\scrcpy-win64-v4.1\adb_real.exe"
ADB_PORT = "5038"
MASTER_FLOW_EXE = r"C:\Users\Administrator\AppData\Local\Programs\flow-automation\Master Flow.exe"
BACKEND_SCRIPT = r"C:\SmartHome\MasterFlow-AutoSuite\backend_server.py"
CLOUDFLARED_EXE = r"C:\SmartHome\MasterFlow-AutoSuite\cloudflared.exe"
DEVICES = ["9T9PTC4LTOY9BQ75", "OR7LHALZSCKNZPDA", "RCV4R8FAV8UWRKPZ", "RS9POV8XPRPZ4XE6"]

def log(msg):
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{t}] [SUPERVISOR] {msg}", flush=True)

def is_within_working_hours():
    now = datetime.datetime.now()
    weekday = now.weekday()  # 0=Mon, ..., 4=Fri, 5=Sat, 6=Sun
    hour = now.hour

    # Weekend spillover (Sat night into Sun 00:00-01:00 or Sun night into Mon 00:00-01:00)
    if weekday in (0, 6) and hour < 1:
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
    except Exception:
        return ""

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        return s.connect_ex(('127.0.0.1', port)) == 0

def is_process_running(process_name):
    try:
        out = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}" /NH', shell=True, text=True)
        return process_name.lower() in out.lower()
    except Exception:
        return False

def ensure_master_flow():
    if not is_process_running("Master Flow.exe"):
        log("Master Flow ไม่ได้เปิดอยู่ -> สั่งเปิดโปรแกรมอัตโนมัติ (Bypass UAC / RunAsInvoker)...")
        try:
            # Ensure RUNASADMIN compatibility flag is removed so Windows UAC never prompts
            subprocess.run([
                "reg", "delete",
                r"HKCU\Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers",
                "/v", MASTER_FLOW_EXE, "/f"
            ], capture_output=True)
            env = os.environ.copy()
            env["__COMPAT_LAYER"] = "RunAsInvoker"
            subprocess.Popen([MASTER_FLOW_EXE], env=env, cwd=os.path.dirname(MASTER_FLOW_EXE))
            time.sleep(5)
        except Exception as e:
            log(f"ไม่สามารถเปิด Master Flow: {e}")

def ensure_backend_server():
    if not is_port_open(3333):
        log("Backend Server (Port 3333) ออฟไลน์ -> สั่งเริ่มทำงาน...")
        try:
            subprocess.Popen([sys.executable, BACKEND_SCRIPT],
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            time.sleep(3)
        except Exception as e:
            log(f"ไม่สามารถเปิด Backend Server: {e}")

def ensure_cloudflared():
    if not is_process_running("cloudflared.exe") and os.path.exists(CLOUDFLARED_EXE):
        log("Cloudflare Tunnel ออฟไลน์ -> สั่งเปิด Tunnel อัตโนมัติ...")
        try:
            cf_log = r"C:\SmartHome\MasterFlow-AutoSuite\cloudflared.log"
            subprocess.Popen([CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:3333", "--logfile", cf_log],
                             creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            time.sleep(3)
        except Exception as e:
            log(f"ไม่สามารถเปิด Cloudflared: {e}")

def recover_phone(serial):
    try:
        out = subprocess.check_output([ADB_PATH, "-P", ADB_PORT, "devices"], text=True)
        if serial not in out or "device" not in out:
            return
    except Exception:
        return

    pwr = adb_shell(serial, "dumpsys power")
    is_asleep = ("mHoldingDisplaySuspendBlocker=false" in pwr or
                 "mWakefulness=Asleep" in pwr or
                 "Display Power: state=OFF" in pwr)

    if is_asleep:
        log(f"มือถือ {serial} หน้าจอดับ -> ปลุกหน้าจอและปลดล็อคอัตโนมัติ...")
        adb_shell(serial, "input keyevent 224")
        adb_shell(serial, "wm dismiss-keyguard")
        adb_shell(serial, "settings put global stay_on_while_plugged_in 7")
        adb_shell(serial, "svc power stayon true")
        time.sleep(1)

    ime = adb_shell(serial, "settings get secure default_input_method")
    if "com.android.adbkeyboard" not in ime:
        adb_shell(serial, "ime enable com.android.adbkeyboard/.AdbIME")
        adb_shell(serial, "ime set com.android.adbkeyboard/.AdbIME")

    win = adb_shell(serial, "dumpsys window")
    if "com.shopee.th" not in win and "com.zhiliaoapp.musically" not in win:
        log(f"มือถือ {serial} ยังไม่ได้เปิด Shopee/TikTok -> สั่งเปิดแอปอัตโนมัติ...")
        adb_shell(serial, "monkey -p com.shopee.th -c android.intent.category.LAUNCHER 1")
        time.sleep(4)
        adb_shell(serial, "input tap 429 1503")

def prompt_20s_shutdown_cancel():
    """
    เด้ง Popup เตือนบนหน้าจอ Windows นับถอยหลัง 20 วินาที พร้อมปุ่มยกเลิก (Cancel)
    และส่งสัญญาณไปยัง Web Dashboard ให้เด้ง Popup 20 วินาทีพร้อมกัน
    คืนค่า True หากต้องปิดระบบต่อ, คืนค่า False หากผู้ใช้กดยกเลิก
    """
    log("แจ้งเตือนการปิดระบบ: เริ่มนับถอยหลัง 20 วินาที (สามารถกดปุ่มยกเลิกได้)...")
    try:
        req = urllib.request.Request(
            "http://127.0.0.1:3333/api/system/shutdown-request",
            data=json.dumps({"reason": "Scheduled Operating Hours Ended", "countdown": 20}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass

    # Show native Windows popup with 20 second timeout using WScript.Shell Popup
    # Return value 2 = Cancel button pressed, -1 = Timed out (proceed with shutdown)
    ps_cmd = (
        "$ws = New-Object -ComObject WScript.Shell; "
        "$res = $ws.Popup('ถึงเวลาปิดระบบอัตโนมัติ (Computer & มือถือ 4 เครื่อง)\n"
        "ระบบจะทำการพักหน้าจอมือถือและปิดระบบในอีก 20 วินาที...\n\n"
        "กดปุ่ม [Cancel / ยกเลิก] หากต้องการให้ระบบทำงานต่อไป', 20, "
        "'Master Flow Auto-Shutdown Warning (20s Countdown)', 1 + 48); "
        "Write-Output $res"
    )
    try:
        res = subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd],
                             capture_output=True, text=True, timeout=25)
        code = res.stdout.strip()
        if code == "2":
            log("ผู้ใช้กดปุ่ม [ยกเลิก / Cancel] -> ยกเลิกการปิดระบบ ทำงานต่อตามปกติ!")
            try:
                req = urllib.request.Request(
                    "http://127.0.0.1:3333/api/system/shutdown-cancel",
                    data=b"{}",
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                urllib.request.urlopen(req, timeout=3)
            except Exception:
                pass
            return False
    except Exception:
        pass

    # Check if cancelled via Web Dashboard
    try:
        res = urllib.request.urlopen("http://127.0.0.1:3333/api/status", timeout=3)
        st = json.loads(res.read().decode("utf-8"))
        if not st.get("shutdown_state", {}).get("active", False):
            log("ผู้ใช้กดยกเลิกผ่านหน้า Web Dashboard -> ยกเลิกการปิดระบบ!")
            return False
    except Exception:
        pass

    return True

def sleep_phones_and_pc():
    log("ดำเนินการปิดระบบ: ปรับมือถือทุกเครื่องเข้าสู่โหมดพักผ่อน (Sleep)...")
    for d in DEVICES:
        adb_shell(d, "am force-stop com.shopee.th")
        adb_shell(d, "settings put system screen_brightness 0")
        adb_shell(d, "input keyevent 26")

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

                ensure_master_flow()
                ensure_backend_server()
                ensure_cloudflared()

                for d in DEVICES:
                    recover_phone(d)

            else:
                if was_active:
                    log("หมดช่วงเวลาทำงาน (Off-Hours) -> เตรียมปิดระบบพร้อมเด้งเตือน 20 วินาที...")
                    if prompt_20s_shutdown_cancel():
                        sleep_phones_and_pc()
                        was_active = False
                    else:
                        log("ข้ามการปิดระบบในรอบนี้เนื่องจากผู้ใช้กดยกเลิก")

            time.sleep(30)

        except Exception as e:
            log(f"Error in supervisor loop: {e}")
            time.sleep(15)

if __name__ == "__main__":
    main()
