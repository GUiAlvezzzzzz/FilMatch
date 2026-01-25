let userId = null;

const header = document.getElementById("header");
const app = document.getElementById("app");

/* ---------- HEADER ---------- */
header.innerHTML = `
  <h1 class="h1main">🎬 FilMatch</h1>
  <p class="pmain">Descubra os filmes que dão match com você.</p>
`;

/* ---------- FORM ---------- */
const form = document.createElement("section");
form.className = "form";

form.innerHTML = `
  <input class="nome" id="name" placeholder="Seu nome">

  <div class="ranges">
    <label>Ação <input type="range" id="action" min="1" max="5" value="3"></label>
    <label>Drama <input type="range" id="drama" min="1" max="5" value="3"></label>
    <label>Comédia <input type="range" id="comedy" min="1" max="5" value="3"></label>
    <label>Ficção <input type="range" id="scifi" min="1" max="5" value="3"></label>
  </div>

  <div class="buttons">
    <button class="User" id="createUser">Criar perfil</button>
    <button class="Rec" id="getRec">Buscar filmes</button>
  </div>
`;

app.appendChild(form);

/* ---------- RESULTS ---------- */
const results = document.createElement("ul");
results.id = "results";
results.className = "results";
app.appendChild(results);

/* ---------- EVENTS ---------- */
document.getElementById("createUser").onclick = createUser;
document.getElementById("getRec").onclick = getRecommendations;

/* ---------- FUNCTIONS ---------- */

async function createUser() {
  const response = await fetch("/users", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: document.getElementById("name").value,
      action: Number(document.getElementById("action").value),
      drama: Number(document.getElementById("drama").value),
      comedy: Number(document.getElementById("comedy").value),
      scifi: Number(document.getElementById("scifi").value)
    })
  });

  if (!response.ok) {
    alert("Erro ao criar usuário");
    return;
  }

  const data = await response.json();
  userId = data.user_id;

  alert("Usuário criado com sucesso!");
}

async function getRecommendations() {
  if (!userId) {
    alert("Crie um perfil primeiro");
    return;
  }


  const response = await fetch(`/recommend/${userId}?t=${Date.now()}`, {
    cache: "no-store"
  });

  if (!response.ok) {
    alert("Erro ao buscar recomendações");
    return;
  }

  const movies = await response.json();
  results.innerHTML = "";

  movies.forEach(movie => {
    const li = document.createElement("li");
    li.className = "movie-card";

    li.innerHTML = `
    <img src="${movie.poster}" alt="${movie.title}">
    <h3>${movie.title}</h3>
    <p> Nota TMDB: ${movie.vote ?? "—"}</p>
    <p> Afinidade: ${movie.score ?? "—"}</p>
    <div class="actions">
      <button class="like"></button>
      <button class="dislike"></button>
    </div>
  `;


    li.querySelector(".like").onclick = () => sendFeedback(movie.title, 5);
    li.querySelector(".dislike").onclick = () => sendFeedback(movie.title, 1);

    results.appendChild(li);
  });
}

async function sendFeedback(title, rating) {
  await fetch("/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: userId,
      movie_title: title,
      rating
    })
  });

  alert("Feedback enviado!");
}
