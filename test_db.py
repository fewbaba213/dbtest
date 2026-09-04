import sqlite3

# 1. เชื่อมต่อ (ถ้ายังไม่มีไฟล์ มันจะสร้างไฟล์ ppe_system.db ให้เองอัตโนมัติ)
conn = sqlite3.connect('ppe_system.db')
cursor = conn.cursor()

# 2. สร้างตารางพนักงาน (users) และตารางประวัติ (ppe_logs)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        department TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ppe_logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT
    )
''')

# ใส่ข้อมูลพนักงาน
cursor.execute("INSERT OR REPLACE INTO users VALUES ('EMP-001', 'เดชาธร เปรมประเสริฐ', 'แผนกคอมพิวเตอร์')")
cursor.execute("INSERT INTO ppe_logs (user_id, status) VALUES ('EMP-001', 'PASS')")

# 4. บันทึกข้อมูลและปิดการเชื่อมต่อ
conn.commit()
conn.close()

print("สร้าง Database และทดสอบใส่ข้อมูลเรียบร้อย!")