from schemas import ScoreBreakdown, ScoredVenture

def _score_tam(tam: float) -> float:
    if tam < 1_000_000_000: return 0
    if tam < 3_000_000_000: return 2
    if tam < 10_000_000_000: return 5
    if tam < 50_000_000_000: return 7
    return 9

def _score_cagr(cagr: float) -> float:
    if cagr < 5: return 1
    if cagr < 10: return 3
    if cagr < 20: return 6
    if cagr < 35: return 8
    return 10

def score_and_wrap(est: dict) -> ScoredVenture:
    ms = _score_tam(float(est["TAM"]))
    mg = _score_cagr(float(est["CAGR"]))
    sf = max(0.0, min(float(est["strategic_fit"]), 10.0))
    feasibility = round(0.4*ms + 0.4*mg + 0.3*sf, 2)
    return ScoredVenture(
        id=int(est["id"]),
        idea=est["idea"],
        summary=est["summary"],
        URL=est["URL"],
        score_breakdown=ScoreBreakdown(
            market_size=ms, market_growth=mg, strategic_fit=sf
        ),
        feasibility_score=feasibility
    )
