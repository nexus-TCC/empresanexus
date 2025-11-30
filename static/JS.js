function mostrarSenha() {
    const input = document.getElementById("senha");
    const icone = document.getElementById("iconeOlho");

    if (input.type === "password") {
        input.type = "text";
        icone.src = "../static/images/olho-fechado-senha.png";
        icone.alt = "Ocultar senha";
    } else {
        input.type = "password";
        icone.src = "../static/images/olho-Aberto-Senha.png";
        icone.alt = "Mostrar senha";
    }
}

function Email_Eh_Valido(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

async function verificarEmailNoBanco(email) {
    try {
        const resposta = await fetch('/api/verificar_email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email }),
        });
        const dados = await resposta.json();

        return dados;
    } catch (erro) {
        console.error('Erro ao verificar email:', erro);
        return { exists: false, error: 'Erro de conexão com o servidor.' };
    }
}

// --- LOGIN ---
async function loginUsuario() {
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();

    if (!email || !senha) {
        Swal.fire({
            icon: 'error',
            title: 'Campos obrigatórios',
            text: 'Preencha todos os campos.',
            confirmButtonColor: '#0B6265'
        });
        return;
    }

    if (!Email_Eh_Valido(email)) {
        Swal.fire({
            icon: 'error',
            title: 'Email inválido',
            text: 'Digite um email válido.',
            confirmButtonColor: '#0B6265'
        });
        return;
    }

    try {
        const resposta = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha }),
        });

        let dados;
        try {
            dados = await resposta.json();
        } catch (e) {
            console.error('Erro ao processar JSON da resposta:', e);
            Swal.fire({
                icon: 'error',
                title: 'Erro de Comunicação',
                text: 'O servidor retornou uma resposta inesperada.',
                confirmButtonColor: '#0B6265'
            });
            return;
        }

        if (resposta.ok) {
            window.location.href = '/index';
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Erro',
                text: dados.error || 'Erro ao fazer login.',
                confirmButtonColor: '#0B6265'
            });
        }
    } catch (erro) {
        console.error('Erro ao fazer login:', erro);
        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Ocorreu um erro de conexão.',
            confirmButtonColor: '#0B6265'
        });
    }
}

// --- CADASTRO ---
async function criarConta() {
    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const senha = document.getElementById("senha").value.trim();
    const tipo_conta = document.getElementById("tipo_conta").value.trim();
    const endereco = document.getElementById("endereco").value.trim();
    const cidade = document.getElementById("cidade").value.trim();
    const estado = document.getElementById("estado").value.trim();
    const cep = document.getElementById("cep").value.trim();

    if (!nome || !email || !senha || !tipo_conta || !endereco || !cidade || !estado || !cep) {
        Swal.fire({
            icon: 'error',
            title: 'Campos obrigatórios',
            text: 'Preencha todos os campos do formulário.',
            confirmButtonColor: '#0B6265'
        });
        return;
    }

    if (!Email_Eh_Valido(email)) {
        Swal.fire({
            icon: 'error',
            title: 'Email inválido',
            text: 'Digite um email válido.',
            confirmButtonColor: '#0B6265'
        });
        return;
    }

    if (senha.length < 6) {
        Swal.fire({
            icon: 'warning',
            title: 'Senha fraca',
            text: 'A senha deve ter pelo menos 6 caracteres.',
            confirmButtonColor: '#0B6265'
        });
        return;
    }

    const dadosCadastro = {
        nome, email, senha, tipo_conta, endereco, cidade, estado, cep
    };

    try {
        const resposta = await fetch('/api/cadastro', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dadosCadastro),
        });
        const dados = await resposta.json();

        if (resposta.ok) {
            Swal.fire({
                icon: 'success',
                title: 'Cadastro realizado!',
                text: 'Você será redirecionado.',
                showConfirmButton: false,
                timer: 1500
            }).then(() => {
                window.location.href = '/index';
            });
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Erro ao cadastrar',
                text: dados.error || 'Tente novamente.',
                confirmButtonColor: '#0B6265'
            });
        }
    } catch (erro) {
        console.error('Erro ao cadastrar:', erro);
        Swal.fire({
            icon: 'error',
            title: 'Erro',
            text: 'Ocorreu um erro de conexão.',
            confirmButtonColor: '#0B6265'
        });
    }
}

