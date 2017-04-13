from flask import Flask, render_template, request
from flask_socketio import SocketIO
from flask_cors import CORS
import webbrowser
from detector import myThread

async_mode = None
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
app.config.update(TEMPLATES_AUTO_RELOAD=True)
socketio = SocketIO(app, async_mode=async_mode)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


if __name__ == '__main__':
    t = myThread(socketio)
    t.start()
    webbrowser.open('http://localhost:25005/', autoraise=True)
    socketio.run(app, host='0.0.0.0', port=25005)
    t.join()