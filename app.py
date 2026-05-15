# from flask import Flask, render_template, url_for
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import random
import string
import qrcode
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

# Store sessions temporarily
sessions = {}

# Generate random session ID
def generate_session_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Generate QR code
# def generate_qr(session_id):
#     url = f"http://192.168.1.12:5000/session/{session_id}"

#     qr = qrcode.make(url)

#     path = f"static/qr/{session_id}.png"

#     qr.save(path)

#     return path
# def generate_qr(session_id, base_url):

#     url = f"{base_url}session/{session_id}"

#     qr = qrcode.make(url)

#     path = f"static/qr/{session_id}.png"

#     qr.save(path)

#     return path
def generate_qr(session_id, base_url):

    url = f"{base_url}session/{session_id}"

    qr = qrcode.make(url)

    folder_path = "static/qr"

    # Create folder if not exists
    os.makedirs(folder_path, exist_ok=True)

    path = f"{folder_path}/{session_id}.png"

    qr.save(path)

    return path

@app.route('/')
def home():

    session_id = generate_session_id()
    

    sessions[session_id] = {
        "text": ""
    }

    base_url = request.host_url

    qr_path = generate_qr(session_id, base_url)

    return render_template(
        'index.html',
        session_id=session_id,
        qr_path=qr_path
    )

@app.route('/session/<session_id>')
def session(session_id):

    return render_template(
        'session.html',
        session_id=session_id
    )

@socketio.on('send_text')
def handle_send_text(data):

    session_id = data['session_id']
    text = data['text']

    sessions[session_id]["text"] = text

    socketio.emit(
        'receive_text',
        {
            "text": text
        }
    )
    
    
if __name__ == '__main__':
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True
    )



    