// --- GOOGLE LOGIN ---
function decodeJWT(token) {
    let base64Url = token.split(".")[1];
    let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    let jsonPayload = decodeURIComponent(
        atob(base64).split("").map(function (c) {
            return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        }).join("")
    );
    return JSON.parse(jsonPayload);
}

function parseJwt(token) {
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
};

async function handleCredentialResponse(response) {
    window.onload = function () {
        google.accounts.id.initialize({
            client_id: "767274472831-8fgrh0mguchu4sivg30b8hgkgkvt645v.apps.googleusercontent.com",
            callback: handleCredentialResponse
        });
    }
    const data = parseJwt(response.credential);
    const email = data.email;
    const nome = data.name;

    const checkResponse = await fetch('/api/verificar_email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email })
    });

    const checkData = await checkResponse.json();

    if (checkData.exists) {
        const loginResponse = await fetch('/api/login_google', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });

        const loginData = await loginResponse.json();
        if (loginData.success) {
            window.location.href = '/index';
        } else {
            Swal.fire('Erro', 'Não foi possível fazer o login com Google.', 'error');
        }
    } else {
        const tipoConta = document.getElementById('tipo_conta') ? document.getElementById('tipo_conta').value : null;
        if (tipoConta) {
            cadastrarComGoogle(email, nome, tipoConta);
        } else {
            Swal.fire({
                title: 'Ops!',
                text: 'Seu e-mail não está cadastrado. Prossiga para o cadastro.',
                icon: 'warning', // Ícone
                confirmButtonColor: '#0B6265',
                confirmButtonText: 'Ok'
            }).then(() => {
                window.location.href = '/tipoConta?email=' + email + '&nome=' + nome;
            });
        }
    }

    // --- UTILITÁRIOS ---
    function formatString(value) {
        return value.toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }

    function filtrarLista(inputId) {
        const value = formatString(document.getElementById(inputId).value);
        const noResults = document.getElementById('no_results');
        const items = document.querySelectorAll('.item-lista');
        let hasResults = false;

        items.forEach(item => {
            if (formatString(item.textContent).includes(value)) {
                item.style.display = 'flex';
                hasResults = true;
            } else {
                item.style.display = 'none';
            }
        });

        if (noResults) {
            noResults.style.display = hasResults ? 'none' : 'block';
        }
    }

    function executarPesquisa() {
        const searchInput = document.getElementById('search');
        const termo = searchInput.value.trim();

        if (termo) {
            window.location.href = `/resultado_pesquisa?search=${encodeURIComponent(termo)}`;
        } else {
            window.location.href = `/index`;
        }
    }

    window.logout = function () {
        if (typeof Swal === 'undefined') {
            window.location.href = '/logout';
            return false;
        }

        Swal.fire({
            title: 'Tem certeza?',
            text: "Você será desconectado da sua conta.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#0B6265',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sim, sair!',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                window.location.href = '/logout';
            }
        });
        return false;
    };

    // Função de Exclusão de Vaga (Mantida)
    window.excluirVagaComSwal = function (vagaId, vagaTitulo) {
        if (typeof Swal === 'undefined') {
            alert("Erro: SweetAlert2 não carregado. Ação cancelada.");
            return;
        }

        Swal.fire({
            title: 'ATENÇÃO!',
            text: `Tem certeza que deseja excluir a vaga "${vagaTitulo}"? Esta ação é irreversível e removerá todos os candidatos associados.`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#0B6265',
            confirmButtonText: 'Sim, EXCLUIR VAGA!',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                const form = document.getElementById(`form-excluir-vaga-${vagaId}`);
                if (form) {
                    form.submit();
                } else {
                    Swal.fire('Erro!', 'Formulário de exclusão não encontrado.', 'error');
                }
            }
        });
    };

    // Função de Exclusão de Currículo (Otimizada com Loading)
    window.confirmarExclusao = function (urlExclusao, urlRedirecionamento) {
        if (typeof Swal === 'undefined') {
            alert("Erro: SweetAlert2 não carregado. Ação cancelada.");
            return;
        }

        Swal.fire({
            title: 'Tem certeza?',
            text: "Ao confirmar, seus dados de experiência e habilidades serão permanentemente excluídos do seu currículo. Sua conta será mantida.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#d33',
            cancelButtonColor: '#0B6265',
            confirmButtonText: 'Sim, EXCLUIR!',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        }).then((result) => {
            if (result.isConfirmed) {

                Swal.fire({
                    title: 'Excluindo...',
                    text: 'Processando a exclusão do seu currículo. Aguarde.',
                    allowOutsideClick: false,
                    didOpen: () => {
                        Swal.showLoading();
                    }
                });

                // Requisição POST via Fetch API
                fetch(urlExclusao, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                    .then(response => response.json())
                    .then(data => {
                        Swal.close(); // Fecha o loading

                        if (data.success) {
                            Swal.fire({
                                title: 'Currículo Deletado!',
                                text: 'Os campos de experiência e habilidades foram limpos com sucesso.',
                                icon: 'success',
                                confirmButtonColor: '#0B6265',
                                confirmButtonText: 'Ok'
                            }).then(() => {
                                window.location.href = urlRedirecionamento;
                            });
                        } else {
                            Swal.fire('Erro!', 'Falha ao limpar o currículo: ' + (data.error || 'Erro desconhecido.'), 'error');
                        }
                    })
                    .catch(error => {
                        Swal.close();
                        console.error('Erro de rede:', error);
                        Swal.fire('Erro!', 'Erro de comunicação com o servidor ao deletar currículo.', 'error');
                    });
            }
        });
    };

    document.addEventListener('DOMContentLoaded', function () {

        // 1. Pesquisa e Offcanvas
        const searchInput = document.getElementById('search');
        const localizationInput = document.getElementById('localiza');
        const searchIcon = document.querySelector('.search-container .fa-magnifying-glass');

        if (searchInput) {
            searchInput.addEventListener('input', () => filtrarLista('search'));
            searchInput.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    // Certifique-se que 'executarPesquisa' existe em outro lugar ou aqui
                    // executarPesquisa(); 
                    e.preventDefault();
                }
            });
            const params = new URLSearchParams(window.location.search);
            const termoURL = params.get('search');
            if (termoURL) {
                searchInput.value = termoURL;
            }
        }
        if (searchIcon) {
            searchIcon.style.cursor = 'pointer';
            // searchIcon.addEventListener('click', executarPesquisa); 
        }
        if (localizationInput) {
            localizationInput.addEventListener('input', () => filtrarLista('localiza'));
        }

        var myOffcanvas = document.getElementById('offcanvasNavbar');
        var toggleBtn = document.getElementById('offcanvasToggleBtn');
        if (myOffcanvas && toggleBtn) {
            myOffcanvas.addEventListener('show.bs.offcanvas', function () {
                toggleBtn.style.visibility = 'hidden';
            });
            myOffcanvas.addEventListener('hide.bs.offcanvas', function () {
                toggleBtn.style.visibility = 'visible';
            });
        }

        const euLink = document.getElementById("euLink");
        const submenu = document.getElementById("submenuEu");
        if (euLink && submenu) {
            euLink.addEventListener("click", function (e) {
                e.preventDefault();
                submenu.style.display = submenu.style.display === "block" ? "none" : "block";
            });
            document.addEventListener("click", function (e) {
                if (!euLink.contains(e.target) && !submenu.contains(e.target)) {
                    submenu.style.display = "none";
                }
            });
            submenu.style.display = "none";
        }


        const btnEntrar = document.getElementById("botaoEntrar");
        const btnCriar = document.getElementById("botaoCriarConta");

        function acionarBotaoNoEnter(event, botao) {
            if (event.key === "Enter") {
                event.preventDefault();
                botao.click();
            }
        }

        if (btnEntrar) {
            const inputEmail = document.getElementById("email");
            const inputSenha = document.getElementById("senha");

            if (inputEmail) inputEmail.addEventListener("keypress", (e) => acionarBotaoNoEnter(e, btnEntrar));
            if (inputSenha) inputSenha.addEventListener("keypress", (e) => acionarBotaoNoEnter(e, btnEntrar));
        }

        if (btnCriar) {
            const camposCadastro = ["nome", "email", "senha", "endereco", "cidade", "estado", "cep"];

            camposCadastro.forEach(id => {
                const elemento = document.getElementById(id);
                if (elemento) {
                    elemento.addEventListener("keypress", (e) => acionarBotaoNoEnter(e, btnCriar));
                }
            });
        }

        // LISTENER PARA EXCLUSÃO DE VAGA (AGORA DENTRO DO BLOCO CORRETO)
        document.querySelectorAll('.btn-excluir-vaga').forEach(button => {
            button.addEventListener('click', function () {
                const vagaId = this.getAttribute('data-vaga-id');
                const vagaTitulo = this.getAttribute('data-vaga-titulo');

                excluirVagaComSwal(vagaId, vagaTitulo);
            });
        });
    });
}