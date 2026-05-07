// 1. Pegamos as referências do HTML pelo ID
const iniciarSistema = document.getElementById('iniciarSistema');
const textoDaTela = document.getElementById('mensagem');
const criarHabito = document.getElementById('criarHabito');
const informacoesHabitos = document.getElementById('informaçõesHabitos');
const apagarDados = document.getElementById('apagarDados');
// 2. Criamos o "ouvinte" de eventos
iniciarSistema.addEventListener('click', function() {
    // 3. O equivalente ao "print" na tela:
    if (iniciarSistema === true) {
        textoDaTela.innerText = "Sistema rodando";
    } 
    else {
        textoDaTela.innerText = "Erro ao iniciar o sistema";
    }
});