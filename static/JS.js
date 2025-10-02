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

//LOGIN

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
                const resposta = await fetch('http://localhost:5000/api/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email, senha }),
                });

                const dados = await resposta.json();

                if (resposta.ok) {
                        sessionStorage.setItem('logado', 'true');
                        Swal.fire({
                                icon: 'success',
                                title: 'Login realizado!',
                                text: dados.message,
                                timer: 1500,
                                showConfirmButton: false,
                        }).then(() => {
                                window.location.href = '/index';
                        });
                } else {
                        Swal.fire({
                                icon: 'error',
                                title: 'Erro',
                                text: dados.error || 'Erro ao fazer login.',
                        });
                }

        } catch (erro) {
                Swal.fire({
                        icon: 'error',
                        title: 'Erro inesperado',
                        text: erro.message,
                });
        }
}



async function criarConta() {
        const nome = document.getElementById("nome").value.trim();
        const email = document.getElementById("email").value.trim();
        const senha = document.getElementById("senha").value.trim();

        if (!nome || !email || !senha) {
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
                const resposta = await fetch('http://localhost:5000/api/cadastro', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ nome, email, senha }),
                });

                const dados = await resposta.json();

                if (resposta.ok) {
                        Swal.fire({
                                icon: 'success',
                                title: 'Cadastro realizado!',
                                text: dados.message,
                                confirmButtonText: 'Fazer login',
                        }).then(() => {
                                window.location.href = '/entrar';
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
                Swal.fire({
                        icon: 'error',
                        title: 'Erro inesperado',
                        text: erro.message,
                });
        }
}



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

function handleCredentialResponse(response) {

        console.log("Encoded JWT ID token: " + response.credential);

        const responsePayload = decodeJWT(response.credential);

        console.log("Campos do token de ID JWT decodificados:");
        console.log("  Nome completo: " + responsePayload.name);
        console.log("  Nome: " + responsePayload.given_name);
        console.log("  Sobrenome: " + responsePayload.family_name);
        console.log("  ID exclusivo: " + responsePayload.sub);
        console.log("  URL da imagem do perfil: " + responsePayload.picture);
        console.log("  E-mail: " + responsePayload.email);
        console.log("  E-mail verificado: " + responsePayload.email_verified);

        // Redireciona para a página seguinte do seu SPA/site
        window.location.href = '/index';
}


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

        noResults.style.display = hasResults ? 'none' : 'block';
}

// Eventos de busca
const searchInput = document.getElementById('search');
if (searchInput) {
        searchInput.addEventListener('input', () => filtrarLista('search'));
}

const localizationInput = document.getElementById('localizat');
if (localizationInput) {
        localizationInput.addEventListener('input', () => filtrarLista('localizat'));
}

// ------------------------------
// Submenu "Eu"
// ------------------------------
const euLink = document.getElementById("euLink");
const submenu = document.getElementById("submenuEu");

if (euLink && submenu) {
        euLink.addEventListener("click", function (e) {
                e.preventDefault();
                submenu.style.display = submenu.style.display === "block" ? "none" : "block";
        });

        // fecha se clicar fora
        document.addEventListener("click", function (e) {
                if (!euLink.contains(e.target) && !submenu.contains(e.target)) {
                        submenu.style.display = "none";
                }
        });

        submenu.style.display = "none";
}