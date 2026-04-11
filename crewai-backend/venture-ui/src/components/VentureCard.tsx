import { useState } from "react";
import type { Venture } from "../types";

function fmt(n?: number) {
  return typeof n === "number" ? Number(n).toFixed(1) : "–";
}

export default function VentureCard({ v }: { v: Venture }) {
  const [open, setOpen] = useState(false);

  return (
    <div className="card">
      <h3>{v.idea || "Untitled"}</h3>

      <div className="rowline">
        <span className="tag">Feasibility: {fmt(v.feasibility_score)}</span>
        <span className="tag">Size: {fmt(v.score_breakdown?.market_size)}</span>
        <span className="tag">Growth: {fmt(v.score_breakdown?.market_growth)}</span>
        <span className="tag">Fit: {fmt(v.score_breakdown?.strategic_fit)}</span>
      </div>

      {v.summary ? <p>{v.summary}</p> : <p className="muted">No summary.</p>}

      {/* quick features preview */}
      {!!(v.insights?.features?.length) && (
        <div className="rowline">
          {v.insights!.features!.slice(0, 6).map((f, i) => (
            <span className="tag" key={i}>{f}</span>
          ))}
        </div>
      )}

      <div className="rowline">
        {v.URL && (
          <a className="btn-secondary" href={v.URL} target="_blank" rel="noreferrer">
            Open link
          </a>
        )}
        <button className="btn" onClick={() => setOpen((s) => !s)}>
          {open ? "Hide details" : "Show details"}
        </button>
      </div>

      {!open ? null : (
        <div className="details">
          {v.insights?.value_proposition && (
            <>
              <h4 className="section-title">Value proposition</h4>
              <p>{v.insights.value_proposition}</p>
            </>
          )}

          {v.insights?.go_to_market && (
            <>
              <h4 className="section-title">Go-to-market</h4>
              <p>{v.insights.go_to_market}</p>
            </>
          )}

          {v.insights?.justification && (
            <>
              <h4 className="section-title">Justification</h4>
              <p>{v.insights.justification}</p>
            </>
          )}

          {v.insights?.positioning && (
            <>
              <h4 className="section-title">Positioning</h4>
              <p>{v.insights.positioning}</p>
            </>
          )}

          {v.insights?.differentiation && (
            <>
              <h4 className="section-title">Differentiation</h4>
              <p>{v.insights.differentiation}</p>
            </>
          )}

          {!!(v.insights?.features?.length) && (
            <>
              <h4 className="section-title">Features</h4>
              <ul className="bullets">
                {v.insights!.features!.map((f, i) => <li key={i}>{f}</li>)}
              </ul>
            </>
          )}

          {(v.white_space_analysis?.market_gap || v.white_space_analysis?.company_fit) && (
            <>
              <h4 className="section-title">White-space analysis</h4>
              {v.white_space_analysis?.market_gap && (
                <p><span className="kv">Market gap:</span> {v.white_space_analysis.market_gap}</p>
              )}
              {v.white_space_analysis?.company_fit && (
                <p><span className="kv">Company fit:</span> {v.white_space_analysis.company_fit}</p>
              )}
            </>
          )}

          {!!(v.citations?.length) && (
            <>
              <h4 className="section-title">Citations</h4>
              <div className="rowline">
                {v.citations!.map((u, i) => (
                  <a className="tag" key={i} href={u} target="_blank" rel="noreferrer">
                    Source {i + 1}
                  </a>
                ))}
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}
