# Master Flow Realtime Automation Suite ⚡

[![Python 3.13+](https://img.shields.io/badge/Python-3.13%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011%20%7C%20Android%2014-green.svg)]()
[![Hardware](https://img.shields.io/badge/Devices-4x%20Redmi%2014C-orange.svg)]()
[![Meta Graph API](https://img.shields.io/badge/Meta%20Graph%20API-v26.0-blue.svg)](https://developers.facebook.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)]()

> **ระบบควบคุมและติดตามอัตโนมัติแบบรวมศูนย์ (End-to-End Automation & Monitoring Suite)**
> สำหรับบริหารจัดการการผลิตและโพสต์คอนเทนต์อัตโนมัติบน **Facebook Reels**, **Shopee Video** และ **TikTok** พร้อมระบบ **วอร์มบัญชีผ่านโทรศัพท์จริง 4 เครื่อง (Redmi 14C)**, ระบบ **Supervisor Auto-Recovery (เปิดเครื่องและกู้คืนอัตโนมัติ)** และ **Realtime Monitoring Dashboard**

---

## 🌟 ฟีเจอร์หลัก (Key Features)

### 1. 🎬 แผนผลิตคอนเทนต์สลับอัตโนมัติ (Alternating Content Pipeline)
* **สูตรสลับ 1:1:** ปล่อยคลิป **"ซีรีส์เรื่องเล่า / แฟ้มคดีปริศนา"** (เพื่อดึงดูดผู้ชม ดันยอดวิว และเพิ่มยอดผู้ติดตาม) สลับกับคลิป **"รีวิวสินค้า Affiliate"** (เพื่อปักตะกร้าสร้างยอดขาย)
* **Multi-Platform Dispatch:** ยิงโพสต์อัตโนมัติพร้อมกัน 3 แพลตฟอร์ม:
  * 🔵 **Facebook Reels:** ยิงผ่าน Meta Graph API v26.0 ไปยังเพจ *น้องบีรีวิว ปักตระกร้า SP* (พร้อมปักหมุดคอมเมนต์แรกอัตโนมัติ)
  * 🟠 **Shopee Video:** รันผ่านระบบมือถือ 4 เครื่อง คาลิเบรตพิกัดสัมผัส 16 จุด และพิมพ์ผ่าน `AdbIME`
  * 🎵 **TikTok:** ซิงค์ผ่านเซสชันคุกกี้อัตโนมัติสำหรับบัญชี `@closec16522`

### 2. 🔥 ระบบวอร์มบัญชีและเร่งอัลกอริทึม (3-Way Warming Engine)
* **4x Redmi 14C Farm:** เชื่อมต่อผ่าน ADB Port `5038`
* บอททำงานพฤติกรรมเลียนแบบมนุษย์:
  * ดูคลิปจบ 100% (High Retention Rate)
  * สุ่มกดหัวใจ (Like) และกดแชร์คลิป (Share / Copy Link)
  * สุ่มคลิกเปิดดูตะกร้าสินค้าเพื่อสร้างประวัติผู้ซื้อคุณภาพใน Niche เดียวกัน

### 3. 🛡️ ระบบเปิดเครื่องและกู้คืนอัตโนมัติ (Hardware Auto-Recovery & Power Center)
* **ฝั่งคอมพิวเตอร์ (PC Auto Power-On):**
  * **Windows Wake Timers:** เปิดใช้งาน `powercfg RTCWAKE 1` สำหรับการปลุกเครื่องตามเวลา
  * **Startup Auto-Launch:** ติดตั้งในโฟลเดอร์ Windows Startup บูตเครื่องแล้วเริ่มรันทันทีโดยไม่ต้องคลิกเปิดโปรแกรม
  * **BIOS AC Power Recovery:** รองรับการเปิดเครื่องทันทีเมื่อไฟดับ/ไฟตกแล้วไฟมา (`Restore on AC/Power Loss: Always On`)
* **ฝั่งมือถือ Redmi 14C ทั้ง 4 เครื่อง (Phone Auto-Recovery):**
  * **Stay-On While Plugged In:** ตั้งค่า `stay_on_while_plugged_in 7` และ `svc power stayon true` หน้าจอไม่ดับขณะเสียบชาร์จ
  * **Watchdog Heartbeat:** Supervisor ตรวจจับสถานะหน้าจอทุก 30 วินาที หากดับจะยิงคำสั่ง `input keyevent 224` ปลุกและปลดล็อคทันที
  * **Keyboard Watcher:** ตรวจสอบและสลับคีย์บอร์ดกลับมาเป็น `com.android.adbkeyboard/.AdbIME` เสมอ

### 4. ⏰ ตารางเวลาทำงานและถนอมอุปกรณ์ (Scheduled Operations)
* **จันทร์ – ศุกร์:** ทำงานเวลา **07:00 – 22:00 น.**
* **เสาร์ – อาทิตย์:** ทำงานเวลา **07:00 – 01:00 น. (ตี 1)**
* **เมื่อถึงเวลาเลิกงาน:** ระบบจะสั่งหยุดโปรแกรม ปรับความสว่างหน้าจอมือถือเป็น 0 และดับหน้าจอ (`Screen Off`) เพื่อประหยัดพลังงานและถนอมหน้าจอมือถือ

### 5. 🌐 แดชบอร์ดติดตามสถานะแบบเรียลไทม์ (Live Realtime Dashboard)
* สตรีมสถานะผ่าน Cloudflare Quick Tunnel ให้ดูภาพรวมจากที่ไหนก็ได้ตลอด 24 ชั่วโมง
* แสดงสถิติการวอร์มคลิป, สถานะแบตเตอรี่, ประวัติคลิปที่โพสต์สำเร็จพร้อมลิงก์ดูสด, ผังคิวงาน และ Live Activity Logs

---

## 📁 โครงสร้างโปรเจกต์ (Project Structure)

```text
MasterFlow-AutoSuite/
├── supervisor.py              # ระบบ Watchdog, Auto-Recovery และคุมเวลาทำงาน
├── backend_server.py          # เซิร์ฟเวอร์ API Status (Port 3333) & บอทวอร์มมือถือ 4 เครื่อง
├── realtime_dashboard.html    # แดชบอร์ด Realtime UI (TailwindCSS)
├── index.html                 # สำเนาแดชบอร์ดสำหรับ GitHub Pages / Local Web
├── start_masterflow_automation.bat  # สคริปต์เริ่มระบบปุ่มเดียว (One-Click Launcher)
├── setup_phone_recovery.bat   # สคริปต์ตั้งค่าความพร้อมมือถือ 4 เครื่อง
├── config.example.json        # ตัวอย่างไฟล์การตั้งค่าระบบ
└── README.md                  # เอกสารคู่มือการใช้งานระบบ
```

---

## 🚀 วิธีการเริ่มต้นใช้งาน (Getting Started)

### 1. รันระบบผ่านสคริปต์ปุ่มเดียว
ดับเบิลคลิกไฟล์:
```cmd
🚀 เริ่มระบบ Master Flow อัตโนมัติ (ปุ่มเดียว).bat
```
หรือรันผ่าน Terminal:
```cmd
cd C:\SmartHome\MasterFlow-AutoSuite
start_masterflow_automation.bat
```

### 2. ดูแดชบอร์ดมอนิเตอร์สด (Dashboard)
เปิดผ่านเบราว์เซอร์:
* **Localhost:** `http://127.0.0.1:3333`
* **Cloudflare Tunnel (Remote):** ลิงก์ที่สร้างโดย `cloudflared` (เช่น `https://preserve-near-firms-blank.trycloudflare.com`)

---

## ⚙️ การตั้งค่าระบบเปิดเครื่องอัตโนมัติ (Hardware Auto-Power Setup)

### 1. การตั้งค่า BIOS/UEFI สำหรับคอมพิวเตอร์
เพื่อให้คอมพิวเตอร์เปิดตัวเองขึ้นมาทันทีเมื่อมีไฟเข้ามา (กรณีไฟดับ ไฟตก หรือปิดสวิตช์แล้วเปิดใหม่):
1. รีสตาร์ทคอมพิวเตอร์ กด `DEL` หรือ `F2` เพื่อเข้าหน้า BIOS Setup
2. ไปที่เมนู **Power Management** หรือ **Advanced**
3. ค้นหาหัวข้อ **Restore on AC/Power Loss** (หรือ *AC Back* / *State After G3*)
4. เปลี่ยนค่าเป็น **`Power On`** หรือ **`Always On`**
5. กด `F10` เพื่อบันทึกและรีสตาร์ท

### 2. การตั้งค่ามือถือ Redmi 14C
1. เปิดโหมด Developer Options และเปิด **USB Debugging**
2. เชื่อมต่อสาย USB และรันคำสั่ง:
   ```cmd
   setup_phone_recovery.bat
   ```
3. สำหรับการตั้งเวลาเปิดเครื่องอัตโนมัติบนมือถือ:
   * ไปที่ **Settings > Battery > Schedule Power On/Off**
   * ตั้งเวลาเปิดเครื่องทุกวันเวลา **06:50 น.**

---

## 👥 ข้อมูลและการติดต่อ (Author & Credits)
* **GitHub Repository:** [closec16522/Master-Flow-Realtime-Automation](https://github.com/closec16522/Master-Flow-Realtime-Automation)
* **Automation Suite:** Master Flow & Google Antigravity Agent
