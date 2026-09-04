import cv2
import sqlite3

def get_user_from_db(user_id):
    """ค้นหาข้อมูลพนักงานใน SQLite ด้วย user_id"""
    conn = sqlite3.connect('ppe_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, department FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# 1. โหลดรูปภาพ QR Code ที่สร้างไว้ (จำลองเฟรมภาพจากกล้อง)
image_path = "EMP-001_qr.png"
img = cv2.imread(image_path)

# 2. ใช้ QRCodeDetector ของ OpenCV อ่านข้อมูลในภาพ
detector = cv2.QRCodeDetector()
qr_data, bbox, _ = detector.detectAndDecode(img)

# 3. ถ้าอ่านค่าได้ ให้เอาค่าไปคิวรีใน Database
if qr_data:
    print(f"==========================================")
    print(f" [SCAN SUCCESS] พบ QR Code รหัส: {qr_data}")
    
    user_info = get_user_from_db(qr_data)
    if user_info:
        print(f" [USER FOUND]   ชื่อ: {user_info[0]}")
        print(f"                แผนก: {user_info[1]}")
        print(f" STATUS: พร้อมเข้าสู่ขั้นตอนสแกนอุปกรณ์ PPE")
    else:
        print(f" [WARNING] ไม่พบข้อมูลรหัส {qr_data} ในระบบ!")
    print(f"==========================================")
else:
    print("ไม่พบ QR Code ในภาพที่นำมาสแกน")