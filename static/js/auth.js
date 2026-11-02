/** JWT session helpers (localStorage). */
const AUTH_TOKEN_KEY = "bingo_access_token";
const AUTH_USER_KEY = "bingo_auth_user";

function getAccessToken() {
  return localStorage.getItem(AUTH_TOKEN_KEY) || "";
}

function getAuthUser() {
  try {
    const raw = localStorage.getItem(AUTH_USER_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (_) {
    return null;
  }
}

function setAuthSession({ access_token, username, role }) {
  localStorage.setItem(AUTH_TOKEN_KEY, access_token);
  localStorage.setItem(AUTH_USER_KEY, JSON.stringify({ username, role }));
}

function clearAuthSession() {
  localStorage.removeItem(AUTH_TOKEN_KEY);
  localStorage.removeItem(AUTH_USER_KEY);
}

function authHeaders(extra = {}) {
  const token = getAccessToken();
  const headers = { ...extra };
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

async function authFetch(url, options = {}) {
  const opts = { ...options };
  opts.headers = authHeaders(opts.headers || {});
  const res = await fetch(url, opts);
  if (res.status === 401) {
    clearAuthSession();
    const next = encodeURIComponent(window.location.pathname + window.location.search);
    window.location.href = `/login?next=${next}`;
    throw new Error("No autenticado");
  }
  return res;
}

function requireAuthPage() {
  if (!getAccessToken()) {
    const next = encodeURIComponent(window.location.pathname + window.location.search);
    window.location.href = `/login?next=${next}`;
    return false;
  }
  return true;
}

function requireAdminPage() {
  if (!requireAuthPage()) return false;
  const user = getAuthUser();
  if (!user || user.role !== "admin") {
    window.location.href = "/";
    return false;
  }
  return true;
}

function logout() {
  clearAuthSession();
  window.location.href = "/login";
}
