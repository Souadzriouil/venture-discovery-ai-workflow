// Small API helper with input sanitization
export const DEFAULTS = {
  focus: "Electric vehicle market in Europe",
  company: "ACME Europe",
  num_ideas: 5,
};

export function cleanStr(v: unknown, dflt: string): string {
  const s = (v ?? "").toString().trim();
  if (!s || ["undefined", "null", "none"].includes(s.toLowerCase())) return dflt;
  return s;
}

export function cleanInt(v: unknown, dflt: number): number {
  const n = Number.parseInt((v ?? dflt).toString(), 10);
  if (Number.isNaN(n)) return dflt;
  return Math.min(50, Math.max(1, n));
}

const API_BASE = import.meta.env.VITE_API_BASE ?? ""; // leave empty to use Vite proxy

export async function discover(focus?: string, company?: string, numIdeas?: number) {
  const f = cleanStr(focus, DEFAULTS.focus);
  const c = cleanStr(company, DEFAULTS.company);
  const n = cleanInt(numIdeas, DEFAULTS.num_ideas);

  const qs = new URLSearchParams({ focus: f, company: c, num_ideas: String(n) });
  const url = `${API_BASE}/api/discover?${qs.toString()}`;
  console.log("GET", url); // sanity log

  const res = await fetch(url);
  if (!res.ok) {
    const txt = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status}${txt ? `: ${txt.slice(0, 200)}` : ""}`);
  }
  return res.json();
}
