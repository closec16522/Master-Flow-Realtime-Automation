import sqlite3
import json

db_path = r"C:\Users\Administrator\AppData\Roaming\flow-automation\unlock108.db"
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cur.fetchall()]
print("Tables in unlock108.db:")
for t in tables:
    cur.execute(f"SELECT count(*) FROM {t}")
    cnt = cur.fetchone()[0]
    print(f"  - {t}: {cnt} rows")

print("\n--- Recent generations ---")
cur.execute("SELECT id, status, prompt, created_at, updated_at FROM generations ORDER BY id DESC LIMIT 5")
for r in cur.fetchall():
    print("Gen:", r)

print("\n--- Accounts ---")
cur.execute("SELECT id, provider, label, meta FROM accounts")
for r in cur.fetchall():
    print("Account:", r)

print("\n--- Settings (first 10) ---")
cur.execute("SELECT key, value FROM settings LIMIT 10")
for r in cur.fetchall():
    print(f"Setting {r[0]}: {r[1][:80] if r[1] else ''}")
