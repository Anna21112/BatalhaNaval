from .conexao import conectar

def verificar_acerto(partida_id, jogador_id, linha, coluna):
    from .partidas import obter_jogadores_partida
    jogador1_id, jogador2_id = obter_jogadores_partida(partida_id)
    adversario = jogador2_id if int(jogador_id) == int(jogador1_id) else jogador1_id

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
        return True
    conn.close()
    return False

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