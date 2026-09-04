import sqlite3

def get_user_info(qr_data):
    """1. ค้นหาพนักงานจากรหัส QR Code"""
    conn = sqlite3.connect('ppe_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, department FROM users WHERE user_id = ?", (qr_data,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return f"พบข้อมูล: {result[0]} ({result[1]})"
    return "ไม่พบข้อมูลพนักงานในระบบ"

def log_ppe_check(user_id, status):
    """2. บันทึกผลการตรวจ PPE"""
    conn = sqlite3.connect('ppe_system.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ppe_logs (user_id, status) VALUES (?, ?)", (user_id, status))
    conn.commit()
    conn.close()
    print(f"บันทึกผลการตรวจ [{status}] สำหรับ {user_id} สำเร็จ")

def show_all_logs():
    """3. แสดงประวัติการตรวจทั้งหมด (JOIN ตาราง users และ ppe_logs)"""
    conn = sqlite3.connect('ppe_system.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT ppe_logs.log_id, users.full_name, ppe_logs.timestamp, ppe_logs.status
        FROM ppe_logs
        JOIN users ON ppe_logs.user_id = users.user_id
    ''')
    logs = cursor.fetchall()
    conn.close()
    
    print("\n--- ประวัติการเข้าตรวจทั้งหมด ---")
    for log in logs:
        print(f"Log ID: {log[0]} | ชื่อ: {log[1]} | เวลา: {log[2]} | ผล: {log[3]}")

# --- ทดลองรันระบบจำลอง ---
print(get_user_info('EMP-001'))  # ลองค้นหาพนักงานรหัส EMP-001
log_ppe_check('EMP-001', 'FAIL') # จำลองตรวจรอบใหม่แล้วได้ FAIL
show_all_logs()                  # แสดงรายงานสรุป