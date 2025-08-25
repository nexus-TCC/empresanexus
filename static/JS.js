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



    document.getElementById("entrarBotao").addEventListener("click", function () {
        window.location.href = "ContinuarGoogle.html";
    });

function continuarGoogle() {
    var senha = document.getElementById("senha").value.trim();


    if (senha === "") {
        Swal.fire({
            icon: 'error',
            title: 'Opa...',
            text: 'Você precisa preencher todos os campos!',
            confirmButtonColor: '#0B6265'
        });
        return false;
    }

    if (senha !== "123456789") {
        Swal.fire({
            icon: 'error',
            title: 'Opa...',
            text: 'Senha incorreta!',
            confirmButtonColor: '#0B6265'
        });
        return false;
    }



    window.location.href = "Index.html";
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


function handleCredentialResponse(response) {
    console.log("JWT ID Token: ", response.credential);

    // Enviar token para o backend
    fetch("http://localhost:3000/auth/google", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ token: response.credential })
    })
    .then(res => res.json())
    .then(data => {
        console.log("Resposta do backend:", data);
        alert("Logado como " + data.user.name);
    })
    .catch(err => console.error("Erro:", err));
}

