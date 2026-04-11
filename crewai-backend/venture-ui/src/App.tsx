import { useEffect, useMemo, useState } from "react";

type Score = { market_size: number; market_growth: number; strategic_fit: number };
type Insights = {
  go_to_market: string;
  justification: string;
  value_proposition: string;
  features: string[];
  positioning: string;
  differentiation: string;
};
type WhiteSpace = { market_gap: string; company_fit: string };
export type Venture = {
  id: number;
  idea: string;
  summary: string;
  URL: string;
  score_breakdown: Score;
  feasibility_score: number;
  insights: Insights;
  white_space_analysis: WhiteSpace;
  citations?: string[];
};
type DiscoverResponse = { ventures: Venture[]; timestamp: string };

function useLocal<T>(key: string, initial: T) {
  const [v, setV] = useState<T>(() => {
    try { const raw = localStorage.getItem(key); return raw ? (JSON.parse(raw) as T) : initial; }
    catch { return initial; }
  });
  useEffect(() => { localStorage.setItem(key, JSON.stringify(v)); }, [key, v]);
  return [v, setV] as const;
}

export default function App() {
  const [focus, setFocus] = useLocal("vd.focus", "Electric vehicle market in Europe");
  const [company, setCompany] = useLocal("vd.company", "ACME Europe");
  const [ideas, setIdeas] = useLocal("vd.ideas", 5);
  const [ventures, setVentures] = useLocal<Venture[]>("vd.ventures", []);
  const [timestamp, setTs] = useLocal("vd.ts", "");
  const [theme, setTheme] = useLocal<"dark" | "light">("vd.theme", "dark");
  const [view, setView] = useLocal<"grid" | "list">("vd.view", "grid");
  const [sortBy, setSortBy] = useLocal<"feas" | "size" | "growth">("vd.sort", "feas");
  const [q, setQ] = useLocal("vd.q", "");

  const [loading, setLoading] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [open, setOpen] = useState<Venture | null>(null);

  useEffect(() => { document.documentElement.setAttribute("data-theme", theme); }, [theme]);

  const filteredSorted = useMemo(() => {
    const text = q.trim().toLowerCase();
    let list = !text ? ventures : ventures.filter(v =>
      v.idea.toLowerCase().includes(text) ||
      v.summary?.toLowerCase().includes(text) ||
      v.insights?.value_proposition?.toLowerCase().includes(text)
    );
    const key = (v: Venture) =>
      sortBy === "feas" ? v.feasibility_score :
      sortBy === "size" ? v.score_breakdown.market_size :
      v.score_breakdown.market_growth;
    list = list.slice().sort((a,b)=> Number(key(b)) - Number(key(a)));
    return list;
  }, [ventures, q, sortBy]);

  async function discover() {
    setLoading(true); setErr(null);
    try {
      const params = new URLSearchParams({
        focus: String(focus),
        company: String(company),
        num_ideas: String(ideas ?? 5),
      });
      const r = await fetch(`/api/discover?${params.toString()}`, { headers: { Accept: "application/json" } });
      if (!r.ok) throw new Error(`${r.status} ${r.statusText}`);
      const data = (await r.json()) as DiscoverResponse;
      setVentures(data.ventures || []); setTs(data.timestamp || new Date().toISOString());
    } catch (e: any) {
      setErr(e?.message ?? "Request failed");
    } finally {
      setLoading(false);
    }
  }

  function exportJSON() {
    const blob = new Blob([JSON.stringify({ ventures, timestamp }, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob); const a = document.createElement("a");
    a.href = url; a.download = "ventures.json"; a.click(); URL.revokeObjectURL(url);
  }
  function exportCSV() {
    const header = ["id","idea","feasibility","size","growth","fit","url"];
    const rows = ventures.map(v => [
      v.id, `"${v.idea.replace(/"/g,'""')}"`,
      v.feasibility_score, v.score_breakdown.market_size,
      v.score_breakdown.market_growth, v.score_breakdown.strategic_fit,
      v.URL || ""
    ].join(","));
    const csv = [header.join(","), ...rows].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob); const a = document.createElement("a");
    a.href = url; a.download = "ventures.csv"; a.click(); URL.revokeObjectURL(url);
  }

  return (
    <div className={`wrap ${view === "list" ? "view-list" : ""}`}>
      <div className="header">
        <div className="brand">Venture Discovery <span className="dim">— Multi-Agent</span></div>
        <div className="toolbar">
          <button className="btn btn-secondary" onClick={()=>setTheme(theme==="dark"?"light":"dark")}>
            {theme === "dark" ? "Light mode" : "Dark mode"}
          </button>
          <button className="btn btn-secondary" onClick={()=>setView(view==="grid"?"list":"grid")}>
            {view === "grid" ? "List view" : "Grid view"}
          </button>
          <button className="btn btn-secondary" disabled={!ventures.length} onClick={exportCSV}>Export CSV</button>
          <button className="btn btn-secondary" disabled={!ventures.length} onClick={exportJSON}>Export JSON</button>
        </div>
      </div>

      <div className="panel">
        <div className="controls">
          <div>
            <label>Focus area</label>
            <input className="input" value={focus} onChange={e=>setFocus(e.target.value)} placeholder="e.g. Electric vehicle market in Europe" />
          </div>
          <div>
            <label>Company</label>
            <input className="input" value={company} onChange={e=>setCompany(e.target.value)} placeholder="e.g. ACME Europe" />
          </div>
          <div>
            <label># ideas (1–20)</label>
            <input className="input" type="number" min={1} max={20}
              value={ideas}
              onChange={e=>setIdeas(Math.max(1, Math.min(20, Number(e.target.value))))}
            />
          </div>
          <div>
            <label>Filter & sort</label>
            <div style={{display:"grid",gridTemplateColumns:"1fr 140px",gap:8}}>
              <input className="input" placeholder="Filter by keyword…" value={q} onChange={e=>setQ(e.target.value)} />
              <select className="select" value={sortBy} onChange={e=>setSortBy(e.target.value as any)}>
                <option value="feas">Sort: Feasibility</option>
                <option value="size">Sort: Size</option>
                <option value="growth">Sort: Growth</option>
              </select>
            </div>
          </div>
          <button className="btn" disabled={loading} onClick={discover}>
            {loading ? <span className="spinner" /> : null}
            {loading ? "Discovering…" : "Discover ventures"}
          </button>
          <button className="btn btn-secondary" disabled={!ventures.length || loading} onClick={()=>{ setVentures([]); setTs(""); }}>
            Clear
          </button>
        </div>

        <div className="meta">
          {err ? (<><span className="dot danger" /> <span className="status danger">Error: {err}</span></>) : null}
          {!err && loading ? (<><span className="dot warn" /> <span>Running multi-agent pipeline…</span></>) : null}
          {!err && !loading && ventures.length ? (<><span className="dot ok" /> <span>Ready • {filteredSorted.length} ventures</span></>) : null}
          {timestamp ? <span style={{opacity:.7}}>Timestamp: {timestamp}</span> : null}
        </div>
      </div>

      {/* Results */}
      <div className="grid" style={{opacity: loading ? .6 : 1}}>
        {loading && !ventures.length ? Array.from({length:6}).map((_,i)=>(<div className="skeleton skel-card" key={i}/>)) : null}

        {filteredSorted.map(v => (
          <article className="card" key={v.id}>
            <header>
              <h3>{v.idea}</h3>
              <div className="kpis">
                <span className="pill"><strong>Feasibility</strong>{Number(v.feasibility_score).toFixed(1)}</span>
                <span className="pill"><strong>Size</strong>{v.score_breakdown.market_size}</span>
                <span className="pill"><strong>Growth</strong>{v.score_breakdown.market_growth}</span>
                <span className="pill"><strong>Fit</strong>{v.score_breakdown.strategic_fit}</span>
              </div>
              <div className="score">
                <div className="scorebar" style={{["--w" as any]: `${(v.score_breakdown.market_size/10)*100}%`}}><span/></div>
                <div className="scorebar" style={{["--w" as any]: `${(v.score_breakdown.market_growth/10)*100}%`}}><span/></div>
                <div className="scorebar" style={{["--w" as any]: `${(v.score_breakdown.strategic_fit/10)*100}%`}}><span/></div>
              </div>
            </header>

            <p className="subtle">{v.summary}</p>

            {v.insights?.features?.length ? (
              <div className="rowline">
                {v.insights.features.slice(0,6).map((f, i)=>(
                  <span className="tag" key={i}>{f}</span>
                ))}
              </div>
            ) : null}

            <div className="actions">
              {v.URL ? <a className="link" href={v.URL} target="_blank" rel="noreferrer">Open link</a> : null}
              <button className="btn btn-secondary" onClick={()=>setOpen(v)}>Show details</button>
            </div>
          </article>
        ))}
      </div>

      <div className="footer">© {new Date().getFullYear()} — Built with CrewAI + FastAPI + Vite/React</div>

      {/* Modal */}
      {open && (
        <div className="modal" onClick={()=>setOpen(null)}>
          <div className="modal-card" onClick={e=>e.stopPropagation()}>
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",gap:12}}>
              <h3 style={{margin:0}}>{open.idea}</h3>
              <button className="btn btn-secondary" onClick={()=>setOpen(null)}>Close</button>
            </div>
            <div className="modal-grid">
              <section>
                <h4>Value proposition</h4>
                <p className="subtle">{open.insights?.value_proposition}</p>
                <h4>Go-to-market</h4>
                <p className="subtle">{open.insights?.go_to_market}</p>
                <h4>Positioning</h4>
                <p className="subtle">{open.insights?.positioning}</p>
                <h4>Differentiation</h4>
                <p className="subtle">{open.insights?.differentiation}</p>
              </section>
              <section>
                <h4>Features</h4>
                <div className="rowline">
                  {open.insights?.features?.map((f,i)=>(<span className="tag" key={i}>{f}</span>))}
                </div>
                <div className="divider"></div>
                <h4>Justification</h4>
                <p className="subtle">{open.insights?.justification}</p>
                <div className="divider"></div>
                <h4>White-space analysis</h4>
                <p className="subtle"><strong>Market gap:</strong> {open.white_space_analysis?.market_gap}</p>
                <p className="subtle"><strong>Company fit:</strong> {open.white_space_analysis?.company_fit}</p>
                {open.citations?.length ? (
                  <>
                    <div className="divider"></div>
                    <h4>Citations</h4>
                    <ul className="subtle" style={{paddingLeft:18, marginTop:6}}>
                      {open.citations.map((c,i)=>(
                        <li key={i}><a className="link" href={c} target="_blank" rel="noreferrer">{c}</a></li>
                      ))}
                    </ul>
                  </>
                ) : null}
              </section>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
