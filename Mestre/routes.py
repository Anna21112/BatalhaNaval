from flask import Blueprint, request, jsonify
from models import *
from utils import letra_para_indice
from models import criar_partida

socketio = None  # Será atribuído no app.py

bp = Blueprint('batalha_naval', __name__)




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

@bp.route('/cadastrar_jogador', methods=['POST'])
def cadastrar_jogador():
    dados = request.get_json()
    nome = dados.get('nome')
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    if not nome or not usuario or not senha:
        return jsonify({"status": "erro", "mensagem": "Dados obrigatórios"}), 400
    jogador_id = criar_jogador(nome, usuario, senha)
    return jsonify({"status": "ok", "jogador_id": jogador_id}), 201

@bp.route('/login_jogador', methods=['POST'])
def login_jogador():
    dados = request.get_json()
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    jogador = autenticar_jogador(usuario, senha)
    if not jogador:
        return jsonify({"status": "erro", "mensagem": "Usuário ou senha inválidos"}), 401
    return jsonify({"status": "ok", "jogador_id": jogador[0], "usuario": jogador[1]})


@bp.route('/jogada', methods=['POST'])
def receber_jogada():
    dados = request.get_json()
    partida_id = dados.get('partida_id') 
    jogador_id = dados.get('jogador_id')
    linha = dados.get('linha')
    coluna = dados.get('coluna')

    if not partida_id:
        return jsonify({"status": "erro", "mensagem": "partida_id é obrigatório"}), 400

    # Converte letras para índices
    if isinstance(linha, str):
        linha = letra_para_indice(linha)

     # Validação extra
    valida, msg = jogada_valida(partida_id, linha, coluna)
    if not valida:
        return jsonify({"status": "erro", "mensagem": msg}), 400
     
    # Verifica se é a vez do jogador
    if jogador_id != vez_atual(partida_id):
        return jsonify({"status": "erro", "mensagem": "Não é sua vez!"}), 403
    
    # Verifica o acerto ou erro
    resultado = verificar_acerto(partida_id, jogador_id, linha, coluna)
    
    # Salva a jogada no banco de dados
    registrar_jogada(partida_id, jogador_id, linha, coluna, resultado)

    # Verifica se o adversário foi atingido
    adversario = 2 if jogador_id == 1 else 1
    fim = verificar_fim_de_jogo(partida_id, adversario)
    
    # Se fim de jogo, emite evento e não alterna mais a vez
    if fim:
        socketio.emit('fim_de_jogo', {'vencedor': jogador_id, 'partida_id': partida_id})
        return jsonify({"status": "ok", "resultado": resultado, "Fim de jogo!": True}), 200
    
    # Alterna a vez para o adversário
    atualizar_vez(partida_id, adversario)

    # Emite evento de nova jogada para os jogadores
    socketio.emit("nova_jogada", {
        'partida_id': partida_id,
        'jogador_id': jogador_id,
        'linha': linha,
        'coluna': coluna,
        'resultado': resultado
    })

    return jsonify({"status": "ok", "resultado": resultado}), 200

@bp.route('/estado_partida/<int:partida_id>/<int:jogador_id>', methods=['GET'])
def estado_partida(partida_id, jogador_id):
    estado = consultar_estado_partida(partida_id, jogador_id)
    if not estado:
        return jsonify({"status": "erro", "mensagem": "Partida não encontrada"}), 404
    return jsonify({"status": "ok", **estado}), 200

