from flask import Blueprint, request, jsonify
from models import ( registrar_jogada, verificar_acerto, vez_atual, atualizar_vez, verificar_fim_de_jogo, init_db,)
from utils import letra_para_indice
from models import criar_partida

socketio = None  # Será atribuído no app.py

bp = Blueprint('batalha_naval', __name__)

PARTIDA_ID = 1



@bp.route('/')
def index():
    return "Servidor está rodando!"

@bp.route('/criar_partida', methods=['POST'])
def criar_partida_route():
    dados = request.get_json()
    jogador1_id = dados.get('jogador1_id')
    jogador2_id = dados.get('jogador2_id')
    if not jogador1_id or not jogador2_id:
        return jsonify({"status": "erro", "mensagem": "IDs dos jogadores são obrigatórios"}), 400

    partida_id = criar_partida(jogador1_id, jogador2_id)
    return jsonify({"status": "ok", "partida_id": partida_id}), 201

@bp.route('/jogada', methods=['POST'])
def receber_jogada():
    dados = request.get_json()
    jogador_id = dados.get('jogador_id')
    linha = dados.get('linha')
    coluna = dados.get('coluna')
    
    # Converte letras para índices
    if isinstance(linha, str):
        linha = letra_para_indice(linha)
     
    # Verifica se é a vez do jogador
    if jogador_id != vez_atual(PARTIDA_ID):
        return jsonify({"status": "erro", "mensagem": "Não é sua vez!"}), 403
    
    # Verifica o acerto ou erro
    resultado = verificar_acerto(PARTIDA_ID, jogador_id, linha, coluna)
    
    # Salva a jogada no banco de dados
    registrar_jogada(PARTIDA_ID, jogador_id, linha, coluna, resultado)

    # Verifica se o adversário foi atingido
    adversario = 2 if jogador_id == 1 else 1
    fim = verificar_fim_de_jogo(PARTIDA_ID, adversario)
    
    # Se fim de jogo, emite evento e não alterna mais a vez
    if fim:
        socketio.emit('fim_de_jogo', {'vencedor': jogador_id})
        return jsonify({"status": "ok", "resultado": resultado,"Fim de jogo!": True}), 200
    
    #Alterna a vez para o adversário
    atualizar_vez(PARTIDA_ID, adversario)

    #Emite evento de nova jogada para os jogadores
    socketio.emit("nova_jogada", {
    'jogador_id': jogador_id,
        'linha': linha,
        'coluna': coluna,
        'resultado': resultado
    })

    return jsonify({"status": "ok", "resultado": resultado}), 200