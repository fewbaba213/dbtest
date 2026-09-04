import cv2
import sqlite3
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw, ImageFont

def get_user_from_db(user_id):
    """ดึงข้อมูลพนักงานจาก SQLite"""
    conn = sqlite3.connect('ppe_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, full_name, department FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def draw_thai_card(frame, user_info):
    """วาดการ์ดแสดงข้อมูลพนักงานภาษาไทยลงบนเฟรมวิดีโอ"""
    # 1. สร้างแถบพื้นหลังสีดำโปร่งแสง (Overlay Card) ด้านซ้ายบน
    h, w, _ = frame.shape
    card_w, card_h = 380, 180
    overlay = frame.copy()
    cv2.rectangle(overlay, (20, 20), (20 + card_w, 20 + card_h), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame) # ทำพื้นหลังให้จางลงเล็กน้อย
    cv2.rectangle(frame, (20, 20), (20 + card_w, 20 + card_h), (0, 255, 0), 2) # กรอบสีเขียว

    # 2. แปลงภาพเป็น PIL เพื่อพิมพ์ภาษาไทย
    img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # ดึงฟอนต์ภาษาไทยจาก Windows
    try:
        font_title = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 22)
        font_body = ImageFont.truetype("C:/Windows/Fonts/tahoma.ttf", 16)
    except:
        font_title = font_body = ImageFont.load_default()

    # 3. กำหนดข้อความที่จะแสดง
    if user_info:
        u_id, name, dept = user_info
        draw.text((35, 30), " [ ยืนยันตัวตนสำเร็จ ]", font=font_title, fill=(0, 255, 0))
        draw.text((35, 65), f"รหัสพนักงาน: {u_id}", font=font_body, fill=(255, 255, 255))
        draw.text((35, 90), f"ชื่อ-นามสกุล: {name}", font=font_body, fill=(255, 255, 255))
        draw.text((35, 115), f"แผนก: {dept}", font=font_body, fill=(255, 255, 255))
    else:
        draw.text((35, 30), " [ ไม่พบข้อมูลในระบบ ]", font=font_title, fill=(255, 0, 0))
        draw.text((35, 70), "กรุณาติดต่อเจ้าหน้าที่ดูแลระบบ", font=font_body, fill=(255, 255, 255))

    # 4. แปลงกลับเป็นภาพ OpenCV (BGR)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

# --- ตั้งค่าสตรีมกล้อง ---
camera_source = "http://192.168.1.5:4747/video"
cap = cv2.VideoCapture(camera_source)

print("เริ่มระบบสแกนข้อมูล... (กด 'q' เพื่อปิด)")

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        continue

    # สแกน QR Code
    detected_qrs = decode(frame)

    for qr in detected_qrs:
        qr_data = qr.data.decode('utf-8')

        # วาดกรอบสีเขียวรอบ QR Code
        pts = qr.polygon
        if len(pts) > 0:
            for j in range(len(pts)):
                cv2.line(frame, tuple(pts[j]), tuple(pts[(j+1) % len(pts)]), (0, 255, 0), 3)

        # ค้นหาข้อมูลใน SQLite
        user_info = get_user_from_db(qr_data)

        # วาดการ์ดแสดงข้อมูลพนักงานภาษาไทยลงบนวิดีโอ
        frame = draw_thai_card(frame, user_info)

    cv2.imshow("PPE Dashboard - User Verification", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()