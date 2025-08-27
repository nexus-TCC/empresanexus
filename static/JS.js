
// Envia dados para o Python usando fetch
fetch('/minha-rota', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ chave: 'valor' })
})
.then(response => response.json())
.then(data => {
    console.log(data); // resposta do Python
});

function mostrarSenha() {
    const input = document.getElementById("senha");
    const icone = document.getElementById("iconeOlho");
  
    if (input.type === "password") {
      input.type = "text";
      icone.src = "../static/images/olho fechado senha.png";
      icone.alt = "Ocultar senha";
    } else {
      input.type = "password";
      icone.src = "../static/images/olho Aberto Senha.png"; 
      icone.alt = "Mostrar senha";
    }
}

function entrar() {
    var email = document.getElementById("email").value.trim();
    var senha = document.getElementById("senha").value.trim();

    if (email === "" || senha === "") {
        Swal.fire({
            icon: 'error',
            title: 'Opa...',
            text: 'Você precisa preencher todos os campos!',
            confirmButtonColor: '#0B6265'
        });
        return false;
    }

    fetch('http://localhost:5001/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, senha: senha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            Swal.fire({
                icon: 'error',
                title: 'Erro',
                text: data.error,
                confirmButtonColor: '#0B6265'
            });
        } else {
            window.location.href = "/index"; // rota do Flask
        }
    });
    return false;
}
function criarConta() {
    var email = document.getElementById("email").value.trim();
    var senha = document.getElementById("senha").value.trim();

    if (email === "" || senha === "") {
        Swal.fire({
            icon: 'error',
            title: 'Opa...',
            text: 'Você precisa preencher todos os campos!',
            confirmButtonColor: '#0B6265'
        });
        return false;
    }

    fetch('http://localhost:5001/cadastro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, senha: senha })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            Swal.fire({
                icon: 'error',
                title: 'Erro',
                text: data.error,
                confirmButtonColor: '#0B6265'
            });
        } else {
            Swal.fire({
                icon: 'success',
                title: 'Conta criada!',
                text: data.message,
                confirmButtonColor: '#0B6265'
            }).then(() => {
                window.location.href = "/index"; // rota do Flask
            });
        }
    });
    return false;
}

    document.getElementById("botaoEntrar").addEventListener("click", function () {
        window.location.href = "/continuarGoogle"; // Redireciona para a rota do Flask
    });



 // Função callback do login com Google
        function handleCredentialResponse(response) {
    console.log("JWT ID Token: ", response.credential);
    const responsePayload = decodeJWT(response.credential);

    Swal.fire({
        title: 'Login com Google feito!',
        text: 'Bem-vindo, ' + responsePayload.name,
        icon: 'success',
        confirmButtonText: 'OK'
    });
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

      

      function validarFormularioCurriculo() {
    let nome = document.querySelector("input[name='nome']").value;
    let telefone = document.querySelector("input[name='telefone']").value;
    if (nome === "" || telefone === "") {
        Swal.fire({
            icon: 'error',
            title: 'Campos obrigatórios!',
            text: 'Preencha Nome e Telefone.',
        });
        return false;
    }
    return true;
}