if (getAccessToken()) {
  window.location.href = "/";
}

const form = document.getElementById("loginForm");
const errorMsg = document.getElementById("errorMsg");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  errorMsg.classList.add("hidden");
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value;

  try {
    const res = await fetch("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      errorMsg.textContent = data.detail || "Credenciales inválidas";
      errorMsg.classList.remove("hidden");
      return;
    }
    setAuthSession({
      access_token: data.access_token,
      username: data.username,
      role: data.role,
    });
    const params = new URLSearchParams(window.location.search);
    const next = params.get("next") || "/";
    window.location.href = next.startsWith("/") ? next : "/";
  } catch (_) {
    errorMsg.textContent = "No se pudo conectar. Reintentá.";
    errorMsg.classList.remove("hidden");
  }
});
