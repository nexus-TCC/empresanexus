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

async function entrar() {
        var email = document.getElementById("email").value.trim();
        var senha = document.getElementById("senha").value.trim();

        // Verifica se campos estão vazios
        if (email === "" || senha === "") {
                Swal.fire({
                        icon: 'error',
                        title: 'Opa...',
                        text: 'Você precisa preencher todos os campos!',
                        confirmButtonColor: '#0B6265'
                });
                return false;
        }

        // Verifica se email/senha estão corretos
        if (email === "" || senha === "") {
                Swal.fire({
                        icon: 'error',
                        title: 'Opa...',
                        text: 'E-mail ou senha incorretos!',
                        confirmButtonColor: '#0B6265'
                })
                return false;
        }
        const response = await fetch("/api/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, senha })
        });

        const data = await response.json();

        if (response.ok) {
                Swal.fire({ icon: 'success', title: 'Sucesso!', text: data.message, confirmButtonColor: '#0B6265' })
                        .then(() => window.location.href = "/index");
        } else {
                Swal.fire({ icon: 'error', title: 'Erro', text: data.error, confirmButtonColor: '#0B6265' });
        }
}



async function criarConta() {
        var email = document.getElementById("email").value.trim();
        var senha = document.getElementById("senha").value.trim();

        // Verifica se campos estão vazios
        if (email === "" || senha === "") {
                Swal.fire({
                        icon: 'error',
                        title: 'Opa...',
                        text: 'Você precisa preencher todos os campos!',
                        confirmButtonColor: '#0B6265'
                });
                return false;
        }
        const response = await fetch("/api/cadastro", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ nome, email, senha })
        });

        const data = await response.json();

        if (response.ok) {
                Swal.fire({ icon: 'success', title: 'Sucesso!', text: data.message, confirmButtonColor: '#0B6265' })
                        .then(() => window.location.href = "/entrar");
        } else {
                Swal.fire({ icon: 'error', title: 'Erro', text: data.error, confirmButtonColor: '#0B6265' });
        }

        // Verifica se email é válido
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
                Swal.fire({
                        icon: 'error',
                        title: 'Opa...',
                        text: 'Por favor, insira um e-mail válido!',
                        confirmButtonColor: '#0B6265'
                });
                return false;
        }

        // Verifica se senha tem pelo menos 8 caracteres
        if (senha.length < 8) {
                Swal.fire({
                        icon: 'error',
                        title: 'Opa...',
                        text: 'A senha deve ter pelo menos 8 caracteres!',
                        confirmButtonColor: '#0B6265'
                });
                return false;
        }

        //Verifica se senha tem pelo menos um número
        var numberPattern = /\d/;
        if (!numberPattern.test(senha)) {
                Swal.fire({
                        icon: 'error',
                        title: 'Opa...',
                        text: 'A senha deve conter pelo menos um número!',
                        confirmButtonColor: '#0B6265'
                });
                return false;
        }

        //Verifica se senha tem pelo menos uma letra maiúscula
        var uppercasePattern = /[A-Z]/;
        if (!uppercasePattern.test(senha)) {
                Swal.fire({
                        icon: 'error',
                        title: 'Opa...',
                        text: 'A senha deve conter pelo menos uma letra maiúscula!',
                        confirmButtonColor: '#0B6265'
                });
                return false;
        }

        //Verifica se senha tem pelo menos uma letra minúscula
        var lowercasePattern = /[a-z]/;
        if (!lowercasePattern.test(senha)) {
                Swal.fire({
                        icon: 'error',
                        title: 'Opa...',
                        text: 'A senha deve conter pelo menos uma letra minúscula!',
                        confirmButtonColor: '#0B6265'
                });
                return false;
        }

        //Verifica se email já está cadastrado 

        // Se passou nas validações, redireciona
        window.location.href = "/index";
        return true;
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
}


const searchInput = document.getElementById('search');
searchInput.addEventListener('input', (event) => {
        const value = formatString(event.target.value);
        const noResults = document.getElementById('no_results');
        const items = document.querySelectorAll('') //Colocar o nome da lista de empregos que vamos criar

        let hasResults = false;

        items.forEach(item => {
                //Aqui podemos manipular o item que quisermos da lista
                if (formatString(item.textContent).indexOf(value) !== -1) {
                        item.style.display = 'flex'

                        let hasResults = true;
                } else {
                        item.style.display = 'none'
                }
        })

        if (hasResults) {
                noResults.style.display = 'none';
        } else {
                noResults.style.display = 'block';
        }
});

const localizationInput = document.getElementById('localizat');
searchInput.addEventListener('input', (event) => {
        const value = formatString(event.target.value);
        const noResults = document.getElementById('no_results');
        const items = document.querySelectorAll('') //Colocar o nome da lista de empregos que vamos criar

        let hasResults = false;

        items.forEach(item => {
                //Aqui podemos manipular o item que quisermos da lista
                if (formatString(item.textContent).indexOf(value) !== -1) {
                        item.style.display = 'flex'

                        let hasResults = true;
                } else {
                        item.style.display = 'none'
                }
        })

        if (hasResults) {
                noResults.style.display = 'none';
        } else {
                noResults.style.display = 'block';
        }
});

function formatString(value) {
        return value.toLowerCase().trim().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
}


const euLink = document.getElementById("euLink");
const submenu = document.getElementById("submenuEu");

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

// Para mostrar <p><span> no html 
document.querySelector('#container2 p').style.display = 'block';

// Para esconder novamente
document.querySelector('#container2 p').style.display = 'none';