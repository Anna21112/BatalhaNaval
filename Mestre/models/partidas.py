from .conexao import conectar
from .navios import gerar_navios_automaticamente

def criar_partida(jogador1_id, jogador2_id):
    conn = conectar()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO partidas (jogador1_id, jogador2_id) VALUES (?, ?)",
        (jogador1_id, jogador2_id)
    )
    conn.commit()
    
    # Pega o id da partida recém-criada
    partida_id = cur.lastrowid
    conn.close()

    gerar_navios_automaticamente(partida_id, jogador1_id)
    gerar_navios_automaticamente(partida_id, jogador2_id)

    return partida_id

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