(function () {
  const $ = (id) => document.getElementById(id);
  const focusEl = $("focus");
  const companyEl = $("company");
  const numEl = $("num");
  const goBtn = $("go");
  const statusEl = $("status");
  const resultsEl = $("results");

  const DEFAULTS = {
    focus: "Electric vehicle market in Europe",
    company: "ACME Europe",
    num_ideas: 5,
  };

  function cleanStr(v, dflt) {
    if (v === undefined || v === null) return dflt;
    const s = String(v).trim();
    if (!s || ["undefined", "null", "none"].includes(s.toLowerCase())) return dflt;
    return s;
  }
  function cleanInt(v, dflt) {
    const s = cleanStr(v, String(dflt));
    const n = parseInt(s, 10);
    if (Number.isNaN(n)) return dflt;
    return Math.min(50, Math.max(1, n));
  }

  function setStatus(msg, ok = true, spin = false) {
    statusEl.innerHTML = (spin ? '<span class="spinner"></span>' : "") +
      `<span class="${ok ? "ok" : "err"}">${msg}</span>`;
  }

  function buildUrl(focus, company, numIdeas) {
    const params = new URLSearchParams({
      focus: cleanStr(focus, DEFAULTS.focus),
      company: cleanStr(company, DEFAULTS.company),
      num_ideas: String(cleanInt(numIdeas, DEFAULTS.num_ideas)),
    });
    const url = `/api/discover?${params.toString()}`;
    console.log("Fetching:", url); // ✅ sanity log (you'll see the real URL, no 'undefined')
    return url;
  }

  function card(v) {
    const scores = v.score_breakdown || {};
    const tags = [
      `Feasibility: ${v.feasibility_score ?? "–"}`,
      `Size: ${scores.market_size ?? "–"}`,
      `Growth: ${scores.market_growth ?? "–"}`,
      `Fit: ${scores.strategic_fit ?? "–"}`
    ];
    const feats = (v.insights?.features || []).slice(0, 5);
    const url = v.URL || "#";

    return `
      <div class="card">
        <h3>${escapeHtml(v.idea || "Untitled")}</h3>
        <div class="rowline">${tags.map(t => `<span class="tag">${escapeHtml(t)}</span>`).join("")}</div>
        <p>${escapeHtml(v.summary || "No summary")}</p>
        ${feats.length ? `<div class="rowline">${feats.map(f => `<span class="tag">${escapeHtml(f)}</span>`).join("")}</div>` : ""}
        <div class="url"><a href="${url}" target="_blank" rel="noopener">Open link</a></div>
      </div>
    `;
  }

  function render(data) {
    const arr = Array.isArray(data?.ventures) ? data.ventures : [];
    if (!arr.length) {
      resultsEl.innerHTML = "";
      setStatus("No ventures returned.", false);
      return;
    }
    resultsEl.innerHTML = arr.map(card).join("");
    setStatus(`Done • ${arr.length} venture(s) • ${data.timestamp}`, true, false);
  }

  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  async function run() {
    // Read inputs safely and apply defaults client-side too
    const focus = cleanStr(focusEl?.value, DEFAULTS.focus);
    const company = cleanStr(companyEl?.value, DEFAULTS.company);
    const numIdeas = cleanInt(numEl?.value, DEFAULTS.num_ideas);

    // Update boxes with cleaned values (helps avoid 'undefined' if fields were empty)
    if (focusEl) focusEl.value = focus;
    if (companyEl) companyEl.value = company;
    if (numEl) numEl.value = String(numIdeas);

    const url = buildUrl(focus, company, numIdeas);
    try {
      setStatus("Working…", true, true);
      goBtn.disabled = true;
      resultsEl.innerHTML = "";
      const res = await fetch(url);
      if (!res.ok) {
        const txt = await res.text();
        throw new Error(`HTTP ${res.status}: ${txt}`);
      }
      const data = await res.json();
      render(data);
    } catch (e) {
      console.error(e);
      setStatus(e.message || "Request failed", false);
    } finally {
      goBtn.disabled = false;
    }
  }

  goBtn?.addEventListener("click", run);

  // Optional: auto-run once on load with defaults
  setTimeout(() => {
    if (resultsEl?.children.length === 0) run();
  }, 150);
})();
