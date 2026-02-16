function register() {
  fetch("/register", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: document.getElementById("name").value,
      age: document.getElementById("age").value,
      email: document.getElementById("email").value,
      password: document.getElementById("password").value
    })
  })
  .then(r => r.json())
  .then(res => {
    document.getElementById("msg").innerText =
      res.error || "Cadastro feito! Agora é só logar 😉"
  })
}

function login() {
  fetch("/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: document.getElementById("email").value,
      password: document.getElementById("password").value
    })
  })
  .then(r => {
    if (!r.ok) throw new Error("Erro")
    return r.json()
  })
  .then(() => {
    window.location.href = "/recomendador"
  })
  .catch(() => {
    document.getElementById("msg").innerText =
      "Email ou senha inválidos"
  })
}
