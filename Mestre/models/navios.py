from .conexao import conectar

def verificar_acerto(partida_id, jogador_id, linha, coluna):
    adversario = 2 if jogador_id == 1 else 1
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM navios WHERE partida_id = ? AND jogador_id = ? AND linha = ? AND coluna = ? AND atingido = 0",
        (partida_id, adversario, linha, coluna)
    )
    navio = cur.fetchone()
    if navio:
        cur.execute("UPDATE navios SET atingido = 1 WHERE id = ?", (navio[0],))
        conn.commit()
        conn.close()
        return "acerto"
    conn.close()
    return "erro"

def verificar_fim_de_jogo(partida_id, jogador_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM navios WHERE partida_id = ? AND jogador_id = ? AND atingido = 0",
        (partida_id, jogador_id)
    )
    restantes = cur.fetchone()[0]
    conn.close()
    return restantes == 0