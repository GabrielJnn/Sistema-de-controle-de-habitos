const API_URL = 'http://localhost:8000';

const iniciarSistema = document.getElementById('iniciarSistema');
const textoDaTela = document.getElementById('mensagem');
const criarHabito = document.getElementById('criarHabito');
const informacoesHabitos = document.getElementById('informaçõesHabitos');
const apagarDados = document.getElementById('apagarDados');
const inputHabito = document.getElementById('habito');
const listaHabitos = document.getElementById('listaHabitos');

function mostrarMensagem(msg, isError = false) {
    textoDaTela.style.display = 'block';
    textoDaTela.innerText = msg;
    if (isError) {
        textoDaTela.classList.add('error');
    } else {
        textoDaTela.classList.remove('error');
    }
    setTimeout(() => { textoDaTela.style.display = 'none'; }, 3000);
}

iniciarSistema.addEventListener('click', async () => {
    try {
        const res = await fetch(`${API_URL}/criar_tabelas`, { method: 'POST' });
        const data = await res.json();
        mostrarMensagem(data.message, data.status === 'error');
    } catch (e) {
        mostrarMensagem("Erro ao conectar com API", true);
    }
});

criarHabito.addEventListener('click', async () => {
    const nome = inputHabito.value.trim();
    if (!nome) return mostrarMensagem("Digite um nome para o hábito", true);

    try {
        const res = await fetch(`${API_URL}/criar_habito`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: nome })
        });
        const data = await res.json();
        mostrarMensagem(data.message, data.status === 'error');
        if (data.status === 'success') {
            inputHabito.value = '';
            informacoesHabitos.click();
        }
    } catch (e) {
        mostrarMensagem("Erro ao conectar com API", true);
    }
});

informacoesHabitos.addEventListener('click', async () => {
    try {
        const res = await fetch(`${API_URL}/informacoes_habitos`);
        const data = await res.json();
        if (data.status === 'success') {
            listaHabitos.innerHTML = '';
            data.data.forEach(habito => {
                const div = document.createElement('div');
                div.className = 'habito-card';
                div.innerHTML = `
                    <span>${habito.name}</span>
                    <div class="habito-actions">
                        <button onclick="marcarFrequencia(${habito.id})">+1 Frequência</button>
                        <button class="danger" onclick="deletarHabito(${habito.id})">Deletar</button>
                    </div>
                `;
                listaHabitos.appendChild(div);
            });
        }
    } catch (e) {
        mostrarMensagem("Erro ao buscar hábitos", true);
    }
});

apagarDados.addEventListener('click', async () => {
    if(!confirm("Tem certeza? Isso apagará tudo e não pode ser desfeito!")) return;
    try {
        const res = await fetch(`${API_URL}/apagar_dados`, { method: 'DELETE' });
        const data = await res.json();
        mostrarMensagem(data.message, data.status === 'error');
        listaHabitos.innerHTML = '';
    } catch (e) {
        mostrarMensagem("Erro ao apagar dados", true);
    }
});

window.marcarFrequencia = async (id) => {
    try {
        const res = await fetch(`${API_URL}/marcar_frequencia/${id}`, { method: 'POST' });
        const data = await res.json();
        mostrarMensagem(data.message, data.status === 'error');
    } catch (e) {
        mostrarMensagem("Erro ao marcar frequência", true);
    }
};

window.deletarHabito = async (id) => {
    if(!confirm("Tem certeza que deseja deletar este hábito?")) return;
    try {
        const res = await fetch(`${API_URL}/deletar_habito/${id}`, { method: 'DELETE' });
        const data = await res.json();
        mostrarMensagem(data.message, data.status === 'error');
        informacoesHabitos.click();
    } catch (e) {
        mostrarMensagem("Erro ao deletar", true);
    }
};