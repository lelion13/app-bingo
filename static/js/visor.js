const ultimaEl = document.getElementById("ultima");
const salidasEl = document.getElementById("salidas");
const contadorEl = document.getElementById("contador");
const totalSalidasEl = document.getElementById("totalSalidas");

const POLL_MS = 1500;
let lastSignature = "";
const visorUsername = String(window.VISOR_USERNAME || "").trim().toLowerCase();

function getColorBolilla(numero) {
  if (numero >= 1 && numero <= 10) return "#ff6b6b";
  if (numero >= 11 && numero <= 20) return "#4dabf7";
  if (numero >= 21 && numero <= 30) return "#51cf66";
  if (numero >= 31 && numero <= 40) return "#ffd43b";
  if (numero >= 41 && numero <= 50) return "#ff8787";
  if (numero >= 51 && numero <= 60) return "#f7a83b";
  if (numero >= 61 && numero <= 70) return "#a288e8";
  if (numero >= 71 && numero <= 80) return "#7ecfd4";
  if (numero >= 81 && numero <= 90) return "#b0b0b0";
  return "#ff6b6b";
}

function renderEstado(data) {
  const salidas = Array.isArray(data.salidas) ? data.salidas : [];
  const restantes = typeof data.restantes === "number" ? data.restantes : "—";
  const signature = `${restantes}|${salidas.join(",")}`;
  if (signature === lastSignature) return;
  lastSignature = signature;

  contadorEl.textContent = `Restantes: ${restantes}`;
  totalSalidasEl.textContent = String(salidas.length);

  if (salidas.length === 0) {
    ultimaEl.className = "ultima-vacia";
    ultimaEl.textContent = "Esperando sorteo…";
    salidasEl.innerHTML = "";
    return;
  }

  const ultima = salidas[salidas.length - 1];
  ultimaEl.className = "ultima-numero";
  ultimaEl.textContent = String(ultima);
  ultimaEl.style.color = getColorBolilla(ultima);

  const orden = [...salidas].reverse();
  salidasEl.innerHTML = "";
  orden.forEach((numero, index) => {
    const div = document.createElement("div");
    div.className = "bolilla" + (index === 0 ? " is-latest" : "");
    const color = getColorBolilla(numero);
    div.style.background = `radial-gradient(circle at 30% 30%, #fff, ${color}, ${color})`;
    div.textContent = String(numero);
    salidasEl.appendChild(div);
  });
}

async function pollEstado() {
  if (!visorUsername) return;
  try {
    const res = await fetch(`/estado/${encodeURIComponent(visorUsername)}`);
    if (!res.ok) return;
    const data = await res.json();
    renderEstado(data);
  } catch (_) {
    // silencioso
  }
}

pollEstado();
setInterval(pollEstado, POLL_MS);
