/** Config de sesión (sessionStorage). Se pierde al cerrar el navegador. */
const CONFIG_MODAL_KEY = "bingo_modal_segundos";
const CONFIG_MODAL_DEFAULT = 3;
const CONFIG_MODAL_MIN = 1;
const CONFIG_MODAL_MAX = 30;

const CONFIG_MODAL_CM_KEY = "bingo_modal_cm";
const CONFIG_MODAL_CM_DEFAULT = 8;
const CONFIG_MODAL_CM_MIN = 3;
const CONFIG_MODAL_CM_MAX = 20;
/** Proporción del diámetro del círculo → tamaño de fuente del número */
const CONFIG_MODAL_NUMERO_RATIO = 0.55;

function clampNumber(n, min, max, fallback) {
  if (!Number.isFinite(n)) return fallback;
  return Math.min(max, Math.max(min, n));
}

function getModalSegundos() {
  const n = Number(sessionStorage.getItem(CONFIG_MODAL_KEY));
  return Math.round(clampNumber(n, CONFIG_MODAL_MIN, CONFIG_MODAL_MAX, CONFIG_MODAL_DEFAULT));
}

function setModalSegundos(segundos) {
  const value = Math.round(
    clampNumber(Number(segundos), CONFIG_MODAL_MIN, CONFIG_MODAL_MAX, CONFIG_MODAL_DEFAULT)
  );
  sessionStorage.setItem(CONFIG_MODAL_KEY, String(value));
  return value;
}

function getModalDuracionMs() {
  return getModalSegundos() * 1000;
}

function getModalTamanoCm() {
  const n = Number(sessionStorage.getItem(CONFIG_MODAL_CM_KEY));
  return clampNumber(n, CONFIG_MODAL_CM_MIN, CONFIG_MODAL_CM_MAX, CONFIG_MODAL_CM_DEFAULT);
}

function setModalTamanoCm(cm) {
  const value = clampNumber(Number(cm), CONFIG_MODAL_CM_MIN, CONFIG_MODAL_CM_MAX, CONFIG_MODAL_CM_DEFAULT);
  // un decimal para permitir 7.5 cm, etc.
  const rounded = Math.round(value * 10) / 10;
  sessionStorage.setItem(CONFIG_MODAL_CM_KEY, String(rounded));
  return rounded;
}

/**
 * Aplica el diámetro del modal circular y el número en proporción (cm).
 * @param {HTMLElement} modalEl círculo del modal
 * @param {HTMLElement} valorEl span del número
 */
function aplicarTamanoModal(modalEl, valorEl) {
  const cm = getModalTamanoCm();
  if (modalEl) {
    modalEl.style.width = `${cm}cm`;
    modalEl.style.height = `${cm}cm`;
  }
  if (valorEl) {
    valorEl.style.fontSize = `${cm * CONFIG_MODAL_NUMERO_RATIO}cm`;
  }
}
