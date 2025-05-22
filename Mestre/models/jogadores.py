from .conexao import conectar

def criar_jogador(nome, usuario):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("INSERT INTO jogadores (nome, usuario) VALUES (?, ?)", (nome, usuario))
    conn.commit()
    jogador_id = cur.lastrowid
    conn.close()
    return jogador_id

def buscar_jogador_por_usuario(usuario):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT * FROM jogadores WHERE usuario = ?", (usuario,))
    jogador = cur.fetchone()
    conn.close()
    return jogador