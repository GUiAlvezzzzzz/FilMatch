/* CONTROLE DE SESSÃO */
const userId = localStorage.getItem("user_id");

if (!userId) {
  window.location.href = "/";
}

/* PREFERÊNCIAS (TEMA + IDIOMA) */
let lang = localStorage.getItem("lang") || "pt";
let theme = localStorage.getItem("theme") || "light";

/* ELEMENTOS DO TOPO */
const langBtn = document.getElementById("langToggle");
const themeBtn = document.getElementById("themeToggle");

/*  IDIOMA  */
langBtn.innerText = lang === "pt" ? "🇧🇷" : "🇺🇸";

langBtn.onclick = () => {
  lang = lang === "pt" ? "en" : "pt";
  localStorage.setItem("lang", lang);
  location.reload();
};

/*  TEMA  */
if (theme === "dark") {
  document.body.classList.add("dark");
  themeBtn.innerText = "☀️";
} else {
  themeBtn.innerText = "🌙";
}

themeBtn.onclick = () => {
  document.body.classList.toggle("dark");

  if (document.body.classList.contains("dark")) {
    localStorage.setItem("theme", "dark");
    themeBtn.innerText = "☀️";
  } else {
    localStorage.setItem("theme", "light");
    themeBtn.innerText = "🌙";
  }
};

/*ELEMENTOS BASE */
const header = document.getElementById("header");
const app = document.getElementById("app");

/* HEADER  */
header.innerHTML = `
  <h1 class="h1main">🎬 FilMatch</h1>
  <p class="pmain">
    ${lang === "pt"
      ? "Descubra os filmes que dão match com você."
      : "Discover movies that match your taste."}
  </p>
`;

/* FORM */
const form = document.createElement("section");
form.className = "form";

form.innerHTML = `
  <div class="ranges">
    <label>${lang === "pt" ? "Ação" : "Action"}
      <input type="range" id="action" min="1" max="5" value="3">
    </label>

    <label>${lang === "pt" ? "Drama" : "Drama"}
      <input type="range" id="drama" min="1" max="5" value="3">
    </label>

    <label>${lang === "pt" ? "Comédia" : "Comedy"}
      <input type="range" id="comedy" min="1" max="5" value="3">
    </label>

    <label>${lang === "pt" ? "Ficção" : "Sci-Fi"}
      <input type="range" id="scifi" min="1" max="5" value="3">
    </label>
  </div>

  <div class="buttons">
    <button class="Rec" id="getRec">
      ${lang === "pt" ? "Buscar filmes" : "Get recommendations"}
    </button>
  </div>
`;

app.appendChild(form);

/* RESULTADOS */
const results = document.createElement("ul");
results.id = "results";
results.className = "results";
app.appendChild(results);

document.getElementById("getRec").onclick = getRecommendations;

/* RENDER DOS FILMES  */
function renderMovies(movies) {
  results.innerHTML = "";

  movies.forEach(movie => {
    const li = document.createElement("li");
    li.className = "movie-card";

    const feedbackKey = `feedback_${userId}_${movie.title}`;
    const savedFeedback = localStorage.getItem(feedbackKey);

    li.innerHTML = `
      <img src="${movie.poster}" alt="${movie.title}" class="movie-img">
      <h3>${movie.title}</h3>
      <p>${lang === "pt" ? "Nota TMDB" : "TMDB Rating"}: ${movie.vote ?? "—"}</p>
      <p>${lang === "pt" ? "Afinidade" : "Match"}: ${movie.score ?? "—"}</p>
      <div class="actions">
        <button class="like"></button>
        <button class="dislike"></button>
      </div>
    `;

    const likeBtn = li.querySelector(".like");
    const dislikeBtn = li.querySelector(".dislike");

    
    if (savedFeedback === "like") likeBtn.classList.add("active-like");
    if (savedFeedback === "dislike") dislikeBtn.classList.add("active-dislike");

    likeBtn.onclick = () => {
      const current = localStorage.getItem(feedbackKey);

      if (current === "like") {
        localStorage.removeItem(feedbackKey);
        likeBtn.classList.remove("active-like");
      } else {
        localStorage.setItem(feedbackKey, "like");
        likeBtn.classList.add("active-like");
        dislikeBtn.classList.remove("active-dislike");
      }

      sendFeedback(movie.title, "like");
    };

    dislikeBtn.onclick = () => {
      const current = localStorage.getItem(feedbackKey);

      if (current === "dislike") {
        localStorage.removeItem(feedbackKey);
        dislikeBtn.classList.remove("active-dislike");
      } else {
        localStorage.setItem(feedbackKey, "dislike");
        dislikeBtn.classList.add("active-dislike");
        likeBtn.classList.remove("active-like");
      }

      sendFeedback(movie.title, "dislike");
    };

    // Abrir modal
    li.querySelector(".movie-img").onclick = () => openModal(movie);

    results.appendChild(li);
  });
}

/* BUSCAR RECOMENDAÇÕES  */
async function getRecommendations() {
  const profile = {
    action: Number(document.getElementById("action").value),
    drama: Number(document.getElementById("drama").value),
    comedy: Number(document.getElementById("comedy").value),
    scifi: Number(document.getElementById("scifi").value)
  };

  const response = await fetch(`/recommend?lang=${lang}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile)
  });

  if (!response.ok) {
    alert("Erro ao buscar recomendações");
    return;
  }

  const movies = await response.json();
  renderMovies(movies);
}

/*  FEEDBACK BACKEND */
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
}

/*  MODAL */

async function openModal(movie) {
  const modal = document.createElement("div");
  modal.className = "modal-overlay";

  modal.innerHTML = `
    <div class="modal-content">
      <span class="close-btn">&times;</span>
      <img src="${movie.poster}" class="modal-poster">
      <div class="modal-info">
        <h2>${movie.title}</h2>
        <p><strong>${lang === "pt" ? "Lançamento" : "Release"}:</strong> ${movie.release_date ?? "—"}</p>
        <p><strong>⭐ TMDB:</strong> ${movie.vote ?? "—"}</p>
        <p class="overview">
          ${movie.overview ?? (lang === "pt"
            ? "Sem descrição disponível."
            : "No description available.")}
        </p>

        <div class="providers-container">
          <p>${lang === "pt" ? "Carregando plataformas..." : "Loading providers..."}</p>
        </div>

      </div>
    </div>
  `;

  document.body.appendChild(modal);

  modal.querySelector(".close-btn").onclick = () => modal.remove();
  modal.onclick = (e) => {
    if (e.target === modal) modal.remove();
  };

  // 🔽 BUSCAR PLATAFORMAS
  try {
    const response = await fetch(`/providers/${movie.id}`);
    if (!response.ok) throw new Error("Erro ao buscar providers");

    const providers = await response.json();

    const container = modal.querySelector(".providers-container");

    if (providers && providers.length > 0) {
      container.innerHTML = `
        <h3>${lang === "pt" ? "Onde assistir:" : "Where to watch:"}</h3>
      `;

      providers.forEach(provider => {
        const logoUrl = `https://image.tmdb.org/t/p/w200${provider.logo_path}`;

        container.innerHTML += `
          <div class="provider">
            <img src="${logoUrl}" alt="${provider.provider_name}">
            <span>${provider.provider_name}</span>
          </div>
        `;
      });

    } else {
      container.innerHTML = `
        <p>${lang === "pt"
          ? "Não disponível em streaming no Brasil."
          : "Not available for streaming in your region."}
        </p>
      `;
    }

  } catch (error) {
    console.error("Erro ao carregar plataformas:", error);
  }
}
