import type { ScoreBreakdown } from "../types";

export default function ScoreBadge({ s }: { s: ScoreBreakdown }) {
  const avg = ((s.market_size + s.market_growth + s.strategic_fit) / 3).toFixed(1);
  return (
    <div className="flex gap-2 items-center">
      <span className="pill">size {s.market_size.toFixed(1)}</span>
      <span className="pill">growth {s.market_growth.toFixed(1)}</span>
      <span className="pill">fit {s.strategic_fit.toFixed(1)}</span>
      <span className="pill bg-cyan-500/10 border-cyan-400/30">score {avg}</span>
    </div>
  );
}
