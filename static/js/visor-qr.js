/** QR + link al visor de producción del usuario logueado. */
const VISOR_PROD_HOST = "bingo.lionapp.cloud";

function visorProdUrlFor(username) {
  const u = String(username || "").trim().toLowerCase();
  return `https://${VISOR_PROD_HOST}/visor/${encodeURIComponent(u)}`;
}

function visorProdLabelFor(username) {
  const u = String(username || "").trim().toLowerCase();
  return `${VISOR_PROD_HOST}/visor/${u}`;
}

function initVisorQr(username) {
  const host = document.getElementById("visorQr");
  const link = document.getElementById("visorLink");
  if (!host || !username) return;

  const url = visorProdUrlFor(username);
  const label = visorProdLabelFor(username);

  if (link) {
    link.href = url;
    link.textContent = label;
  }

  if (typeof QRCode === "undefined") {
    host.textContent = "QR no disponible";
    return;
  }

  host.innerHTML = "";
  // eslint-disable-next-line no-new
  new QRCode(host, {
    text: url,
    width: 112,
    height: 112,
    colorDark: "#1e1b4b",
    colorLight: "#ffffff",
    correctLevel: QRCode.CorrectLevel.M,
  });
}
