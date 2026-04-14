// 1. Pegamos as referências do HTML pelo ID
const botao = document.getElementById('iniciarSistema');
const textoDaTela = document.getElementById('mensagem');

// 2. Criamos o "ouvinte" de eventos
botao.addEventListener('click', function() {
    // 3. O equivalente ao "print" na tela:
    if (botao === true) {
        textoDaTela.innerText = "Sistema rodando";
    } 
    else {
        textoDaTela.innerText = "Erro ao iniciar o sistema";
    }
});