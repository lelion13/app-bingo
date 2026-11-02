if (!requireAuthPage()) {
  /* redirecting */
}

const inputSegundos = document.getElementById("modalSegundos");
const inputTamanoCm = document.getElementById("modalTamanoCm");
const guardarBtn = document.getElementById("guardarBtn");
const mensaje = document.getElementById("mensajeGuardado");

async function bootConfig() {
  try {
    const cfg = await loadConfigFromServer();
    inputSegundos.value = cfg.modal_seconds;
    inputTamanoCm.value = cfg.modal_cm;
  } catch (_) {
    inputSegundos.value = getModalSegundos();
    inputTamanoCm.value = getModalTamanoCm();
  }
}

guardarBtn.addEventListener("click", async () => {
  try {
    const saved = await saveConfigToServer(inputSegundos.value, inputTamanoCm.value);
    inputSegundos.value = saved.modal_seconds;
    inputTamanoCm.value = saved.modal_cm;
    mensaje.classList.remove("hidden");
    setTimeout(() => mensaje.classList.add("hidden"), 2000);
  } catch (_) {
    mensaje.textContent = "No se pudo guardar.";
    mensaje.classList.remove("hidden");
  }
});

[inputSegundos, inputTamanoCm].forEach((el) => {
  el.addEventListener("keydown", (e) => {
    if (e.key === "Enter") guardarBtn.click();
  });
});

bootConfig();
