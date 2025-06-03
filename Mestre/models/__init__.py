from .conexao import conectar, init_db
from .jogadas import registrar_jogada
from .partidas import vez_atual, atualizar_vez, criar_partida, consultar_estado_partida, jogada_valida, obter_jogadores_partida
from .navios import verificar_acerto, verificar_fim_de_jogo
from .jogadores import criar_jogador, buscar_jogador_por_usuario, autenticar_jogador
from .gerarNavios import gerar_navios_automaticamente, posicao_valida