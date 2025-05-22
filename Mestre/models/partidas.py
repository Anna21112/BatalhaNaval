from .conexao import conectar

def vez_atual(partida_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT vez_atual FROM partidas WHERE id = ?", (partida_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 1

def atualizar_vez(partida_id, novo_jogador_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE partidas SET vez_atual = ? WHERE id = ?", (novo_jogador_id, partida_id))
    conn.commit()
    conn.close()