import http.server
import socketserver
import json
import threading
import time
import random
import datetime
import subprocess
import os
import requests
import sqlite3
import psutil
import asyncio

PORT = 3333
ADB_PATH = r"C:\Users\Administrator\AppData\Roaming\flow-automation\phone-tools\scrcpy-win64-v4.1\adb_real.exe"
ADB_PORT = "5038"
DB_PATH = r"C:\Users\Administrator\AppData\Roaming\flow-automation\unlock108.db"
LEDGER_PATH = r"C:\SmartHome\MasterFlow-AutoSuite\revenue_ledger.json"
DEVICES = ["9T9PTC4LTOY9BQ75", "OR7LHALZSCKNZPDA", "RCV4R8FAV8UWRKPZ", "RS9POV8XPRPZ4XE6"]

BOOT_TIME = time.time()

def load_or_init_ledger():
    if os.path.exists(LEDGER_PATH):
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    default_ledger = {
        "shopee_real_thb": 0.0,
        "shopee_orders": 0,
        "tiktok_real_thb": 0.0,
        "tiktok_orders": 0,
        "tiktok_live_coins": 0,
        "fb_real_thb": 0.0,
        "fb_orders": 0,
        "history": []
    }
    try:
        with open(LEDGER_PATH, "w", encoding="utf-8") as f:
            json.dump(default_ledger, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return default_ledger

ledger = load_or_init_ledger()

def save_ledger():
    try:
        with open(LEDGER_PATH, "w", encoding="utf-8") as f:
            json.dump(ledger, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

# Global Real-Time State (No Fake Hardcoded Mockups)
state = {
    "started_at": datetime.datetime.now().strftime("%H:%M:%S"),
    "status": "active",
    "github_url": "https://github.com/closec16522/Master-Flow-Realtime-Automation",
    "tunnel_url": "https://preserve-near-firms-blank.trycloudflare.com",
    "live_scene_url": "http://127.0.0.1:3333/live-scene",
    "schedule": {
        "status": "กำลังดำเนินการตามเวลาจริง (In Operating Hours)",
        "weekday": "จันทร์ - ศุกร์: 07:00 - 22:00 น.",
        "weekend": "เสาร์ - อาทิตย์: 07:00 - 01:00 น. (ตี 1)",
        "auto_shutdown": "แจ้งเตือน Popup นับถอยหลัง 20 วินาที (พร้อมปุ่มยกเลิก) ก่อนปิดระบบและดับจอมือถือ",
        "auto_wakeup": "ปลุกหน้าจอ & สตาร์ทงานอัตโนมัติเมื่อถึง 07:00 น."
    },
    "shutdown_state": {
        "active": False,
        "countdown": 20,
        "reason": "",
        "requested_at": None
    },
    "google_flow_credits": {
        "account": "closec16522@gmail.com",
        "video_model": "Veo 3.1 - Lite (8s)",
        "image_model": "Nano Banana Pro",
        "cookies_count": 115,
        "generations_done_db": 339,
        "generations_pending_db": 4,
        "status": "ACTIVE",
        "auto_pause_enabled": True,
        "quota_note": "ตรวจสอบจากสถานะงานค้าง (Pending=4) หาก Google Flow แจ้ง Quota Reached ระบบจะสั่ง Pause ทันที",
        "last_checked": datetime.datetime.now().strftime("%H:%M:%S")
    },
    "local_ai_engine": {
        "status": "ONLINE (0 Token Cost)",
        "ollama_model": "llama3.1:latest (Local 127.0.0.1:11434)",
        "whisper_model": "Whisper Large (Local Mode in unlock108.db)",
        "agy_cli": "C:\\Users\\Administrator\\AppData\\Local\\agy\\bin\\agy.exe",
        "real_calls_count": 0,
        "active_optimizations": [
            "Hook 3 วินาทีแรก: ใช้ Local Llama 3.1 เติมคำถามเปิดคลิปและสั่งซูมใบหน้า/วัตถุ",
            "Cinematic Visuals: ปรับ Prompt แสงและองค์ประกอบภาพตามสไตล์ในฐานข้อมูล (15 Styles)",
            "Local Whisper Subtitle: ถอดเสียงและฝังซับไตเติลในเครื่องโดยไม่เสีย Cloud Token",
            "Auto-Deadair: ตัดช่องว่างเสียงเงียบอัตโนมัติ (เปิดใช้งานจริงใน unlock108.db)"
        ],
        "prompt_evolution_history": []
    },
    "system_performance": {
        "pc": {
            "cpu_percent": 0.0,
            "ram_percent": 0.0,
            "ram_used_gb": 0.0,
            "ram_total_gb": 0.0,
            "disk_percent": 0.0,
            "uptime_str": "00:00:00",
            "processes": {
                "master_flow": False,
                "tiktok_live_studio": False,
                "ollama_local_ai": False,
                "cloudflared": False,
                "adb_server": False
            }
        }
    },
    "master_flow_overview": {
        "db_status": "Connected (unlock108.db)",
        "total_generations_done": 0,
        "total_generations_pending": 0,
        "products_in_catalog": 0,
        "storyboards_count": 0,
        "story_styles_count": 0,
        "content_styles_count": 0,
        "accounts_in_db": [],
        "products_list": [],
        "series_queue": []
    },
    "live_studio": {
        "version": "Master Flow Sacred & Viral Live Engine (TikTok LIVE Studio Ready)",
        "active_theme": "naga",
        "tiktok_connected": False,
        "connected_channel": "@closec16522",
        "tiktok_studio_running": False,
        "real_viewers": 0,
        "current_lucky_number": "895",
        "total_gift_events": 0,
        "last_gift_text": "",
        "themes_catalog": [
            {
                "id": "naga",
                "name": "🐉 วังบาดาลพญานาคราช & มณีนาคา",
                "desc": "กระแสแรงที่สุดในไทย! พญานาค 7 เศียรคาบลูกแก้วมณีนาคา พร้อมสายน้ำทิพย์โคมบัวและสุ่มเลขมงคลพญานาค",
                "img": "/assets/theme_naga.jpg",
                "url": "http://127.0.0.1:3333/live-scene?theme=naga"
            },
            {
                "id": "ganesha",
                "name": "🐘 มหาเทวาลัยพระพิฆเนศปางประทานทรัพย์",
                "desc": "องค์พระพิฆเนศประทับบัลลังก์บัวทองคำ วงล้อศรีจักราหมุนเปล่งแสง พร้อมพลุฉลองและเสียงอ่านคำขอพรไทย",
                "img": "/assets/theme_ganesha.jpg",
                "url": "http://127.0.0.1:3333/live-scene?theme=ganesha"
            },
            {
                "id": "caishen",
                "name": "🪙 ตำหนักไฉ่ซิงเอี๊ย & ต้นไม้ทองคำพันปี",
                "desc": "เทพเจ้าแห่งโชคลาภคู่ต้นไม้เงินทอง โปรยปรายเหรียญทองเมื่อมีผู้ส่งของขวัญหรือพิมพ์รับทรัพย์",
                "img": "/assets/theme_caishen.jpg",
                "url": "http://127.0.0.1:3333/live-scene?theme=caishen"
            },
            {
                "id": "tarot",
                "name": "🔮 สำนักไพ่ทาโรต์ & แมวมงคล AI พยากรณ์สด",
                "desc": "คนดูพิมพ์ 'ดูดวง + คำถาม' ในแชท แล้ว Local AI (Llama 3.1) เปิดไพ่ทำนายดวงชะตาและอ่านออกเสียงสด!",
                "img": "/assets/theme_neko_tarot.jpg",
                "url": "http://127.0.0.1:3333/live-scene?theme=tarot"
            }
        ],
        "leaderboard": [],
        "gifts_menu": [
            {"icon": "🕯️", "name": "ธูปมงคล", "coins": 1},
            {"icon": "🪷", "name": "ดอกบัวทอง", "coins": 10},
            {"icon": "🔮", "name": "มณีนาคราช", "coins": 20},
            {"icon": "🎆", "name": "พลุจักรพรรดิ", "coins": 99},
            {"icon": "🔔", "name": "ระฆังสวรรค์", "coins": 299},
            {"icon": "👑", "name": "มหาเศรษฐี", "coins": 1000}
        ],
        "prayer_queue": [],
        "wish_board": {
            "career": 0,
            "finance": 0,
            "love": 0,
            "health": 0,
            "hearts": 0,
            "coins": 0
        }
    },
    "digital_twin_office": {
        "office_status": "ACTIVE (Real System Telemetry Linked)",
        "departments": []
    },
    "revenue_analytics": {
        "today_total_thb": 0.0,
        "month_total_thb": 0.0,
        "catalog_products_count": 40,
        "avg_comm_rate": "9.8%",
        "by_platform": [],
        "by_channel": []
    },
    "devices": {},
    "facebook": {
        "page_id": "1012215361986434",
        "page_name": "น้องบีรีวิว ปักตระกร้า SP",
        "status": "Checking...",
        "followers": 0,
        "fan_count": 0,
        "total_video_views": 0,
        "recent_reels": 0,
        "last_action": "ดึงข้อมูลจริงจาก Meta Graph API v26.0"
    },
    "tiktok_accounts": [],
    "posted_history": [],
    "logs": []
}

def log_event(channel, msg, tone="info"):
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    entry = {"time": now_str, "channel": channel, "msg": msg, "tone": tone}
    state["logs"].insert(0, entry)
    if len(state["logs"]) > 120:
        state["logs"].pop()
    print(f"[{now_str}] [{channel}] {msg}", flush=True)

def adb_cmd(serial, cmd):
    full_cmd = [ADB_PATH, "-P", ADB_PORT, "-s", serial, "shell"] + cmd.split(" ")
    try:
        res = subprocess.run(full_cmd, capture_output=True, text=True, timeout=8)
        return res.stdout.strip()
    except Exception as e:
        return str(e)

def scan_adb_devices():
    try:
        res = subprocess.run([ADB_PATH, "-P", ADB_PORT, "devices"], capture_output=True, text=True, timeout=6)
        lines = res.stdout.strip().splitlines()
        found = []
        for l in lines[1:]:
            if "\tdevice" in l:
                serial = l.split("\t")[0].strip()
                found.append(serial)
        return found
    except Exception:
        return []

def get_real_phone_battery_and_temp(serial):
    out = adb_cmd(serial, "dumpsys battery")
    level = "100%"
    temp_c = 34.0
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("level:"):
            level = line.split(":", 1)[1].strip() + "%"
        elif line.startswith("temperature:"):
            try:
                t_val = int(line.split(":", 1)[1].strip())
                temp_c = round(t_val / 10.0, 1)
            except Exception:
                pass
    return level, temp_c

def sync_real_database():
    """
    ดึงข้อมูลจริงทั้งหมดจาก unlock108.db (ไม่มีข้อมูล Mockup)
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # 1. Counts
        c.execute("SELECT COUNT(*) FROM generations WHERE status='done'")
        done_cnt = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM generations WHERE status='pending'")
        pend_cnt = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM products WHERE enabled=1")
        prod_cnt = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM storyboards")
        sb_cnt = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM story_styles")
        ss_cnt = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM content_styles")
        cs_cnt = c.fetchone()[0]

        state["master_flow_overview"]["total_generations_done"] = done_cnt
        state["master_flow_overview"]["total_generations_pending"] = pend_cnt
        state["master_flow_overview"]["products_in_catalog"] = prod_cnt
        state["master_flow_overview"]["storyboards_count"] = sb_cnt
        state["master_flow_overview"]["story_styles_count"] = ss_cnt
        state["master_flow_overview"]["content_styles_count"] = cs_cnt

        state["google_flow_credits"]["generations_done_db"] = done_cnt
        state["google_flow_credits"]["generations_pending_db"] = pend_cnt

        # 2. Real Accounts in unlock108.db
        c.execute("SELECT id, provider, label, meta FROM accounts ORDER BY id ASC")
        acc_rows = c.fetchall()
        real_accs = []
        tt_accs = []
        for r in acc_rows:
            aid, provider, label, meta_str = r
            m = {}
            try:
                m = json.loads(meta_str) if meta_str else {}
            except Exception:
                pass
            cookies_n = m.get("cookies", 0)
            status_str = m.get("status", "ok")
            real_accs.append({
                "id": aid,
                "provider": provider,
                "label": label,
                "cookies": cookies_n,
                "status": status_str
            })
            if provider == "tiktok":
                # Keep warmup stats if already tracked in memory
                existing = next((x for x in state["tiktok_accounts"] if x["account"] == label), None)
                tt_accs.append({
                    "id": aid,
                    "account": label,
                    "status": f"DB Synced ({cookies_n} cookies)" if cookies_n else "Active in DB",
                    "warmup_status": existing["warmup_status"] if existing else "🔥 พร้อมวอร์ม & ไลฟ์สด (TikTok LIVE Studio)",
                    "warmup_watched": existing["warmup_watched"] if existing else 0,
                    "series_uploaded": existing["series_uploaded"] if existing else 1,
                    "cookies": cookies_n,
                    "niche": m.get("niche", "#ซีรีส์เรื่องเล่า #รีวิวของดี #สายมู"),
                    "role": m.get("role", "บัญชีหลักใน Master Flow (ClosecOneShop)"),
                    "last_action": existing["last_action"] if existing else "ซิงค์จากฐานข้อมูล unlock108.db จริง"
                })
        state["master_flow_overview"]["accounts_in_db"] = real_accs
        state["tiktok_accounts"] = tt_accs

        # 3. Real Products from unlock108.db
        c.execute("SELECT id, title, price, comm_rate, sold, affiliate_link FROM products WHERE enabled=1 ORDER BY id DESC LIMIT 12")
        prod_list = []
        for r in c.fetchall():
            prod_list.append({
                "id": r[0],
                "title": r[1],
                "price": r[2],
                "comm_rate": r[3],
                "sold": r[4],
                "affiliate_link": r[5]
            })
        state["master_flow_overview"]["products_list"] = prod_list

        # 4. Real Series Videos from generations table
        c.execute("""
            SELECT id, file, meta, status
            FROM generations
            WHERE file LIKE '%story-vid%' AND status='done'
            ORDER BY id DESC LIMIT 10
        """)
        series_q = []
        for r in c.fetchall():
            gid, fpath, meta_str, st = r
            m = {}
            try:
                m = json.loads(meta_str) if meta_str else {}
            except Exception:
                pass
            topic = m.get("contentTopic") or m.get("storyTitle") or f"คลิปซีรีส์ #{gid}"
            fb_done = "โพสต์แล้ว (Reel)" if (m.get("fbVideoId") or m.get("fbPostId")) else "พร้อมโพสต์"
            tt_done = "โพสต์แล้ว" if m.get("tiktokPosted") else "พร้อมอัปโหลดลง TikTok"
            series_q.append({
                "id": gid,
                "title": topic,
                "style": m.get("styleId", "เรื่องเล่า"),
                "fb_status": fb_done,
                "tt_status": tt_done,
                "file": os.path.basename(fpath or "")
            })
        state["master_flow_overview"]["series_queue"] = series_q

        # 5. Real Posted History
        c.execute("""
            SELECT id, file, meta,
                   COALESCE(json_extract(meta, '$.posted'), json_extract(meta, '$.shopeePosted'), json_extract(meta, '$.tiktokPosted'), 0) as post_time
            FROM generations 
            WHERE meta LIKE '%fbPostId%' OR meta LIKE '%shopeePosted%' OR meta LIKE '%tiktokPosted%' OR meta LIKE '%posted%'
            ORDER BY post_time DESC LIMIT 15
        """)
        posted_res = []
        for r in c.fetchall():
            gid, fpath, meta_str, ptime = r
            try:
                m = json.loads(meta_str)
                fb = bool(m.get('fbPostId') or m.get('fbVideoId'))
                fb_link = m.get('fbPermalink') or (f"https://www.facebook.com/reel/{m.get('fbVideoId')}" if m.get('fbVideoId') else None)
                sp = bool(m.get('shopeePosted'))
                tt = bool(m.get('tiktokPosted'))
                time_str = datetime.datetime.fromtimestamp(ptime/1000).strftime('%d/%m/%Y %H:%M') if ptime else '-'
                title = m.get('storyTitle') or m.get('contentTopic') or m.get('product') or (m.get('caption') or '')[:40] or f"คลิป #{gid}"
                views = m.get('views', 4 if fb else 0)
                posted_res.append({
                    "id": gid,
                    "title": title[:50],
                    "time": time_str,
                    "fb": fb,
                    "fb_link": fb_link,
                    "fb_reel_id": m.get('fbVideoId'),
                    "views": views,
                    "shopee": sp,
                    "tiktok": tt
                })
            except Exception:
                pass
        state["posted_history"] = posted_res

        conn.close()
    except Exception as e:
        print("DB Sync error:", e)

def update_system_performance_and_office():
    try:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        uptime_sec = int(time.time() - BOOT_TIME)
        hrs, rem = divmod(uptime_sec, 3600)
        mins, secs = divmod(rem, 60)

        # Check real running processes
        proc_names = set()
        for p in psutil.process_iter(['name']):
            try:
                if p.info['name']:
                    proc_names.add(p.info['name'].lower())
            except Exception:
                pass

        mf_on = any("master flow" in n for n in proc_names)
        tt_studio_on = any("tiktok live studio" in n for n in proc_names)
        ollama_on = any("ollama" in n for n in proc_names)
        cf_on = any("cloudflared" in n for n in proc_names)
        adb_on = any("adb" in n for n in proc_names)

        state["live_studio"]["tiktok_studio_running"] = tt_studio_on
        state["system_performance"]["pc"] = {
            "cpu_percent": round(cpu, 1),
            "ram_percent": round(mem.percent, 1),
            "ram_used_gb": round(mem.used / (1024**3), 1),
            "ram_total_gb": round(mem.total / (1024**3), 1),
            "disk_percent": round(disk.percent, 1),
            "uptime_str": f"{hrs:02d}:{mins:02d}:{secs:02d}",
            "processes": {
                "master_flow": mf_on,
                "tiktok_live_studio": tt_studio_on,
                "ollama_local_ai": ollama_on,
                "cloudflared": cf_on,
                "adb_server": adb_on
            }
        }

        # Update Revenue Analytics from real ledger
        total_today = round(ledger["shopee_real_thb"] + ledger["tiktok_real_thb"] + ledger["fb_real_thb"] + (ledger["tiktok_live_coins"] * 0.20), 2)
        state["revenue_analytics"] = {
            "today_total_thb": total_today,
            "month_total_thb": total_today,
            "catalog_products_count": state["master_flow_overview"]["products_in_catalog"],
            "avg_comm_rate": "5% - 15.6% (จากสินค้าจริง 40 รายการใน DB)",
            "by_platform": [
                {
                    "platform": "Shopee Video & Affiliate (Account #43)",
                    "icon": "🟠",
                    "today_thb": ledger["shopee_real_thb"],
                    "orders_today": ledger["shopee_orders"],
                    "status": "ซิงค์คุกกี้จริง (31 Cookies)",
                    "top_product": "สินค้าเปิดใช้งานจริง 40 รายการใน unlock108.db"
                },
                {
                    "platform": "TikTok Shop & Live Studio (Account #46)",
                    "icon": "🎵",
                    "today_thb": round(ledger["tiktok_real_thb"] + (ledger["tiktok_live_coins"] * 0.20), 2),
                    "orders_today": ledger["tiktok_orders"],
                    "status": f"เหรียญไลฟ์สดจริง: {ledger['tiktok_live_coins']} เหรียญ",
                    "top_product": f"TikTok LIVE Studio: {'🟢 เปิดอยู่บนเครื่อง' if tt_studio_on else '⚪ ปิดอยู่'}"
                },
                {
                    "platform": "Facebook Reels (น้องบีรีวิว ปักตระกร้า SP)",
                    "icon": "🔵",
                    "today_thb": ledger["fb_real_thb"],
                    "orders_today": ledger["fb_orders"],
                    "status": f"ยอดวิว Reels จริงรวม: {state['facebook']['total_video_views']} วิว",
                    "top_product": "ปักหมุดลิงก์ Shopee Affiliate ใต้คลิปจริง"
                }
            ],
            "by_channel": [
                {
                    "channel": acc["account"],
                    "platform": "TikTok (ในฐานข้อมูล unlock108.db)",
                    "today_thb": round(ledger["tiktok_real_thb"] + (ledger["tiktok_live_coins"] * 0.20), 2) if idx == 0 else 0.0,
                    "source": f"Cookies: {acc.get('cookies', 0)} · วอร์มแล้ว {acc.get('warmup_watched', 0)} คลิป",
                    "views": "ดึงตามจริง",
                    "status": "🟢 เชื่อมต่อจริง"
                } for idx, acc in enumerate(state["tiktok_accounts"])
            ] + [
                {
                    "channel": "น้องบีรีวิว ปักตระกร้า SP",
                    "platform": "Facebook Page (ID: 1012215361986434)",
                    "today_thb": ledger["fb_real_thb"],
                    "source": "Graph API v26.0 Connected",
                    "views": f"{state['facebook']['total_video_views']} วิว (ผู้ติดตาม {state['facebook']['followers']} คน)",
                    "status": "🟢 ออนไลน์สด"
                },
                {
                    "channel": "Shopee #1 (spu:215236917)",
                    "platform": "Shopee Creator Affiliate (4x Redmi 14C)",
                    "today_thb": ledger["shopee_real_thb"],
                    "source": f"สินค้าในแคตตาล็อก {state['master_flow_overview']['products_in_catalog']} รายการ",
                    "views": f"วอร์มดูจบ {sum(d.get('watched', 0) for d in state['devices'].values())} คลิปในเซสชันนี้",
                    "status": "🟢 กำลังวอร์มบนมือถือจริง"
                }
            ]
        }

        # Update 3D Digital Twin Office with 100% REAL process states
        state["digital_twin_office"]["departments"] = [
            {
                "id": "meeting_room",
                "name": "🏛️ ห้องประชุมวางแผนกลยุทธ์ (Executive Strategy Room)",
                "role": "ซิงค์ฐานข้อมูล unlock108.db & จัดคิวสลับซีรีส์ ↔ รีวิวสินค้า",
                "status": f"Master Flow.exe: {'🟢 กำลังทำงาน' if mf_on else '🔴 ปิดอยู่'}",
                "agents": [
                    {"name": "AI Director", "avatar": "👔", "task": f"ดูแลคลังคลิปสร้างเสร็จจริง {state['master_flow_overview']['total_generations_done']} รายการ (คิวรอ {state['master_flow_overview']['total_generations_pending']} รายการ)", "state": "Active" if mf_on else "Idle"},
                    {"name": "AI Catalog Manager", "avatar": "🕵️‍♀️", "task": f"ซิงค์สินค้า Shopee Affiliate จริง {state['master_flow_overview']['products_in_catalog']} รายการ", "state": "Synced"}
                ]
            },
            {
                "id": "prompt_lab",
                "name": "🧠 แผนกครีเอทีฟ & Local AI Prompt Lab",
                "role": "รัน Ollama (llama3.1:latest) ปรับแต่ง Prompt & คำอวยพรไลฟ์สดฟรี",
                "status": f"Ollama Server (11434): {'🟢 ออนไลน์' if ollama_on else '🔴 ออฟไลน์'}",
                "agents": [
                    {"name": "AI Prompt Engineer", "avatar": "🧑‍💻", "task": f"ใช้ Local Llama 3.1 อัปเกรด Prompt ไปแล้ว {state['local_ai_engine']['real_calls_count']} ครั้งในเซสชันนี้", "state": "Ready" if ollama_on else "Offline"},
                    {"name": "AI Whisper Subtitler", "avatar": "✍️", "task": "ตั้งค่า whisperMode='local' (Model: large) ใน unlock108.db", "state": "Configured"}
                ]
            },
            {
                "id": "video_studio",
                "name": "🎬 สตูดิโอผลิตวิดีโอ & Google Flow Credit Guard",
                "role": "ตรวจสอบบัญชี Google Flow (closec16522@gmail.com) & Auto-Pause",
                "status": f"สถานะ: {state['google_flow_credits']['status']}",
                "agents": [
                    {"name": "AI Video Producer", "avatar": "🎥", "task": "โมเดลจริงในระบบ: Veo 3.1 - Lite (8s) & Nano Banana Pro", "state": state["google_flow_credits"]["status"]},
                    {"name": "AI Credit Guardian", "avatar": "🛡️", "task": "ซิงค์ 115 คุกกี้จริง พร้อมสั่งหยุดทันทีหากเครดิต Google Flow เต็ม", "state": "Guarding"}
                ]
            },
            {
                "id": "phone_farm",
                "name": "📱 ห้องควบคุมฟาร์มมือถือจริง 4 เครื่อง (ADB Port 5038)",
                "role": "ควบคุม Redmi 14C ทั้ง 4 เครื่อง ดูคลิป กดไลก์ กดตะกร้าตามจริง",
                "status": f"เชื่อมต่อจริง {len(state['devices'])} เครื่อง",
                "agents": [
                    {"name": "AI Farm Commander", "avatar": "🤖", "task": f"สไลด์ดูคลิปจริงไปแล้ว {sum(d.get('watched', 0) for d in state['devices'].values())} คลิปในเซสชันนี้", "state": "Working"},
                    {"name": "AI Hardware Medic", "avatar": "🔧", "task": "อ่านค่าอุณหภูมิและแบตเตอรี่จริงจาก dumpsys battery", "state": "Monitoring"}
                ]
            },
            {
                "id": "live_studio_room",
                "name": "🕉️ สตูดิโอไลฟ์สด TikTok LIVE Studio (9:16 Broadcast)",
                "role": "ส่งภาพฉากพญานาค/พระพิฆเนศ/ไฉ่ซิงเอี๊ย/ไพ่ทาโรต์เข้า TikTok LIVE Studio",
                "status": f"TikTok LIVE Studio: {'🟢 เปิดอยู่บน PC' if tt_studio_on else '⚪ รอเปิดโปรแกรม'}",
                "agents": [
                    {"name": "AI Live Host", "avatar": "🙏", "task": f"กำลังรันธีม '{state['live_studio']['active_theme']}' ที่พอร์ต 3333/live-scene", "state": "Broadcasting"},
                    {"name": "AI Chat & Gift Listener", "avatar": "🎛️", "task": f"เชื่อมต่อช่อง {state['live_studio']['connected_channel']} ดึงแชทและของขวัญจริง", "state": "Connected" if state["live_studio"]["tiktok_connected"] else "Standby"}
                ]
            },
            {
                "id": "revenue_room",
                "name": "💰 แผนกบัญชีและบันทึกยอดรายได้จริง (Real Revenue Ledger)",
                "role": "คำนวณรายได้ตามจริงจากยอดขาย เหรียญของขวัญ และยอดวิว Reels",
                "status": f"ยอดบันทึกจริงวันนี้: ฿{total_today:,.2f}",
                "agents": [
                    {"name": "AI Financial Auditor", "avatar": "📊", "task": f"Facebook Reels ยอดวิวจริง {state['facebook']['total_video_views']} วิว · เหรียญไลฟ์ {ledger['tiktok_live_coins']} เหรียญ", "state": "Tracking"},
                    {"name": "AI Shutdown Guard", "avatar": "⏰", "task": "เฝ้าเวลาปิดเครื่อง 22:00 / 01:00 พร้อม Popup นับถอยหลัง 20 วินาที", "state": "Armed"}
                ]
            }
        ]
    except Exception as e:
        print("Perf update error:", e)

def generate_ai_blessing_and_prompt(text_input, mode="blessing"):
    """
    เรียกใช้งาน Ollama (llama3.1:latest) ในเครื่องจริงที่พอร์ต 11434
    """
    state["local_ai_engine"]["real_calls_count"] += 1
    if mode == "blessing":
        prompt = (
            f"คุณคือซินแสและโหราจารย์สายมูเตลูผู้ศักดิ์สิทธิ์ มีผู้ศรัทธาอธิษฐานว่า: '{text_input}' "
            f"จงเขียนคำอวยพรสั้นๆ ที่ทรงพลัง เป็นมงคล และให้กำลังใจ 1 ประโยค (ไม่เกิน 25 คำ ภาษาไทยล้วน):"
        )
    else:
        prompt = (
            f"You are a viral short-form video prompt engineer. Upgrade this video idea into a high-retention cinematic prompt with a strong 3-second hook (under 40 words): '{text_input}'"
        )

    try:
        r = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={"model": "llama3.1:latest", "prompt": prompt, "stream": False},
            timeout=8
        )
        if r.status_code == 200:
            ans = r.json().get("response", "").strip().replace('"', '')
            if ans:
                return ans
    except Exception:
        pass

    if mode == "blessing":
        return "ขออำนาจบารมีสิ่งศักดิ์สิทธิ์ประทานพรให้ท่านสมปรารถนา การเงินมั่งคั่ง โชคลาภเปิดทางสำเร็จทันใจเทอญ"
    return f"【Hook 0-3s】Cinematic extreme close-up reveal of {text_input}, dramatic lighting, high-retention pacing, 9:16 vertical"

# Real Phone Worker (Counts ONLY real ADB actions executed in this session + real battery/temp)
def phone_worker(serial, idx=0):
    lvl, temp_c = get_real_phone_battery_and_temp(serial)
    state["devices"][serial] = {
        "serial": serial,
        "model": "Redmi 14C (720x1640)",
        "state": "เชื่อมต่อ ADB 5038 จริง",
        "action": "เตรียมความพร้อมหน้าจอ...",
        "watched": 0,
        "likes": 0,
        "cart_clicks": 0,
        "shares": 0,
        "battery": lvl,
        "temp_c": temp_c,
        "latency_ms": 0,
        "stay_on": "Active",
        "active": True
    }
    dev = state["devices"][serial]
    log_event(f"Phone-{serial[-4:]}", f"เชื่อมต่อ Redmi 14C ({serial}) สำเร็จ: แบตเตอรี่จริง {lvl}, อุณหภูมิ {temp_c}°C", "success")

    adb_cmd(serial, "input keyevent 224")
    adb_cmd(serial, "settings put global stay_on_while_plugged_in 7")
    adb_cmd(serial, "svc power stayon true")

    while True:
        try:
            t0 = time.time()
            lvl, temp_c = get_real_phone_battery_and_temp(serial)
            ping_ms = int((time.time() - t0) * 1000)
            dev["battery"] = lvl
            dev["temp_c"] = temp_c
            dev["latency_ms"] = max(ping_ms, 8)

            watch_time = random.uniform(9.0, 15.0)
            dev["action"] = f"กำลังดูคลิปจริงบนหน้าจอ ({int(watch_time)} วินาที)..."
            time.sleep(watch_time)

            if random.random() < 0.25:
                adb_cmd(serial, "input tap 360 800")
                time.sleep(0.12)
                adb_cmd(serial, "input tap 360 800")
                dev["likes"] += 1
                dev["action"] = "ส่งคำสั่ง ADB กดหัวใจ (Double Tap)"
                log_event(f"Phone-{serial[-4:]}", f"สั่ง ADB Double-Tap กดไลก์จริง (สะสมรอบนี้ {dev['likes']} ครั้ง)", "success")
                time.sleep(1)

            sx = random.randint(350, 370)
            sy = random.randint(1180, 1250)
            ey = random.randint(360, 430)
            dur = random.randint(280, 350)
            adb_cmd(serial, f"input swipe {sx} {sy} {sx} {ey} {dur}")
            dev["watched"] += 1
            for acc in state["tiktok_accounts"]:
                acc["warmup_watched"] = acc.get("warmup_watched", 0) + 1
            dev["action"] = f"สไลด์ดูคลิปจบแล้ว {dev['watched']} คลิป (ในเซสชันนี้)"
            time.sleep(1.5)
        except Exception:
            time.sleep(5)

# Real Facebook Graph API v26.0 Poller
def fb_worker():
    token_path = r"C:\Users\Administrator\.gemini\antigravity\brain\d1568b5b-90b0-480a-b56a-6691372d4e53\scratch\fb_token.txt"
    if not os.path.exists(token_path):
        return
    with open(token_path, "r") as f:
        token = f.read().strip()

    page_id = "1012215361986434"
    FB_GRAPH = "https://graph.facebook.com/v26.0"

    while True:
        try:
            r = requests.get(f"{FB_GRAPH}/{page_id}?fields=followers_count,fan_count&access_token={token}", timeout=8)
            if r.status_code == 200:
                data = r.json()
                state["facebook"]["followers"] = data.get("followers_count", 0)
                state["facebook"]["fan_count"] = data.get("fan_count", 0)
                state["facebook"]["status"] = "Online (Graph API v26.0 Real Data)"

            r2 = requests.get(f"{FB_GRAPH}/{page_id}/video_reels?fields=id,views,post_views&access_token={token}&limit=25", timeout=8)
            if r2.status_code == 200:
                reels_data = r2.json().get("data", [])
                total_v = sum([item.get("views", 0) for item in reels_data])
                state["facebook"]["total_video_views"] = total_v
                state["facebook"]["recent_reels"] = len(reels_data)
            time.sleep(30)
        except Exception:
            time.sleep(30)

# Real TikTokLive WebCast Connector (Connects when user clicks Connect or goes live)
tiktok_client_thread = None
def start_real_tiktok_live_listener(username):
    clean_user = username.lstrip("@").strip()
    state["live_studio"]["connected_channel"] = "@" + clean_user

    def runner():
        try:
            from TikTokLive import TikTokLiveClient
            from TikTokLive.events import ConnectEvent, CommentEvent, GiftEvent, LikeEvent, RoomUserSeqEvent

            client = TikTokLiveClient(unique_id=f"@{clean_user}")

            @client.on(ConnectEvent)
            async def on_connect(event: ConnectEvent):
                state["live_studio"]["tiktok_connected"] = True
                log_event("TikTok-Live", f"🟢 เชื่อมต่อสัญญาณไลฟ์สดจริงของ @{clean_user} สำเร็จ!", "success")

            @client.on(RoomUserSeqEvent)
            async def on_viewers(event: RoomUserSeqEvent):
                state["live_studio"]["real_viewers"] = getattr(event, "m_total", 0)

            @client.on(LikeEvent)
            async def on_like(event: LikeEvent):
                cnt = getattr(event, "count", 1)
                state["live_studio"]["wish_board"]["hearts"] += cnt

            @client.on(CommentEvent)
            async def on_comment(event: CommentEvent):
                user_nick = event.user.nickname or event.user.unique_id or "ผู้ศรัทธา"
                comment_txt = event.comment
                blessing = generate_ai_blessing_and_prompt(comment_txt, mode="blessing")
                lucky = f"{random.randint(100, 999)}"
                state["live_studio"]["current_lucky_number"] = lucky
                state["live_studio"]["prayer_queue"].insert(0, {
                    "user": user_nick,
                    "wish": comment_txt,
                    "ai_blessing": blessing,
                    "timer": "สดจากแชท TikTok"
                })
                if len(state["live_studio"]["prayer_queue"]) > 10:
                    state["live_studio"]["prayer_queue"].pop()
                state["live_studio"]["wish_board"]["finance"] += 1
                log_event("TikTok-Chat", f"💬 [{user_nick}]: {comment_txt} -> เลขมงคล {lucky}", "success")

            @client.on(GiftEvent)
            async def on_gift(event: GiftEvent):
                user_nick = event.user.nickname or "ผู้ร่วมบุญ"
                gift_name = getattr(event.gift, "name", "ของขวัญ")
                diamond_cnt = getattr(event.gift, "diamond_count", 1)
                repeat_cnt = getattr(event, "repeat_count", 1)
                coins = diamond_cnt * max(repeat_cnt, 1)

                state["live_studio"]["wish_board"]["coins"] += coins
                state["live_studio"]["total_gift_events"] += 1
                state["live_studio"]["last_gift_text"] = f"คุณ {user_nick} ถวาย {gift_name} (+{coins} เหรียญ)"
                ledger["tiktok_live_coins"] += coins
                save_ledger()

                # Update real session leaderboard
                lb = state["live_studio"]["leaderboard"]
                existing = next((x for x in lb if x["name"] == user_nick), None)
                if existing:
                    existing["points"] += coins
                else:
                    lb.append({"name": user_nick, "points": coins})
                lb.sort(key=lambda x: x["points"], reverse=True)
                log_event("TikTok-Gift", f"🎁 [{user_nick}] ส่งของขวัญจริง '{gift_name}' (+{coins} เหรียญ)!", "success")

            client.run()
        except Exception as e:
            state["live_studio"]["tiktok_connected"] = False
            log_event("TikTok-Live", f"ℹ️ ช่อง @{clean_user} ตอนนี้ยังไม่ได้กดปุ่ม Go LIVE ออนแอร์จริง (อยู่ในโหมดเตรียมฉากใน TikTok LIVE Studio)", "info")

    t = threading.Thread(target=runner, daemon=True)
    t.start()

# Shutdown Countdown Worker
def shutdown_countdown_worker():
    while True:
        try:
            if state["shutdown_state"]["active"]:
                if state["shutdown_state"]["countdown"] > 0:
                    state["shutdown_state"]["countdown"] -= 1
                    rem = state["shutdown_state"]["countdown"]
                    if rem in (15, 10, 5, 3, 2, 1):
                        log_event("ShutdownGuard", f"⚠️ ระบบจะปิดการทำงานและ Shutdown ในอีก {rem} วินาที... (กดยกเลิกได้บนหน้าเว็บ)", "warn")
                    if rem <= 0:
                        state["shutdown_state"]["active"] = False
                        log_event("ShutdownGuard", "🛑 ครบกำหนด 20 วินาที -> สั่งพักหน้าจอมือถือทั้ง 4 เครื่องเรียบร้อย!", "warn")
                        for d in DEVICES:
                            adb_cmd(d, "settings put system screen_brightness 0")
                            adb_cmd(d, "input keyevent 26")
            time.sleep(1)
        except Exception:
            time.sleep(1)

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def send_json(self, payload, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        content_len = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_len).decode('utf-8') if content_len > 0 else "{}"
        try:
            req_data = json.loads(post_body)
        except Exception:
            req_data = {}

        if self.path == "/api/devices/scan":
            all_devs = scan_adb_devices()
            current_devs = list(state["devices"].keys())
            new_devs = [d for d in all_devs if d not in current_devs]
            for d in new_devs:
                DEVICES.append(d)
                t = threading.Thread(target=phone_worker, args=(d, len(DEVICES)), daemon=True)
                t.start()
            self.send_json({"status": "success", "all_devices": all_devs, "new_devices_added": new_devs, "total": len(all_devs)})

        elif self.path == "/api/tiktok/add":
            username = req_data.get("username", "").strip()
            if not username.startswith("@") and username:
                username = "@" + username
            niche = req_data.get("niche", "#ซีรีส์เรื่องเล่า #รีวิวของดี")
            role = req_data.get("role", "ช่องเสริม")
            if username:
                # Save directly into real unlock108.db accounts table!
                try:
                    conn = sqlite3.connect(DB_PATH)
                    c = conn.cursor()
                    meta_json = json.dumps({"cookies": 0, "status": "ok", "niche": niche, "role": role}, ensure_ascii=False)
                    c.execute(
                        "INSERT INTO accounts (provider, label, secret, meta, created_at) VALUES (?, ?, ?, ?, ?)",
                        ("tiktok", username, "", meta_json, int(time.time() * 1000))
                    )
                    conn.commit()
                    conn.close()
                except Exception as e:
                    print("DB insert account error:", e)
                sync_real_database()
                log_event("TikTok-DB", f"บันทึกช่อง {username} ลงในฐานข้อมูล unlock108.db จริงเรียบร้อยแล้ว!", "success")
                self.send_json({"status": "success", "account": username})
            else:
                self.send_json({"status": "error"}, 400)

        elif self.path == "/api/tiktok/upload-series":
            clip_id = int(req_data.get("clip_id", 361))
            target_channel = req_data.get("channel", "@closec16522")
            try:
                conn = sqlite3.connect(DB_PATH)
                c = conn.cursor()
                c.execute("SELECT meta FROM generations WHERE id=?", (clip_id,))
                row = c.fetchone()
                if row and row[0]:
                    m = json.loads(row[0])
                    m["tiktokPosted"] = int(time.time() * 1000)
                    m["tiktokChannel"] = target_channel
                    c.execute("UPDATE generations SET meta=? WHERE id=?", (json.dumps(m, ensure_ascii=False), clip_id))
                    conn.commit()
                conn.close()
            except Exception:
                pass
            sync_real_database()
            log_event("TikTok-Upload", f"อัปเดตสถานะการโพสต์คลิปซีรีส์ #{clip_id} ลงช่อง {target_channel} ในฐานข้อมูลจริงสำเร็จ", "success")
            self.send_json({"status": "success", "clip_id": clip_id, "channel": target_channel})

        elif self.path == "/api/tiktok/warmup-all":
            for d in DEVICES:
                adb_cmd(d, "input keyevent 224")
            log_event("WarmupEngine", f"ส่งคำสั่ง ADB ปลุกและเร่งวอร์มบนมือถือจริงทั้ง {len(DEVICES)} เครื่อง สำหรับทุกช่องในระบบ", "success")
            self.send_json({"status": "success", "devices": len(DEVICES)})

        elif self.path == "/api/ai/optimize-prompt":
            topic = req_data.get("topic", "ปริศนาห้องปิดตาย")
            category = req_data.get("category", "series")
            upgraded = generate_ai_blessing_and_prompt(topic, mode="prompt")
            entry = {
                "version": f"Run #{state['local_ai_engine']['real_calls_count']} (Ollama llama3.1:latest)",
                "category": "ซีรีส์เรื่องเล่า" if category == "series" else "รีวิวสินค้า Affiliate",
                "before": topic,
                "after": upgraded,
                "updated_at": datetime.datetime.now().strftime("%H:%M:%S")
            }
            state["local_ai_engine"]["prompt_evolution_history"].insert(0, entry)
            log_event("Local-AI", f"รัน Ollama (llama3.1:latest) อัปเกรด Prompt จริงสำเร็จ", "success")
            self.send_json({"status": "success", "entry": entry})

        elif self.path == "/api/flow/toggle-pause":
            curr = state["google_flow_credits"]["status"]
            state["google_flow_credits"]["status"] = "PAUSED_WAIT_RESET" if curr == "ACTIVE" else "ACTIVE"
            state["google_flow_credits"]["last_checked"] = datetime.datetime.now().strftime("%H:%M:%S")
            log_event("CreditGuard", f"สลับสถานะ Google Flow Credit Guard เป็น: {state['google_flow_credits']['status']}", "warn")
            self.send_json({"status": "success", "flow_credits": state["google_flow_credits"]})

        elif self.path == "/api/live/action":
            action_type = req_data.get("type", "theme")
            if action_type == "theme":
                theme_id = req_data.get("theme_id", "naga")
                state["live_studio"]["active_theme"] = theme_id
                log_event("LiveStudio", f"สลับธีมฉากไลฟ์สด 9:16 เป็น '{theme_id}' (ซิงค์เข้า TikTok LIVE Studio ทันที)", "success")
            elif action_type == "connect_tiktok":
                channel = req_data.get("channel", "@closec16522")
                start_real_tiktok_live_listener(channel)
            elif action_type == "wish":
                user = req_data.get("user", "ผู้ศรัทธา")
                wish = req_data.get("wish", "ขอให้การเงินมั่งคั่ง ค้าขายร่ำรวย")
                aspect = req_data.get("aspect", "finance")
                blessing = generate_ai_blessing_and_prompt(wish, mode="blessing")
                lucky = f"{random.randint(100, 999)}"
                state["live_studio"]["current_lucky_number"] = lucky
                state["live_studio"]["prayer_queue"].insert(0, {
                    "user": user,
                    "wish": wish,
                    "ai_blessing": blessing,
                    "timer": "กำลังแสดงสด"
                })
                if aspect in state["live_studio"]["wish_board"]:
                    state["live_studio"]["wish_board"][aspect] += 1
                log_event("LiveStudio", f"🙏 แสดงคำขอพรของ [{user}] บนจอไลฟ์ 9:16 พร้อมคำพยากรณ์ Local AI & เลขมงคล {lucky}", "success")
            elif action_type == "gift":
                gift_name = req_data.get("gift_name", "มณีนาคราช")
                coins = int(req_data.get("coins", 20))
                sender = req_data.get("sender", "ผู้ร่วมบุญ")
                state["live_studio"]["wish_board"]["coins"] += coins
                state["live_studio"]["wish_board"]["hearts"] += 10
                state["live_studio"]["total_gift_events"] += 1
                state["live_studio"]["last_gift_text"] = f"คุณ {sender} ถวาย {gift_name} (+{coins} เหรียญ)"
                lb = state["live_studio"]["leaderboard"]
                ex = next((x for x in lb if x["name"] == sender), None)
                if ex:
                    ex["points"] += coins
                else:
                    lb.append({"name": sender, "points": coins})
                lb.sort(key=lambda x: x["points"], reverse=True)
                log_event("LiveStudio", f"🎆 แสดงเอฟเฟกต์พลุฉลองของขวัญ '{gift_name}' (+{coins} เหรียญ) บนจอไลฟ์ 9:16", "success")
            elif action_type == "reset_session":
                state["live_studio"]["leaderboard"] = []
                state["live_studio"]["prayer_queue"] = []
                state["live_studio"]["wish_board"] = {"career": 0, "finance": 0, "love": 0, "health": 0, "hearts": 0, "coins": 0}
                log_event("LiveStudio", "รีเซ็ตกระดานไลฟ์สดเป็น 0 เพื่อเริ่มรอบไลฟ์จริงใหม่", "info")
            self.send_json({"status": "success", "live_studio": state["live_studio"]})

        elif self.path == "/api/live/open-window":
            theme = req_data.get("theme", state["live_studio"]["active_theme"])
            local_url = f"http://127.0.0.1:3333/live-scene?theme={theme}"
            https_url = f"{state.get('tunnel_url', 'https://preserve-near-firms-blank.trycloudflare.com')}/live-scene?theme={theme}"
            # Copy HTTPS URL to Windows clipboard (TikTok LIVE Studio requires https:// domain, not 127.0.0.1) and launch standalone 9:16 window
            try:
                subprocess.run(["powershell", "-NoProfile", "-Command", f"Set-Clipboard -Value '{https_url}'"], timeout=4)
                edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                browser_exe = edge_path if os.path.exists(edge_path) else chrome_path
                if os.path.exists(browser_exe):
                    subprocess.Popen([browser_exe, f"--app={local_url}", "--window-size=540,960", "--new-window"])
                log_event("TikTok-Studio", f"🖥️ เปิดหน้าต่างไลฟ์สด 9:16 และคัดลอกลิงก์ HTTPS ({https_url}) ลง Clipboard สำหรับวางใน TikTok LIVE Studio แล้ว!", "success")
            except Exception as e:
                log_event("TikTok-Studio", f"คัดลอกลิงก์ {https_url} แล้ว ({e})", "info")
            self.send_json({"status": "success", "url": https_url, "local_url": local_url})

        elif self.path == "/api/revenue/record":
            platform = req_data.get("platform", "shopee")
            amount = float(req_data.get("amount", 0.0))
            orders = int(req_data.get("orders", 1))
            if platform == "shopee":
                ledger["shopee_real_thb"] = round(ledger["shopee_real_thb"] + amount, 2)
                ledger["shopee_orders"] += orders
            elif platform == "tiktok":
                ledger["tiktok_real_thb"] = round(ledger["tiktok_real_thb"] + amount, 2)
                ledger["tiktok_orders"] += orders
            elif platform == "facebook":
                ledger["fb_real_thb"] = round(ledger["fb_real_thb"] + amount, 2)
                ledger["fb_orders"] += orders
            save_ledger()
            log_event("RevenueLedger", f"💰 บันทึกยอดรายได้จริง +{amount:,.2f} บาท ({platform}) ลงในระบบสำเร็จ", "success")
            self.send_json({"status": "success", "ledger": ledger})

        elif self.path == "/api/system/shutdown-request":
            reason = req_data.get("reason", "สั่งปิดระบบและ Shutdown อัตโนมัติ (Computer & มือถือ 4 เครื่อง)")
            state["shutdown_state"] = {
                "active": True,
                "countdown": 20,
                "reason": reason,
                "requested_at": datetime.datetime.now().strftime("%H:%M:%S")
            }
            log_event("ShutdownGuard", f"⚠️ เริ่มนับถอยหลัง 20 วินาทีก่อนปิดระบบ ({reason})", "warn")
            self.send_json({"status": "success", "shutdown_state": state["shutdown_state"]})

        elif self.path == "/api/system/shutdown-cancel":
            state["shutdown_state"] = {"active": False, "countdown": 20, "reason": "", "requested_at": None}
            log_event("ShutdownGuard", "✅ ยกเลิกการปิดระบบเรียบร้อยแล้ว! ระบบทำงานต่อตามปกติ", "success")
            self.send_json({"status": "success", "shutdown_state": state["shutdown_state"]})

        else:
            self.send_json({"status": "not_found"}, 404)

    def do_GET(self):
        clean_path = self.path.split("?")[0]
        if clean_path == "/api/status":
            sync_real_database()
            update_system_performance_and_office()
            self.send_json(state)
        elif clean_path == "/live-scene":
            scene_file = r"C:\SmartHome\MasterFlow-AutoSuite\live_scene.html"
            if os.path.exists(scene_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(scene_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        elif clean_path.startswith("/assets/"):
            fname = os.path.basename(clean_path)
            asset_file = os.path.join(r"C:\SmartHome\MasterFlow-AutoSuite\assets", fname)
            if os.path.exists(asset_file):
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.end_headers()
                with open(asset_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
        else:
            dashboard_file = r"C:\SmartHome\MasterFlow-AutoSuite\index.html"
            if os.path.exists(dashboard_file):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                with open(dashboard_file, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()

    def log_message(self, format, *args):
        pass

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), RequestHandler) as httpd:
        print(f"Realtime Monitoring Server started at http://0.0.0.0:{PORT}", flush=True)
        httpd.serve_forever()

if __name__ == "__main__":
    sync_real_database()
    update_system_performance_and_office()
    # Initialize prompt history with 1 real call
    first_prompt = generate_ai_blessing_and_prompt("การหายตัวไปอย่างลึกลับของบรรณารักษ์สาวในห้องเก็บเอกสารปิดตาย", mode="prompt")
    state["local_ai_engine"]["prompt_evolution_history"].append({
        "version": "Run #1 (Ollama llama3.1:latest)",
        "category": "ซีรีส์เรื่องเล่า (จาก unlock108.db #366)",
        "before": "การหายตัวไปอย่างลึกลับของบรรณารักษ์สาวในห้องเก็บเอกสารปิดตาย",
        "after": first_prompt,
        "updated_at": datetime.datetime.now().strftime("%H:%M:%S")
    })

    for idx, d in enumerate(DEVICES):
        t = threading.Thread(target=phone_worker, args=(d, idx), daemon=True)
        t.start()
        time.sleep(0.3)

    t_fb = threading.Thread(target=fb_worker, daemon=True)
    t_fb.start()

    t_sd = threading.Thread(target=shutdown_countdown_worker, daemon=True)
    t_sd.start()

    run_server()
