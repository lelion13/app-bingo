const inputSegundos = document.getElementById("modalSegundos");
const inputTamanoCm = document.getElementById("modalTamanoCm");
const guardarBtn = document.getElementById("guardarBtn");
const mensaje = document.getElementById("mensajeGuardado");

inputSegundos.value = getModalSegundos();
inputTamanoCm.value = getModalTamanoCm();

guardarBtn.addEventListener("click", () => {
  inputSegundos.value = setModalSegundos(inputSegundos.value);
  inputTamanoCm.value = setModalTamanoCm(inputTamanoCm.value);
  mensaje.classList.remove("hidden");
  setTimeout(() => mensaje.classList.add("hidden"), 2000);
});

[inputSegundos, inputTamanoCm].forEach((el) => {
  el.addEventListener("keydown", (e) => {
    if (e.key === "Enter") guardarBtn.click();
  });
});
