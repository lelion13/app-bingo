/** QR + link al visor de producción (siempre, aunque el home sea local). */
const VISOR_PROD_URL = "https://bingo.lionapp.cloud/visor";

function initVisorQr() {
  const host = document.getElementById("visorQr");
  const link = document.getElementById("visorLink");
  if (!host) return;

  if (link) {
    link.href = VISOR_PROD_URL;
    link.textContent = "bingo.lionapp.cloud/visor";
  }

  if (typeof QRCode === "undefined") {
    host.textContent = "QR no disponible";
    return;
  }

  host.innerHTML = "";
  // qrcodejs: dibuja en el contenedor
  // eslint-disable-next-line no-new
  new QRCode(host, {
    text: VISOR_PROD_URL,
    width: 112,
    height: 112,
    colorDark: "#1e1b4b",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M,
  });
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initVisorQr);
} else {
  initVisorQr();
}
