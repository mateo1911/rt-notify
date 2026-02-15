function getToken() {
  return localStorage.getItem("token");
}

async function refreshAccessToken() {
  const res = await fetch("/auth/refresh", {
    method: "POST",
    credentials: "same-origin", // bitno: šalje refresh cookie
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || !data.access_token) return null;

  localStorage.setItem("token", data.access_token);
  return data.access_token;
}

async function api(path, options = {}) {
  const token = getToken();
  const headers = { ...(options.headers || {}) };

  if (token) headers["Authorization"] = "Bearer " + token;

  const fetchOpts = {
    credentials: "same-origin", // bitno za cookie
    ...options,
    headers,
  };

  let res = await fetch(path, fetchOpts);
  let data = await res.json().catch(() => ({}));

  // access istekao -> refresh jednom pa retry
  if ((res.status === 401 || res.status === 422) && path !== "/auth/refresh") {
    const newToken = await refreshAccessToken();
    if (newToken) {
      fetchOpts.headers["Authorization"] = "Bearer " + newToken;
      res = await fetch(path, fetchOpts);
      data = await res.json().catch(() => ({}));
    }
  }

  return { res, data };
}

function formatTs(ts) {
  if (!ts) return "";
  const d = new Date(ts * 1000);
  return d.toLocaleString();
}

async function load() {
  const { res: r1, data: d1 } = await api("/notifications/unread-count");
  console.log("unread-count status:", r1.status, "data:", d1);

  // redirect samo ako refresh nije pomogao
  if (r1.status === 401 || r1.status === 422) {
    window.location.replace("/login");
    return;
  }

  const unreadEl = document.getElementById("unread");
  if (unreadEl) unreadEl.textContent = d1.unread ?? 0;

  const { res: r2, data: list } = await api("/notifications");
  const ul = document.getElementById("list");
  if (!ul) return;

  ul.innerHTML = "";
if (r2.ok && Array.isArray(list)) {
  list.forEach((n) => {
    const li = document.createElement("li");
    li.className = "item";

    const from = document.createElement("b");
    from.textContent = n.from_user || "system";

    const text = document.createElement("span");
    text.textContent = ": " + (n.message || "");

    const br = document.createElement("br");

    const time = document.createElement("small");
    time.textContent = formatTs(n.ts);

    li.appendChild(from);
    li.appendChild(text);
    li.appendChild(br);
    li.appendChild(time);

    ul.appendChild(li);
  });
}
}

document.addEventListener("DOMContentLoaded", () => {
  // ako nema access tokena, probaj refresh iz cookie-a prije redirecta
  (async () => {
    if (!getToken()) {
      const newToken = await refreshAccessToken();
      if (!newToken) {
        window.location.replace("/login");
        return;
      }
    }

    const meEl = document.getElementById("me");
    if (meEl) meEl.textContent = localStorage.getItem("username") || "-";

    // logout: obriši cookie (server) + local storage
    const logoutBtn = document.getElementById("logout");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        await fetch("/auth/logout", { method: "POST", credentials: "same-origin" });
        localStorage.removeItem("token");
        localStorage.removeItem("username");
        window.location.replace("/login");
      });
    }

    // send notification
    const sendForm = document.getElementById("sendForm");
    if (sendForm) {
      sendForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const to_user = document.getElementById("toUser")?.value?.trim();
        const message = document.getElementById("message")?.value?.trim();

        const msgEl = document.getElementById("sendMsg");

        if (!to_user || !message) {
          if (msgEl) msgEl.textContent = "Upiši To user i Message.";
          return;
        }

        const { res, data } = await api("/notifications", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ to_user, message }),
        });

        if (msgEl) msgEl.textContent = res.ok ? "Sent ✅" : (data.error || "Error");

        if (res.ok) {
          const messageEl = document.getElementById("message");
          if (messageEl) messageEl.value = "";
          setTimeout(load, 500);
        }
      });
    }

    // refresh
    const refreshBtn = document.getElementById("refresh");
    if (refreshBtn) refreshBtn.addEventListener("click", load);

    // mark read
    const markReadBtn = document.getElementById("markRead");
    if (markReadBtn) {
      markReadBtn.addEventListener("click", async () => {
        await api("/notifications/mark-read", { method: "POST" });
        load();
      });
    }

    // clear messages
    const clearBtn = document.getElementById("clear");
    if (clearBtn) {
      clearBtn.addEventListener("click", async () => {
        if (!confirm("Obrisati sve poruke?")) return;
        await api("/notifications/clear", { method: "POST" });
        load();
      });
    }

    load();
    setInterval(load, 2500);
  })();
});