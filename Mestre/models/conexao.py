import sqlite3

DB_PATH = 'database.db'

def conectar():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = conectar()
    cur = conn.cursor()
    # Tabela de jogadores
    cur.execute('''
        CREATE TABLE IF NOT EXISTS jogadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    # Tabela de partidas
    cur.execute('''
        CREATE TABLE IF NOT EXISTS partidas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            jogador1_id INTEGER NOT NULL,
            jogador2_id INTEGER NOT NULL,
            status TEXT DEFAULT 'em_andamento',
            vez_atual INTEGER DEFAULT 1,
            vencedor_id INTEGER,
            data_inicio TEXT DEFAULT CURRENT_TIMESTAMP,
            data_fim TEXT,
            FOREIGN KEY (jogador1_id) REFERENCES jogadores(id),
            FOREIGN KEY (jogador2_id) REFERENCES jogadores(id),
            FOREIGN KEY (vencedor_id) REFERENCES jogadores(id)
        )
    ''')
    # Tabela de jogadas
    cur.execute('''
        CREATE TABLE IF NOT EXISTS jogadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER NOT NULL,
            jogador_id INTEGER NOT NULL,
            linha INTEGER NOT NULL,
            coluna INTEGER NOT NULL,
            resultado TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (partida_id) REFERENCES partidas(id),
            FOREIGN KEY (jogador_id) REFERENCES jogadores(id)
        )
    ''')
    # Tabela de navios
    cur.execute('''
        CREATE TABLE IF NOT EXISTS navios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partida_id INTEGER NOT NULL,
            jogador_id INTEGER NOT NULL,
            linha INTEGER NOT NULL,
            coluna INTEGER NOT NULL,
            tamanho INTEGER NOT NULL,
            orientacao TEXT NOT NULL,
            atingido INTEGER DEFAULT 0,
            FOREIGN KEY (partida_id) REFERENCES partidas(id),
            FOREIGN KEY (jogador_id) REFERENCES jogadores(id)
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso.")


