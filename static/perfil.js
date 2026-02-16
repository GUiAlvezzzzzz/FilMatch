async function saveProfile() {
  const user_id = localStorage.getItem("user_id");

  if (!user_id) {
    alert("Sessão expirada. Faça login novamente.");
    window.location.href = "/";
    return;
  }

  await fetch("/profile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      user_id: user_id,
      action: Number(action.value),
      drama: Number(drama.value),
      comedy: Number(comedy.value),
      scifi: Number(scifi.value)
    })
  });

  window.location.href = "/recomendador";
}
