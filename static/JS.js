
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
            window.location.href = "Index.html";
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
            });
            window.location.href = "Index.html";
        }
    });
    return false;
    }


    window.location.href = "../templates/Index.html";
    return true;
}



    document.getElementById("entrarBotao").addEventListener("click", function () {
        window.location.href = "ContinuarGoogle.html";
    });

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


    if (email !== "dsmbispo@gmail.com" || senha !== "123456789") {
        Swal.fire({
            icon: 'error',
            title: 'Opa...',
            text: 'E-mail ou senha incorretos!',
            confirmButtonColor: '#0B6265'
        })
        return false;
    }


    window.location.href = "../templates/Index.html";
    return true;
}

 // Função callback do login com Google
        function handleCredentialResponse(response) {
            // Aqui você recebe o JWT do Google
            console.log("JWT ID Token: ", response.credential);


            // Exemplo: exibir alerta
            Swal.fire({
                title: 'Login com Google feito!',
                text: 'Token recebido no console.',
                icon: 'success',
                confirmButtonText: 'OK'
            });


            // Aqui você pode enviar esse token para o backend validar
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

        console.log("Decoded JWT ID token fields:");
        console.log("  Full Name: " + responsePayload.name);
        console.log("  Given Name: " + responsePayload.given_name);
        console.log("  Family Name: " + responsePayload.family_name);
        console.log("  Unique ID: " + responsePayload.sub);
        console.log("  Profile image URL: " + responsePayload.picture);
        console.log("  Email: " + responsePayload.email);
        console.log("  VerifiedEmail: " + responsePayload.email_verified);
      }
