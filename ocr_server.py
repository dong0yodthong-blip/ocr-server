from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    file.save("image.jpg")
    return "OK"

@app.route('/image')
def image():
    return send_file("image.jpg", mimetype='image/jpeg')

app.run(host='0.0.0.0', port=10000)