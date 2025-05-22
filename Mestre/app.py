from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from models import ( registrar_jogada, verificar_acerto, vez_atual, atualizar_vez, verificar_fim_de_jogo, init_db
)
from routes import bp, socketio as bp_socketio

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Injeta o socketio no blueprint
bp_socketio = socketio

app.register_blueprint(bp)

if __name__ == '__main__':
    init_db()
    socketio.run(app, host='0.0.0.0', port=5000)