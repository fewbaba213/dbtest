import cv2

# รายการช่องสัญญาณกล้องที่ระบบจะลองทดสอบ
test_sources = [
    0, 
    1, 
    2, 
    "http://192.168.1.5:4747/mjpegfeed",
    "http://192.168.1.5:4747/video",
    "http://192.168.1.5:8080/video"
]

working_source = None

print("กำลังค้นหาสัญญาณกล้อง...")

for src in test_sources:
    cap = cv2.VideoCapture(src)
    ret, frame = cap.read()
    if ret and frame is not None and frame.shape[0] > 0:
        print(f" SUCCESS! พบกล้องที่ใช้งานได้ที่ช่อง: {src}")
        working_source = src
        cap.release()
        break
    else:
        print(f" Connection failed: {src}")
    cap.release()

if working_source is None:
    print("\n[!] ไม่พบกล้องในระบบเลย กรุณาเช็กว่าเปิดแอป DroidCam บนมือถือแล้วหรือยัง")