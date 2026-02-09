# Author: @SuryaPrabhas
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.utils import secure_filename
import os
import qrcode
import socket
import time
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Global State
text_data = "Welcome to Gesture Drop!"
image_filename = ""
history = []  # List of {text, time}

@app.route('/')
def index():
    return render_template('mobile_view.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global image_filename
    message = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('upload.html', message="No file part")
        file = request.files['file']
        if file.filename == '':
            return render_template('upload.html', message="No selected file")
        
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_filename = filename
        message = f"✅ Uploaded: {filename}"
        
    return render_template('upload.html', message=message)

@app.route('/save', methods=['POST'])
def save():
    global text_data, history
    data = request.get_json()
    new_text = data.get("text", "")
    
    if new_text and new_text != text_data:
        text_data = new_text
        timestamp = datetime.now().strftime("%H:%M:%S")
        history.insert(0, {"text": text_data, "time": timestamp})
        history = history[:5]  # Keep last 5 items
        print(f"[✅] Text Saved: {text_data}")
        
    return jsonify({"status": "success"})

@app.route('/get', methods=['GET'])
def get():
    return jsonify({
        "text": text_data,
        "image": image_filename
    })

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify({"history": history})

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    ip = get_ip_address()
    port = 5000
    url = f"http://{ip}:{port}"

    # Try to fetch Ngrok URL automatically or prompt user
    public_url = ""
    try:
        import requests
        import json
        print("\n[⏳] Attempting to auto-detect Ngrok URL...")
        response = requests.get("http://127.0.0.1:4040/api/tunnels", timeout=2)
        data = json.loads(response.text)
        public_url = data['tunnels'][0]['public_url']
        print(f"[✅] Auto-detected URL: {public_url}")
    except Exception:
        print("[⚠️] Could not auto-detect Ngrok URL (Tunnel API not reachable)")
        print("\n" + "!"*60)
        print("ACTION REQUIRED: Check the 'Gesture Drop Tunnel' window!")
        print("Copy the forwarding URL (e.g., https://xxxx-xx.ngrok-free.app)")
        print("!"*60 + "\n")
        public_url = input("👉 Paste the Ngrok URL here: ").strip()

    if not public_url.startswith("http"):
        # Add https if missing, though user should paste full url
        if not public_url:
             public_url = f"http://{ip}:{port}" # Fallback to local
        elif "ngrok" in public_url:
             public_url = "https://" + public_url if not public_url.startswith("http") else public_url
    
    # Generate QR Code
    qr = qrcode.QRCode(box_size=10, border=4)
    qr.add_data(public_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("static/qrcode.png")

    print("\n" + "="*50)
    print(f"🚀 GESTURE DROP SERVER RUNNING")
    print(f"📱 MOBILE URL: {public_url}")
    print(f"📷 SCAN QR CODE: Saved to static/qrcode.png")
    print("="*50)
    print("\n[ℹ️] TIPS FOR MOBILE CONNECTION:")
    print("1. If you see 'Connection Not Private' or 'Dangerous Site':")
    print("   -> Click 'Advanced' -> 'Proceed to ... (unsafe)'")
    print("2. Ensure your phone and PC are connected to the internet.")
    print("="*50 + "\n")

    app.run(host='0.0.0.0', port=port)
