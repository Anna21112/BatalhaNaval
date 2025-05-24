from .conexao import conectar
import bcrypt

def criar_jogador(nome, usuario, senha):
    conn = conectar()
    cur = conn.cursor()
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    cur.execute("INSERT INTO jogadores (nome, usuario, senha) VALUES (?, ?, ?)", (nome, usuario, senha_hash))
    conn.commit()
    jogador_id = cur.lastrowid
    conn.close()
    return jogador_id

def autenticar_jogador(usuario, senha):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT id, usuario, senha FROM jogadores WHERE usuario = ?", (usuario,))
    jogador = cur.fetchone()
    conn.close()
    if jogador and bcrypt.checkpw(senha.encode('utf-8'), jogador[2]):
        return jogador[:2]  # retorna id e usuario
    return None

def buscar_jogador_por_usuario(usuario):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jogadores WHERE usuario = ?", (usuario,))
    jogador = cur.fetchone()
    conn.close()
    return jogador