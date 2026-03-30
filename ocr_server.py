from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    with open("image.jpg", "wb") as f:
        f.write(request.data)   # 🔥 รับ raw ตรง ๆ
    return "OK", 200

@app.route('/image')
def image():
    if not os.path.exists("image.jpg"):
        return "No image yet", 404
    return send_file("image.jpg", mimetype='image/jpeg')

@app.route('/')
def home():
    return "Server is running", 200