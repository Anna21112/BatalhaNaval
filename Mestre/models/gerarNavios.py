import random
from .conexao import conectar

TABULEIRO_TAMANHO = 10

def posicao_valida(tabuleiro, linha, coluna, tamanho, orientacao):
    #Verifica se o navio cabe e não sobrepõe outro.
    if orientacao == 'H':
        if coluna + tamanho > TABULEIRO_TAMANHO:
            return False
        for i in range(tamanho):
            if tabuleiro[linha][coluna + i]:
                return False
    else:  # 'V'
        if linha + tamanho > TABULEIRO_TAMANHO:
            return False
        for i in range(tamanho):
            if tabuleiro[linha + i][coluna]:
                return False
    return True

def marcar_navio(tabuleiro, linha, coluna, tamanho, orientacao):
    #Marca as posições ocupadas pelo navio no tabuleiro.
    if orientacao == 'H':
        for i in range(tamanho):
            tabuleiro[linha][coluna + i] = True
    else:
        for i in range(tamanho):
            tabuleiro[linha + i][coluna] = True

def gerar_navios_automaticamente(partida_id, jogador_id):
    navios = [(3, 1), (2, 2), (1, 3)]  # (tamanho, quantidade)
    tabuleiro = [[False for _ in range(TABULEIRO_TAMANHO)] for _ in range(TABULEIRO_TAMANHO)]
    conn = conectar()
    cur = conn.cursor()

    for tamanho, quantidade in navios:
        for _ in range(quantidade):
            colocado = False
            tentativas = 0
            while not colocado and tentativas < 100:
                linha = random.randint(0, TABULEIRO_TAMANHO - 1)
                coluna = random.randint(0, TABULEIRO_TAMANHO - 1)
                orientacao = random.choice(['H', 'V'])
                if posicao_valida(tabuleiro, linha, coluna, tamanho, orientacao):
                    marcar_navio(tabuleiro, linha, coluna, tamanho, orientacao)
                    # Salva cada célula do navio no banco
                    for i in range(tamanho):
                        l = linha + i if orientacao == 'V' else linha
                        c = coluna + i if orientacao == 'H' else coluna
                        cur.execute(
                            "INSERT INTO navios (partida_id, jogador_id, linha, coluna, tamanho, orientacao, atingido) VALUES (?, ?, ?, ?, ?, ?, 0)",
                            (partida_id, jogador_id, l, c, tamanho, orientacao)
                        )
                    colocado = True
                tentativas += 1
            if not colocado:
                raise Exception("Não foi possível posicionar todos os navios!")
    conn.commit()
    conn.close()
          