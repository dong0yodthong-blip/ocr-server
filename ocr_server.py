from flask import Flask, request
import os
import re
import numpy as np
import cv2
import easyocr

app = Flask(__name__)

# โหลด OCR ตอนเริ่มเซิร์ฟเวอร์
reader = easyocr.Reader(['th', 'en'], gpu=False)

@app.route("/")
def home():
    return "OCR Server is running!"

def clean_plate_text(text):
    text = text.replace(" ", "")
    text = text.replace("\n", "")
    text = text.strip()

    # เอาเฉพาะ ไทย อังกฤษ ตัวเลข
    text = re.sub(r'[^ก-๙A-Za-z0-9]', '', text)
    return text

@app.route("/ocr", methods=["POST"])
def ocr():
    try:
        if not request.data:
            return "NO_IMAGE", 400

        # แปลง bytes -> image
        npimg = np.frombuffer(request.data, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return "READ_IMAGE_FAIL", 400

        # ขยายภาพให้ OCR อ่านง่ายขึ้น
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        # แปลงเป็นขาวดำ
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # ลด noise
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # threshold
        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # OCR
        results = reader.readtext(th, detail=0)

        if not results:
            return "NOT_FOUND"

        best_text = ""
        for text in results:
            cleaned = clean_plate_text(text)
            if len(cleaned) >= 4:
                best_text = cleaned
                break

        if best_text == "":
            best_text = clean_plate_text(results[0])

        if best_text == "":
            return "NOT_FOUND"

        return best_text

    except Exception as e:
        print("OCR ERROR:", e)
        return "OCR_ERROR", 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)