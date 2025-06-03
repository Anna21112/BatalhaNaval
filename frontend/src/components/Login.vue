<template>
  <v-container class="d-flex align-center justify-center" style="height: 100vh; background-color: white;">
    <v-card class="pa-8" color="white" elevation="3" width="400">
      <v-img class="mb-5" contain height="60" src="/images/navio.png" />
      <v-card-title class="text-h5 text-center font-weight-bold" style="color: #1976D2;">
        Acesse sua conta
      </v-card-title>

      <v-form ref="form">
        <!-- Campo de E-mail -->
        <v-text-field
          v-model="email"
          :error-messages="emailErro"
          flat
          label="E-mail"
          required
          solo
          style="color: black;"
          type="email"
        />

        <!-- Campo de Senha -->
        <v-text-field
          v-model="senha"
          :error-messages="senhaErro"
          flat
          label="Senha"
          required
          solo
          style="color: black;"
          type="password"
        />

        <div class="text-right mt-2" />

        <!-- Botão de Login -->
        <v-btn block class="mt-4" style="background-color: #1976D2; color: white;" @click="validarLogin">
          Entrar
        </v-btn>
      </v-form>

      <!-- Link para cadastro -->
      <div class="text-center mt-3">
        <router-link class="text-decoration-none" style="color: #1976D2; font-weight: bold;" to="/cadastro">
          Criar uma conta
        </router-link>
      </div>
    </v-card>
  </v-container>
</template>

<script>
  import { loginJogador } from '../api.js';

  export default {
    data () {
      return {
        email: '', // Armazena o e-mail digitado pelo usuário
        senha: '', // Armazena a senha digitada pelo usuário
        emailErro: '', // Mensagem de erro do e-mail
        senhaErro: '', // Mensagem de erro da senha
      };
    },
    methods: {
      validarLogin () {
        // Reseta mensagens de erro
        this.emailErro = '';
        this.senhaErro = '';

        // Verifica se o campo de e-mail está preenchido
        if (!this.email) {
          this.emailErro = 'O campo e-mail é obrigatório!';
        }

        // Verifica se o campo de senha está preenchido
        if (!this.senha) {
          this.senhaErro = 'O campo senha é obrigatório!';
        }

        // Se ambos os campos estiverem preenchidos, tenta autenticar na API
        if (!this.emailErro && !this.senhaErro) {
          loginJogador(this.email, this.senha)
            .then(resp => {
              // Salve o jogador_id se quiser usar depois
              localStorage.setItem('jogador_id', resp.data.jogador_id);
              this.$router.push('/novaPartida');
            })
            .catch(err => {
              alert(err.response?.data?.mensagem || 'Usuário ou senha inválidos!');
            });
        }
      },
    },
  };
</script>
