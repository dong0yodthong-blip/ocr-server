from flask import Flask, request
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "OCR Server is running!"

@app.route("/ocr", methods=["POST"])
def ocr():
    # ตอนนี้จำลองผล OCR ก่อน
    if not request.data:
        return "NO_IMAGE", 400
    return "1กข1234"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)