<template>
  <v-container class="d-flex flex-column align-center justify-center" style="height: 100vh;">
    <v-card class="pa-5" width="400">
      <v-card-title class="text-h5 text-center">Nova Partida</v-card-title>
      <v-text-field v-model="jogador2_id" label="ID do segundo jogador" />
      <v-btn color="primary" @click="iniciarPartida">Criar Partida</v-btn>
      <v-divider class="my-4" />
      <v-card-title class="text-h6 text-center">Entrar em Partida</v-card-title>
      <v-text-field v-model="partidaExistente" label="ID da Partida" />
      <v-btn color="secondary" @click="entrarPartida">Entrar</v-btn>
    </v-card>
  </v-container>
</template>

<script>
  import { criarPartida } from '../api.js';

  export default {
    data () {
      return {
        jogador2_id: '',
        partidaExistente: '',
      };
    },
    methods: {
      async iniciarPartida () {
        const jogador1_id = localStorage.getItem('jogador_id');
        if (!jogador1_id || !this.jogador2_id) {
          alert('Preencha ambos os IDs!');
          return;
        }
        try {
          const resp = await criarPartida(jogador1_id, this.jogador2_id);
          localStorage.setItem('partida_id', resp.data.partida_id);
          this.$router.push('/batalhanaval');
        } catch (err) {
          alert(err.response?.data?.mensagem || 'Erro ao criar partida!');
        }
      },
      entrarPartida () {
        if (!this.partidaExistente) {
          alert('Digite o ID da partida!');
          return;
        }
        localStorage.setItem('partida_id', this.partidaExistente);
        this.$router.push('/batalhanaval');
      },
    },
  };
</script>
