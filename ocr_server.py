from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "OCR Server is running!"

# 👇 เพิ่มอันนี้เข้าไป
@app.route("/ocr", methods=["POST"])
def ocr():
    return "1234TEST"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)