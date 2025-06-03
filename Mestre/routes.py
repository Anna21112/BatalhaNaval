import logging
from flask import Blueprint, request, jsonify
from models import *
from utils import letra_para_indice
from models import criar_partida
from models import obter_jogadores_partida
from models import consultar_estado_partida

socketio = None  # Será atribuído no app.py

def set_socketio(sio):
    global socketio
    socketio = sio

bp = Blueprint('batalha_naval', __name__)

@bp.route('/')
def index():
    logging.info("Rota / acessada")
    return "Servidor está rodando!"

@bp.route('/criar_partida', methods=['POST'])
def criar_partida_route():
    logging.info("Rota /criar_partida acessada")
    dados = request.get_json()
    jogador1_id = dados.get('jogador1_id')
    jogador2_id = dados.get('jogador2_id')
    if not jogador1_id or not jogador2_id:
        logging.warning("IDs dos jogadores não informados na criação de partida")
        return jsonify({"status": "erro", "mensagem": "IDs dos jogadores são obrigatórios"}), 400

    partida_id = criar_partida(jogador1_id, jogador2_id)
    logging.info(f"Partida criada: {partida_id} (Jogador1: {jogador1_id}, Jogador2: {jogador2_id})")
    return jsonify({"status": "ok", "partida_id": partida_id}), 201

@bp.route('/cadastrar_jogador', methods=['POST'])
def cadastrar_jogador():
    logging.info("Rota /cadastrar_jogador acessada")
    dados = request.get_json()
    nome = dados.get('nome')
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    if not nome or not usuario or not senha:
        logging.warning("Dados obrigatórios não informados no cadastro de jogador")
        return jsonify({"status": "erro", "mensagem": "Dados obrigatórios"}), 400
    jogador_id = criar_jogador(nome, usuario, senha)
    logging.info(f"Jogador cadastrado: {jogador_id} ({usuario})")
    return jsonify({"status": "ok", "jogador_id": jogador_id}), 201

@bp.route('/login_jogador', methods=['POST'])
def login_jogador():
    logging.info("Rota /login_jogador acessada")
    dados = request.get_json()
    usuario = dados.get('usuario')
    senha = dados.get('senha')
    jogador = autenticar_jogador(usuario, senha)
    if not jogador:
        logging.warning(f"Tentativa de login inválida para usuário: {usuario}")
        return jsonify({"status": "erro", "mensagem": "Usuário ou senha inválidos"}), 401
    logging.info(f"Login realizado: {usuario} (ID: {jogador[0]})")
    return jsonify({"status": "ok", "jogador_id": jogador[0], "usuario": jogador[1]})

@bp.route('/jogada', methods=['POST'])
def receber_jogada():
    logging.info("Rota /jogada acessada")
    dados = request.get_json()
    partida_id = dados.get('partida_id') 
    jogador_id = dados.get('jogador_id')
    linha = dados.get('linha')
    coluna = dados.get('coluna')

    logging.info(f"Jogada recebida - partida_id: {partida_id}, jogador_id: {jogador_id}, linha: {linha}, coluna: {coluna}")

    if not partida_id:
        logging.warning("partida_id não informado na jogada")
        return jsonify({"status": "erro", "mensagem": "partida_id é obrigatório"}), 400
    
    estado = consultar_estado_partida(partida_id, jogador_id)
    status = estado["partida_status"] if estado else None
    if status == 'finalizada':
      return jsonify({"status": "erro", "mensagem": "A partida já foi finalizada!"}), 400

    # Converte letras para índices
    if isinstance(linha, str):
        linha = letra_para_indice(linha)

    # Validação extra
    valida, msg = jogada_valida(partida_id, jogador_id, linha, coluna)
    if not valida:
        logging.warning(f"Jogada inválida: {msg}")
        return jsonify({"status": "erro", "mensagem": msg}), 400
    
    # Verifica se é a vez do jogador
    if int(jogador_id) != int(vez_atual(partida_id)):
     logging.warning(f"Jogador {jogador_id} tentou jogar fora da sua vez na partida {partida_id}")
     return jsonify({"status": "erro", "mensagem": "Não é sua vez!"}), 403
    
    # Verifica o acerto ou erro
    resultado = verificar_acerto(partida_id, jogador_id, linha, coluna)

    jogador1_id, jogador2_id = obter_jogadores_partida(partida_id)
    adversario = jogador2_id if int(jogador_id) == int(jogador1_id) else jogador1_id

    # Salva a jogada no banco de dados
    registrar_jogada(partida_id, jogador_id, linha, coluna, resultado)

    # Mensagem amigável
    if resultado:
        mensagem = "Você acertou um navio!"
    else:
        mensagem = "Você errou o tiro."

    # Verifica se o adversário foi atingido
    jogador1_id, jogador2_id = obter_jogadores_partida(partida_id)
    adversario = jogador2_id if int(jogador_id) == int(jogador1_id) else jogador1_id
    fim = verificar_fim_de_jogo(partida_id, adversario)
    
    # Se fim de jogo, emite evento e não alterna mais a vez
    logging.info(f"verificar_fim_de_jogo: {fim} para partida {partida_id}, adversario {adversario}")
    if fim:
     logging.info(f"Fim de jogo na partida {partida_id}. Vencedor: {jogador_id}")
    # Atualiza status e vencedor no banco
     conn = conectar()
     cur = conn.cursor()
     cur.execute("UPDATE partidas SET status = ?, vencedor_id = ?, data_fim = CURRENT_TIMESTAMP WHERE id = ?", 
            ('finalizada', jogador_id, partida_id))
     conn.commit()
     conn.close()
     socketio.emit('fim_de_jogo', {'vencedor': jogador_id, 'partida_id': partida_id})
     return jsonify({"status": "ok", "resultado": resultado, "mensagem": mensagem, "Fim de jogo!": True}), 200
    
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

    return jsonify({"status": "ok", "resultado": resultado, "mensagem": mensagem}), 200

@bp.route('/estado_partida/<int:partida_id>/<int:jogador_id>', methods=['GET'])
def estado_partida(partida_id, jogador_id):
    logging.info(f"Rota /estado_partida/{partida_id}/{jogador_id} acessada")
    estado = consultar_estado_partida(partida_id, jogador_id)
    if not estado:
        logging.warning(f"Partida {partida_id} não encontrada para consulta de estado")
        return jsonify({"status": "erro", "mensagem": "Partida não encontrada"}), 404
    return jsonify({"status": "ok", **estado}), 200