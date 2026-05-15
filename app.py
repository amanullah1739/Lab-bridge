# from flask import Flask, render_template, url_for
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import random
import string
import qrcode
import os
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

# Store sessions temporarily
sessions = {}

# Generate random session ID
def generate_session_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def generate_qr(session_id, base_url):

    url = f"{base_url}session/{session_id}"

    qr = qrcode.make(url)

    buffer = io.BytesIO()

    qr.save(buffer, format="PNG")

    buffer.seek(0)

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return qr_base64

@app.route('/')
def home():

    session_id = generate_session_id()
    

    sessions[session_id] = {
        "text": ""
    }

    base_url = request.host_url

    qr_code = generate_qr(session_id, base_url)

    return render_template(
        'index.html',
        session_id=session_id,
        qr_code=qr_code
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



    