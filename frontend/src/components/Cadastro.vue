<template>
  <v-container class="d-flex align-center justify-center" style="height: 100vh; background-color: white;">
    <v-card class="pa-8" color="white" elevation="3" width="400">
      <v-img class="mb-5" contain height="60" src="/images/navio.png" />
      <v-card-title class="text-h5 text-center font-weight-bold" style="color: #1976D2;">
        Crie sua conta
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
          type="email"
        />

        <!-- Campo de Nickname -->
        <v-text-field
          v-model="nickname"
          :error-messages="nicknameErro"
          flat
          label="Nickname"
          required
          solo
        />

        <!-- Campo de Senha -->
        <v-text-field
          v-model="senha"
          :error-messages="senhaErro"
          flat
          label="Senha"
          required
          solo
          type="password"
        />

        <!-- Botão de Cadastro -->
        <v-btn block class="mt-4" style="background-color: #1976D2; color: white;" @click="validarCadastro">
          Cadastrar
        </v-btn>
      </v-form>

      <!-- Link para login -->
      <div class="text-center mt-3">
        <router-link class="text-decoration-none" style="color: #1976D2; font-weight: bold;" to="/login">
          Já tem uma conta? Faça login
        </router-link>
      </div>
    </v-card>
  </v-container>
</template>


<script>
  import { cadastrarJogador } from '../api.js'; // Caminho correto

  export default {
    data () {
      return {
        email: '',
        nickname: '',
        senha: '',
        emailErro: '',
        nicknameErro: '',
        senhaErro: '',
      };
    },
    methods: {
      validarCadastro () {
        this.emailErro = '';
        this.nicknameErro = '';
        this.senhaErro = '';

        if (!this.email) {
          this.emailErro = 'O campo e-mail é obrigatório!';
        }
        if (!this.nickname) {
          this.nicknameErro = 'O campo nickname é obrigatório!';
        }
        if (!this.senha) {
          this.senhaErro = 'O campo senha é obrigatório!';
        }

        if (!this.emailErro && !this.nicknameErro && !this.senhaErro) {
          cadastrarJogador(this.nickname, this.email, this.senha)
            .then(() => {
              alert('Cadastro realizado com sucesso!');
              this.$router.push('/login');
            })
            .catch(err => {
              alert(err.response?.data?.mensagem || 'Erro ao cadastrar!');
            });
        }
      },
    },
  };
</script>
