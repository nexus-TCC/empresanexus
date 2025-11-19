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

// LOGIN
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
                        // Tenta ler o JSON. Se o Flask retornar HTML (por erro 500), isso falha
                        dados = await resposta.json();
                } catch (e) {
                        console.error('Erro ao processar JSON da resposta:', e);
                        Swal.fire({
                                icon: 'error',
                                title: 'Erro de Comunicação',
                                text: 'O servidor retornou uma resposta inesperada. Verifique os logs do Flask.',
                                confirmButtonColor: '#0B6265'
                        });
                        return;
                }

                if (resposta.ok) {
                        // Sucesso (Status 200) - Redireciona
                        // Não precisa de sessionStorage.setItem('logado', 'true') se o Flask gerencia a sessão
                        window.location.href = '/index';
                } else {
                        // Falha (Status 400 ou 401) - Exibe o erro do JSON
                        Swal.fire({
                                icon: 'error',
                                title: 'Erro',
                                text: dados.error || 'Erro ao fazer login. Credenciais inválidas ou erro no servidor.',
                                confirmButtonColor: '#0B6265'
                        });
                }
        } catch (erro) {
                // Erro de rede (ex: servidor Flask fora do ar)
                console.error('Erro ao fazer login:', erro);
                Swal.fire({
                        icon: 'error',
                        title: 'Erro',
                        text: 'Ocorreu um erro de conexão. Verifique se o servidor está ativo.',
                        confirmButtonColor: '#0B6265'
                });
        }
}

// CADASTRO
async function criarConta() {
        const nome = document.getElementById("nome").value.trim();
        const email = document.getElementById("email").value.trim();
        const senha = document.getElementById("senha").value.trim();
        const tipo_conta = document.getElementById("tipo_conta").value.trim();
        const endereco = document.getElementById("endereço").value.trim();
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
                nome,
                email,
                senha,
                tipo_conta,
                endereco,
                cidade,
                estado,
                cep
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
                                icon: 'success', // Adicionado para sucesso, pois a lógica de redirecionamento está em um .then() que parece estar incompleto/incorreto.
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
        }
        catch (erro) {
                console.error('Erro ao cadastrar:', erro);
                Swal.fire({
                        icon: 'error',
                        title: 'Erro',
                        text: 'Ocorreu um erro de conexão. Tente novamente mais tarde.',
                        confirmButtonColor: '#0B6265'
                });
        }
}

// GOOGLE LOGIN
function decodeJWT(token) {
        let base64Url = token.split(".")[1];
        let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        let jsonPayload = decodeURIComponent(
                atob(base64)
                        .split("")
                        .map(function (c) {
                                return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
                        })
                        .join("")
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
                        Swal.fire({ // Adicionado para sucesso, pois a lógica de redirecionamento está em um .then() que parece estar incompleto/incorreto.
                                icon: 'success',
                                title: 'Login com Google realizado!',
                                text: 'Você será redirecionado.',
                                showConfirmButton: false,
                                timer: 1500
                        }).then(() => {
                                window.location.href = '/index';
                        });
                } else {
                        Swal.fire('Erro', 'Não foi possível fazer o login com Google.', 'error');
                }
        } else {

                const tipoConta = document.getElementById('tipo_conta') ? document.getElementById('tipo_conta').value : null;

                if (tipoConta) {
                        cadastrarComGoogle(email, nome, tipoConta);
                } else {
                        Swal.fire('Ops!', 'Seu e-mail não está cadastrado. Prossiga para o cadastro.', 'warning').then(() => {
                                window.location.href = '/tipoConta?email=' + email + '&nome=' + nome;
                        });
                }
        }
}

// FILTRAGEM
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

// Eventos de busca
const searchInput = document.getElementById('search');
if (searchInput) {
        searchInput.addEventListener('input', () => filtrarLista('search'));
}

const localizationInput = document.getElementById('localiza');
if (localizationInput) {
        localizationInput.addEventListener('input', () => filtrarLista('localiza'));
}
// Submenu "Eu" (Mantido)
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
function executarPesquisa() {
        const searchInput = document.getElementById('search');
        const termo = searchInput.value.trim();

        if (termo) {
                window.location.href = `/resultado_pesquisa?search=${encodeURIComponent(termo)}`;
        } else {
                window.location.href = `/index`;
        }
}

document.addEventListener('DOMContentLoaded', function () {
        const searchInput = document.getElementById('search');
        const searchIcon = document.querySelector('#allcontainer .fa-magnifying-glass');

        if (searchInput) {
                searchInput.addEventListener('keypress', function (e) {
                        if (e.key === 'Enter') {
                                executarPesquisa();
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
                searchIcon.addEventListener('click', executarPesquisa);
        }

        function logout() {
                // Função para tratar o logout com confirmação
                // (Requer a biblioteca SweetAlert2 - <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>)
                Swal.fire({
                        title: 'Tem certeza?',
                        text: "Você será desconectado da sua conta.",
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonColor: '#3085d6',
                        cancelButtonColor: '#d33',
                        confirmButtonText: 'Sim, sair!',
                        cancelButtonText: 'Cancelar'
                }).then((result) => {
                        if (result.isConfirmed) {
                                window.location.href = '/logout';
                        }
                });
        }
});