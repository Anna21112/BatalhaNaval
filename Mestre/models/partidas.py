from .conexao import conectar
from .gerarNavios import gerar_navios_automaticamente

def criar_partida(jogador1_id, jogador2_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO partidas (jogador1_id, jogador2_id, vez_atual) VALUES (?, ?, ?)",
        (jogador1_id, jogador2_id, jogador1_id)
    )
    conn.commit()
    
    # Pega o id da partida recém-criada
    partida_id = cur.lastrowid
    conn.close()

    gerar_navios_automaticamente(partida_id, jogador1_id)
    gerar_navios_automaticamente(partida_id, jogador2_id)

    return partida_id

def obter_jogadores_partida(partida_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT jogador1_id, jogador2_id FROM partidas WHERE id = ?", (partida_id,))
    resultado = cur.fetchone()
    conn.close()
    return resultado if resultado else (None, None)

def vez_atual(partida_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("SELECT vez_atual FROM partidas WHERE id = ?", (partida_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else 1

def consultar_estado_partida(partida_id, jogador_id):
    conn = conectar()
    cur = conn.cursor()

    cur.execute("SELECT status, vez_atual, vencedor_id FROM partidas WHERE id = ?", (partida_id,))
    partida = cur.fetchone()
    if not partida:
        conn.close()
        return None
    status, vez_atual, vencedor_id = partida

    vencedor_nome = None
    if vencedor_id is not None:
        cur.execute("SELECT nome FROM jogadores WHERE id = ?", (vencedor_id,))
        row = cur.fetchone()
        if row:
            vencedor_nome = row[0]

    cur.execute("SELECT linha, coluna, tamanho, orientacao, atingido FROM navios WHERE partida_id = ? AND jogador_id = ?", (partida_id, jogador_id))
    navios = [
        {"linha": linha, "coluna": coluna, "tamanho": tamanho, "orientacao": orientacao, "atingido": bool(atingido)}
        for linha, coluna, tamanho, orientacao, atingido in cur.fetchall()
    ]

    cur.execute("SELECT jogador_id, linha, coluna, resultado FROM jogadas WHERE partida_id = ?", (partida_id,))
    jogadas = [
        {"jogador_id": j_id, "linha": linha, "coluna": coluna, "resultado": resultado}
        for j_id, linha, coluna, resultado in cur.fetchall()
    ]

    conn.close()
    print("DEBUG vencedor_id:", vencedor_id, "vencedor_nome:", vencedor_nome)
    
    return {
        "partida_status": status,
        "vez_atual": vez_atual,
        "vencedor_id": vencedor_id,
        "vencedor_nome": vencedor_nome,
        "navios": navios,
        "jogadas": jogadas
    }

def jogada_valida(partida_id, jogador_id, linha, coluna):
    # Verifica se está dentro do tabuleiro
    if not (0 <= linha < 10) or not (0 <= coluna < 10):
        return False, "Jogada fora do tabuleiro"

    # Verifica se a célula já foi jogada POR ESTE JOGADOR
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "SELECT 1 FROM jogadas WHERE partida_id = ? AND jogador_id = ? AND linha = ? AND coluna = ?",
        (partida_id, jogador_id, linha, coluna)
    )
    existe = cur.fetchone()
    conn.close()
    if existe:
        return False, "Esta célula já foi jogada por você"
    return True, ""

def atualizar_vez(partida_id, novo_jogador_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute("UPDATE partidas SET vez_atual = ? WHERE id = ?", (novo_jogador_id, partida_id))
    conn.commit()
    conn.close()

