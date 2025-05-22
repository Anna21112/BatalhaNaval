from .conexao import conectar

def registrar_jogada(partida_id, jogador_id, linha, coluna, resultado):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO jogadas (partida_id, jogador_id, linha, coluna, resultado) VALUES (?, ?, ?, ?, ?)",
        (partida_id, jogador_id, linha, coluna, resultado)
    )
    conn.commit()
    conn.close()