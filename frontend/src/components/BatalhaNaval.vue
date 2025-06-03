<template>
  <v-container class="d-flex flex-column align-center justify-center" style="height: 100vh; background-color: white;">
    <v-card class="pa-5" color="white" elevation="3" width="600">
      <v-card-title class="text-h5 text-center font-weight-bold" style="color: #1976D2;">
        Batalha Naval
      </v-card-title>
      <p class="text-center font-weight-bold" style="color: #1976D2;">
        Modo de Batalha
      </p>
      <v-container>
        <v-row v-for="linha in 10" :key="linha" justify="center">
          <v-col v-for="coluna in 10" :key="coluna" cols="1">
            <v-btn
              class="game-cell"
              :color="grid[linha - 1][coluna - 1] === 'H' ? 'green' : (grid[linha - 1][coluna - 1] === 'X' ? 'red' : (grid[linha - 1][coluna - 1] === 'N' ? 'grey' : 'blue'))"
              @click="interagirCelula(linha, coluna)"
            >
              {{ grid[linha - 1][coluna - 1] }}
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
      <div v-if="partidaStatus === 'finalizada'" class="text-h5 mt-4" style="color: green;">
        Fim de jogo!<br>
        <span v-if="String(vencedorId) === String(jogadorId)">
          Você venceu! 🏆
        </span>
        <span v-else>
          O campeão foi {{ vencedorNome ? vencedorNome : 'o jogador ' + vencedorId }}!
        </span>
      </div>
      <v-btn block class="mt-4" style="background-color: #D32F2F; color: white;" @click="sairJogo">
        Sair do Jogo
      </v-btn>
    </v-card>
  </v-container>
</template>

<script>
  import { consultarPartida, enviarJogada } from '../api.js';
  export default {
    data () {
      return {
        grid: Array(10).fill().map(() => Array(10).fill('~')),
        partidaStatus: '',
        vencedorId: null,
        jogadorId: localStorage.getItem('jogador_id'),
        vencedorNome: null,
      };
    },

    mounted () {
      this.carregarEstadoPartida();
    },
    methods: {
      /**
       * Função chamada ao clicar em uma célula do tabuleiro
       * Se estiver no modo de posicionamento, adiciona um navio (até o limite de 20)
       * No modo de batalha, permite ataques
       */
      async carregarEstadoPartida () {
        const partida_id = localStorage.getItem('partida_id');
        const jogador_id = localStorage.getItem('jogador_id');
        try {
          const resp = await consultarPartida(partida_id, jogador_id);
          // Inicializa o grid vazio
          this.grid = Array(10).fill().map(() => Array(10).fill('~'));
          this.partidaStatus = resp.data.partida_status || '';
          this.vencedorId = resp.data.vencedor_id || null;
          this.vencedorNome = resp.data.vencedor_nome || null;
          // Mostra seus navios
          for (const navio of resp.data.navios || []) {
            this.grid[navio.linha][navio.coluna] = 'N';
          }
          // Mostra acertos/erros das jogadas
          for (const jogada of resp.data.jogadas || []) {
            if (String(jogada.jogador_id) === String(jogador_id)) {
              if (jogada.resultado === true || jogada.resultado === 1 || jogada.resultado === 'True' || jogada.resultado === 'true' || jogada.resultado === '1') {
                this.grid[jogada.linha][jogada.coluna] = 'H'; // Acerto (verde)
              } else {
                this.grid[jogada.linha][jogada.coluna] = 'X'; // Erro (vermelho)
              }
            }
          }
        } catch (err) {
          alert('Erro ao carregar o estado da partida!');
        }
      },

      async interagirCelula (linha, coluna) {
        if (this.partidaStatus === 'finalizada') {
          alert('A partida já foi finalizada!');
          return;
        }
        const partida_id = localStorage.getItem('partida_id');
        const jogador_id = localStorage.getItem('jogador_id');
        try {
          const resp = await enviarJogada(partida_id, jogador_id, linha - 1, coluna - 1);
          await this.carregarEstadoPartida(); // Atualiza o grid após atacar
        } catch (err) {
          alert(err.response?.data?.mensagem || 'Erro ao enviar jogada!');
        }
      },

      /**
       * Quando o jogador terminar de posicionar os navios e clicar em "Iniciar Batalha"
       * Transforma o jogo no modo de batalha, impedindo novas alterações nos navios
       */
      /**
       * Função para sair do jogo e redirecionar para a tela de login
       */
      sairJogo () {
        alert('Você saiu do jogo!');
        this.$router.push('/'); // Redireciona para a tela de login
      },
    },
  };
</script>

<style>
/* Define o tamanho de cada célula do tabuleiro */
.game-cell {
  width: 40px;
  height: 40px;
  font-size: 18px;
}
</style>
