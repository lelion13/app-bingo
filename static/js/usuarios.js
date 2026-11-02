if (!requireAdminPage()) {
  /* redirecting */
}

const userList = document.getElementById("userList");
const createForm = document.getElementById("createForm");
const createMsg = document.getElementById("createMsg");

async function loadUsers() {
  const res = await authFetch("/api/users/");
  const users = await res.json();
  userList.innerHTML = "";
  users.forEach((u) => {
    const row = document.createElement("div");
    row.className = "p-3 rounded-xl border border-slate-200 bg-white flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between";
    row.innerHTML = `
      <div>
        <p class="font-bold text-slate-800">${u.username}</p>
        <p class="text-sm text-slate-500">${u.role} · ${u.active ? "activo" : "desactivado"}</p>
      </div>
      <div class="flex flex-wrap gap-2">
        <select data-role="${u.id}" class="field !w-auto">
          <option value="operador" ${u.role === "operador" ? "selected" : ""}>operador</option>
          <option value="admin" ${u.role === "admin" ? "selected" : ""}>admin</option>
        </select>
        <input data-pass="${u.id}" type="password" class="field !w-36" placeholder="nueva clave" minlength="6" />
        <button data-save="${u.id}" type="button" class="px-3 py-2 rounded-xl bg-slate-800 text-white text-sm font-bold">Guardar</button>
        <button data-toggle="${u.id}" data-active="${u.active}" type="button" class="px-3 py-2 rounded-xl text-sm font-bold ${u.active ? "bg-rose-500 text-white" : "bg-emerald-500 text-white"}">
          ${u.active ? "Desactivar" : "Activar"}
        </button>
      </div>
    `;
    userList.appendChild(row);
  });
}

createForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  createMsg.classList.add("hidden");
  const body = {
    username: document.getElementById("newUsername").value,
    password: document.getElementById("newPassword").value,
    role: document.getElementById("newRole").value,
  };
  const res = await authFetch("/api/users/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    createMsg.textContent = typeof data.detail === "string" ? data.detail : "No se pudo crear";
    createMsg.className = "mt-2 text-sm font-semibold text-rose-600";
    createMsg.classList.remove("hidden");
    return;
  }
  createForm.reset();
  createMsg.textContent = `Creado: ${data.username}`;
  createMsg.className = "mt-2 text-sm font-semibold text-emerald-600";
  createMsg.classList.remove("hidden");
  await loadUsers();
});

userList.addEventListener("click", async (e) => {
  const saveId = e.target.getAttribute("data-save");
  const toggleId = e.target.getAttribute("data-toggle");
  if (saveId) {
    const roleEl = userList.querySelector(`select[data-role="${saveId}"]`);
    const passEl = userList.querySelector(`input[data-pass="${saveId}"]`);
    const payload = { role: roleEl.value };
    if (passEl.value) payload.password = passEl.value;
    const res = await authFetch(`/api/users/${saveId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      alert("No se pudo guardar");
      return;
    }
    passEl.value = "";
    await loadUsers();
  }
  if (toggleId) {
    const active = e.target.getAttribute("data-active") === "true";
    const res = await authFetch(`/api/users/${toggleId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ active: !active }),
    });
    if (!res.ok) {
      alert("No se pudo cambiar el estado");
      return;
    }
    await loadUsers();
  }
});

loadUsers().catch(() => {
  userList.innerHTML = `<p class="text-rose-600 font-semibold">Error al cargar usuarios</p>`;
});
