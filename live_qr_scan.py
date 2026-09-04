import cv2
import sqlite3
import time
from pyzbar.pyzbar import decode

def get_user_from_db(user_id):
    """ดึงข้อมูลจาก SQLite"""
    conn = sqlite3.connect('ppe_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT full_name, department FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# URL สตรีมจาก DroidCam
camera_source = "http://192.168.1.5:4747/video"

print("กำลังเชื่อมต่อกล้อง Wi-Fi...")
cap = cv2.VideoCapture(camera_source)

# ให้เวลาระบบบัฟเฟอร์สัญญาณวิดีโอ 1 วินาที
time.sleep(1)

if not cap.isOpened():
    print("[!] ไม่สามารถเปิดสตรีมกล้องได้ กรุณาปิด Browser หรือแอปอื่นที่เปิดค้างไว้")
    exit()

print("เชื่อมต่อกล้องสำเร็จ! กำลังเปิดหน้าต่างสแกน... (กด 'q' เพื่อปิด)")

fail_count = 0

while True:
    ret, frame = cap.read()

    # ถ้ารับภาพไม่ได้ชั่วคราว ให้รอ retry ก่อน ไม่เพิ่งปิดโปรแกรมทันที
    if not ret or frame is None:
        fail_count += 1
        time.sleep(0.1)
        if fail_count > 30: # ถ้ารอนานเกิน 3 วินาทีแล้วยังไม่มีภาพ ค่อยตัด
            print("\n[!] สัญญาณกล้องขาดหาย")
            break
        continue
    
    # ถ้ารับภาพได้ปกติ 
    fail_count = 0

    # ใช้ pyzbar ถอดรหัส QR Code จากภาพ
    detected_qrs = decode(frame)

    for qr in detected_qrs:
        qr_data = qr.data.decode('utf-8')
        
        # วาดกรอบสีเขียวรอบ QR Code
        pts = qr.polygon
        if len(pts) > 0:
            for j in range(len(pts)):
                cv2.line(frame, tuple(pts[j]), tuple(pts[(j+1) % len(pts)]), (0, 255, 0), 3)

        print(f"[DETECTED] สแกนพบรหัส: '{qr_data}'")

        # ค้นหาข้อมูล SQLite
        user_info = get_user_from_db(qr_data)
        if user_info:
            text = f"PASS: {user_info[0]} ({user_info[1]})"
            color = (0, 255, 0)
        else:
            text = f"UNKNOWN ID: {qr_data}"
            color = (0, 0, 255)

        cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("PPE System - Live QR Scan (pyzbar)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()