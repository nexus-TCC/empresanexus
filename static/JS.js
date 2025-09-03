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
    if (email !== "dsmbispo@gmail.com" || senha !== "123456789") {
        Swal.fire({
            icon: 'error',
            title: 'Opa...',
            text: 'E-mail ou senha incorretos!',
            confirmButtonColor: '#0B6265'
        })
        return false;
    }

    // Se passou nas validações, redireciona
    window.location.href = "../templates/Index.html";
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

        console.log("Decoded JWT ID token fields:");
        console.log("  Full Name: " + responsePayload.name);
        console.log("  Given Name: " + responsePayload.given_name);
        console.log("  Family Name: " + responsePayload.family_name);
        console.log("  Unique ID: " + responsePayload.sub);
        console.log("  Profile image URL: " + responsePayload.picture);
        console.log("  Email: " + responsePayload.email);
        console.log("  VerifiedEmail: " + responsePayload.email_verified);
      }


const searchInput = document.getElementById('search');
      searchInput.addEventListener('input', (event) => {
        const value = formatString(event.target.value);
        const noResults = document.getElementById('no_results');
        const items = document.querySelectorAll('') //Colocar o nome da lista de empregos que vamos criar

        let hasResults = false;

        items.forEach(item =>{
          //Aqui podemos manipular o item que quisermos da lista
          if(formatString(item.textContent).indexOf(value) !== -1) {
            item.style.display = 'flex'

            let hasResults = true;
          } else {
            item.style.display = 'none'
          }
        })

        if (hasResults) {
          noResults.style.display = 'none';
        } else{
          noResults.style.display = 'block';
        }
      });

  const localizationInput = document.getElementById('localizat');
      searchInput.addEventListener('input', (event) => {
        const value = formatString(event.target.value);
        const noResults = document.getElementById('no_results');
        const items = document.querySelectorAll('') //Colocar o nome da lista de empregos que vamos criar

        let hasResults = false;

        items.forEach(item =>{
          //Aqui podemos manipular o item que quisermos da lista
          if(formatString(item.textContent).indexOf(value) !== -1) {
            item.style.display = 'flex'

            let hasResults = true;
          } else {
            item.style.display = 'none'
          }
        })

        if (hasResults) {
          noResults.style.display = 'none';
        } else{
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

