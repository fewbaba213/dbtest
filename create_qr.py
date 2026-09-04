import qrcode

# รหัสพนักงานที่จะฝังใน QR Code
user_id = "EMP-002"

# สร้าง QR Code
img = qrcode.make(user_id)
img.save("EMP-002_qr.png")

print(f"สร้างไฟล์ QR Code สำหรับ {user_id} เรียบร้อย: EMP-002_qr.png")