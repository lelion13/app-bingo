/** Config del usuario autenticado (fuente de verdad: API / SQLite). */
const CONFIG_MODAL_DEFAULT = 3;
const CONFIG_MODAL_MIN = 1;
const CONFIG_MODAL_MAX = 30;

const CONFIG_MODAL_CM_DEFAULT = 8;
const CONFIG_MODAL_CM_MIN = 3;
const CONFIG_MODAL_CM_MAX = 20;
const CONFIG_MODAL_NUMERO_RATIO = 0.55;

let _modalSeconds = CONFIG_MODAL_DEFAULT;
let _modalCm = CONFIG_MODAL_CM_DEFAULT;
let _configLoaded = false;

function clampNumber(n, min, max, fallback) {
  if (!Number.isFinite(n)) return fallback;
  return Math.min(max, Math.max(min, n));
}

function getModalSegundos() {
  return Math.round(clampNumber(_modalSeconds, CONFIG_MODAL_MIN, CONFIG_MODAL_MAX, CONFIG_MODAL_DEFAULT));
}

function getModalDuracionMs() {
  return getModalSegundos() * 1000;
}

function getModalTamanoCm() {
  return clampNumber(_modalCm, CONFIG_MODAL_CM_MIN, CONFIG_MODAL_CM_MAX, CONFIG_MODAL_CM_DEFAULT);
}

function applyConfigValues(seconds, cm) {
  _modalSeconds = Math.round(
    clampNumber(Number(seconds), CONFIG_MODAL_MIN, CONFIG_MODAL_MAX, CONFIG_MODAL_DEFAULT)
  );
  const rawCm = clampNumber(Number(cm), CONFIG_MODAL_CM_MIN, CONFIG_MODAL_CM_MAX, CONFIG_MODAL_CM_DEFAULT);
  _modalCm = Math.round(rawCm * 10) / 10;
  _configLoaded = true;
  return { modal_seconds: _modalSeconds, modal_cm: _modalCm };
}

async function loadConfigFromServer() {
  const res = await authFetch("/api/config/");
  if (!res.ok) throw new Error("config load failed");
  const data = await res.json();
  return applyConfigValues(data.modal_seconds, data.modal_cm);
}

async function saveConfigToServer(seconds, cm) {
  const payload = applyConfigValues(seconds, cm);
  const res = await authFetch("/api/config/", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("config save failed");
  const data = await res.json();
  return applyConfigValues(data.modal_seconds, data.modal_cm);
}

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
