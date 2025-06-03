import axios from 'axios';

const API_URL = 'http://localhost:5000';


// Cadastro do Jogador
export function cadastrarJogador (nickname, email, senha) {
  return axios.post(`${API_URL}/cadastrar_jogador`, { nome: nickname, usuario: email, senha });
}


//Login do Jogador
export function loginJogador (email, senha) {
  return axios.post(`${API_URL}/login_jogador`, {
    usuario: email,
    senha,
  });
}


//Criar a partida
export function criarPartida (jogador1_id, jogador2_id){
  return axios.post(`${API_URL}/criar_partida`, { jogador1_id, jogador2_id });
}

//Enviar a jogada
export function enviarJogada (partida_id, jogador_id, linha, coluna) {
  return axios.post(`${API_URL}/jogada`, {
    partida_id,
    jogador_id,
    linha,
    coluna,
  });
}

//Consultar o status da partida
export function consultarPartida (partida_id, jogador_id) {
  return axios.get(`http://localhost:5000/estado_partida/${partida_id}/${jogador_id}`);
}
