# crew/multi_tools.py
# Minimal, self-contained CrewAI tools (no imports from main.py)

import os, sys, json, time, re, random
from typing import List, Dict, Optional, Any, Type

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import requests
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
from crewai.tools import BaseTool  # correct import for CrewAI tools

# Try to use your SerpAPI helper if present; otherwise fallback silently
try:
    from tools.serpapi_search import serpapi_top5 as _serp_search  # type: ignore
except Exception:
    _serp_search = None


# ---------- small helpers ----------
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

def _get_env(name: str) -> Optional[str]:
    v = os.getenv(name)
    return v.strip() if v else None

def _clean_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for s in soup(["script", "style", "noscript"]):
        s.extract()
    text = soup.get_text("\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()

def _fetch_url(url: str, timeout: int = 25) -> str:
    try:
        r = requests.get(url, headers={"User-Agent": UA}, timeout=timeout)
        r.raise_for_status()
        return _clean_text(r.text)[:120_000]
    except Exception:
        return ""

def _unique(items: List[Dict], key: str) -> List[Dict]:
    seen, out = set(), []
    for it in items:
        v = it.get(key)
        if not v or v in seen:
            continue
        seen.add(v)
        out.append(it)
    return out

def _as_dict(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    if isinstance(obj, str):
        try:
            return json.loads(obj)
        except Exception:
            return {"value": obj}
    return {"value": obj}


# ---------- input schemas ----------
class ExpandQueriesInput(BaseModel):
    focus_area: str = Field(..., description="Market/topic focus string")

class SearchCollectInput(BaseModel):
    queries_json: str = Field(..., description='JSON like {"queries": ["q1", ...]}')

class SummarizeDocsInput(BaseModel):
    docs_json: str = Field(..., description='JSON like {"docs": [{"url":..., "title":..., "content":...}, ...]}')

class IdeateInput(BaseModel):
    summaries_json: str
    focus_area: Optional[str] = None
    company: Optional[str] = None
    seed: Optional[int] = None

class EstimateInput(BaseModel):
    ideas_json: str  # may include {"domain": "..."} from ideation

class ScoreFilterInput(BaseModel):
    estimates_json: str
    top_k: int = 10
    min_score: float = 7.0

class InsightsInput(BaseModel):
    scored_json: str
    ideas_or_mapping_json: str

class WhiteSpaceInput(BaseModel):
    finals_json: str
    company: str


# ---------- tools ----------
class ExpandQueriesTool(BaseTool):
    name: str = "expand_queries"
    description: str = "Return a robust set of queries for a focus area"
    args_schema: Type[ExpandQueriesInput] = ExpandQueriesInput

    def _run(self, focus_area: str) -> str:
        fa = focus_area.strip()
        queries = [
            f"{fa} market trends 2024",
            f"Top companies in {fa}",
            f"{fa} global market size and growth",
            f"{fa} regulations and policy landscape",
            f"{fa} leading startups and funding",
            f"customer pain points in {fa}",
            f"future projections for {fa}",
        ]
        return json.dumps({"queries": queries}, ensure_ascii=False)


class SearchCollectTool(BaseTool):
    name: str = "search_collect"
    description: str = "Search (SerpAPI if available) and fetch pages. Returns docs JSON."
    args_schema: Type[SearchCollectInput] = SearchCollectInput

    def _run(self, queries_json: str) -> str:
        qobj = _as_dict(queries_json)
        queries: List[str] = qobj.get("queries", [])[:7]
        docs: List[Dict[str, str]] = []
        serp_key = _get_env("SERPAPI_API_KEY")

        for q in queries:
            results: List[Dict] = []
            if serp_key and _serp_search:
                try:
                    results = _serp_search(q)[:5]
                except Exception:
                    results = []

            cleaned: List[Dict[str, str]] = []
            for r in results:
                url = r.get("link") or r.get("url")
                title = r.get("title") or r.get("name") or ""
                if url:
                    cleaned.append({"url": url, "title": title})

            for item in cleaned:
                url = item["url"]
                title = item.get("title") or url
                content = _fetch_url(url)
                if len(content) < 400:
                    continue
                docs.append({"url": url, "title": title, "content": content})

        docs = _unique(docs, "url")
        return json.dumps({"docs": docs}, ensure_ascii=False)


class SummarizeDocsTool(BaseTool):
    name: str = "summarize_docs"
    description: str = "Summarize docs to Title/Summary/URL. LLM-free heuristic."
    args_schema: Type[SummarizeDocsInput] = SummarizeDocsInput

    def _run(self, docs_json: str) -> str:
        dobj = _as_dict(docs_json)
        docs: List[Dict] = dobj.get("docs", [])
        sums: List[Dict[str, str]] = []
        for d in docs:
            url = d.get("url", "")
            title = (d.get("title") or "")[:120] or url
            content = (d.get("content") or "").strip()
            words = content.split()
            summary = " ".join(words[:120]) + ("..." if len(words) > 120 else "")
            sums.append({"title": title, "summary": summary, "url": url})
        return json.dumps({"summaries": sums}, ensure_ascii=False)


class IdeateVenturesTool(BaseTool):
    name: str = "ideate_ventures"
    description: str = "Heuristic ideation from focus + summaries (no static catalog)."
    args_schema: Type[IdeateInput] = IdeateInput

    def _keywords(self, focus_area: Optional[str], sums: List[Dict]) -> List[str]:
        base = (focus_area or "")
        for s in sums:
            base += " " + (s.get("title", "") + " " + s.get("summary", ""))
        base = base.lower()

        # keep alphabetic tokens 3–20 chars, drop stopwords
        stop = set("""
            the a an of and or for with on to in by from at as is are be this that these those into via than over under about
            using use new real-time real time ai data system platform solution app services service technology
        """.split())
        toks = [t for t in re.findall(r"[a-z][a-z\-]{2,20}", base) if t not in stop]
        # dedupe preserving order
        seen, out = set(), []
        for t in toks:
            if t not in seen:
                seen.add(t)
                out.append(t)
        return out[:60]  # cap

    def _titleize(self, words: List[str]) -> str:
        return " ".join(w.capitalize() for w in words)

    def _gen_name(self, rnd: random.Random, kws: List[str]) -> str:
        # building blocks
        prefixes = ["", "Smart", "Auto", "Predictive", "Insight", "Signal", "Flow",
                    "Pulse", "Grid", "Chain", "Route", "Crop", "Clinic", "Fin", "Agri", "Logi"]
        cores     = ["Copilot", "Monitor", "Optimizer", "Analytics", "Guard", "Hub",
                     "Planner", "Gateway", "Forecast", "Navigator", "Workbench", "Studio"]
        # pick 1–2 domain keywords to mix in
        dom = []
        if kws:
            dom.append(self._titleize([rnd.choice(kws)]))
            if rnd.random() < 0.5 and len(kws) > 1:
                dom.append(self._titleize([rnd.choice(kws)]))
        parts = []
        p = rnd.choice(prefixes)
        if p: parts.append(p)
        if dom: parts.append(dom[0])
        parts.append(rnd.choice(cores))
        return "".join(parts) if rnd.random() < 0.5 else " ".join(parts)

    def _gen_summary(self, name: str, focus_area: Optional[str], company: Optional[str]) -> str:
        fa = (focus_area or "the target domain")
        tail = f" Designed to leverage {company}'s assets." if company else ""
        return (f"{name} provides AI-assisted workflows for {fa}, combining retrieval, prediction, and decision support "
                f"to reduce costs and improve outcomes.{tail}")

    def _infer_domain(self, focus_area: Optional[str], kws: List[str]) -> str:
        txt = (focus_area or "").lower() + " " + " ".join(kws).lower()
        if any(k in txt for k in ["electric", "ev", "charging", "battery", "mobility"]): return "ev"
        if any(k in txt for k in ["health", "patient", "telemedicine", "medical", "care"]): return "health"
        if any(k in txt for k in ["fintech", "bank", "payment", "blockchain", "defi", "crypto"]): return "fintech"
        if any(k in txt for k in ["agri", "farm", "crop", "soil", "precision", "agriculture"]): return "agri"
        if any(k in txt for k in ["logistics", "supply", "warehouse", "fleet", "routing"]): return "logistics"
        return "generic"

    def _run(self, summaries_json: str, focus_area: Optional[str] = None,
             company: Optional[str] = None, seed: Optional[int] = None) -> str:
        sobj = _as_dict(summaries_json)
        sums: List[Dict] = sobj.get("summaries", [])
        rnd = random.Random(seed) if seed is not None else random

        kws = self._keywords(focus_area, sums)
        multi = [k for k in kws if "-" in k or len(k) > 8]
        chosen = (multi[:4] + kws[:16])[:16]
        if not chosen and focus_area:
            chosen = focus_area.lower().split()

        domain = self._infer_domain(focus_area, chosen)

        ideas, mapping = [], {}
        N = 10  # generate 10 ideas
        for i in range(1, N + 1):
            name = self._gen_name(rnd, chosen or ["market"])
            src_url = sums[(i - 1) % len(sums)].get("url") if sums else ""
            ideas.append({
                "id": i,
                "idea": name,
                "summary": self._gen_summary(name, focus_area, company),
                "URL": src_url or f"https://{name.lower().replace(' ', '').replace('-', '')}.com"
            })
            mapping[name] = [src_url] if src_url else []

        return json.dumps({"ideas": ideas, "idea_source": mapping, "domain": domain}, ensure_ascii=False)


class EstimateMarketsTool(BaseTool):
    name: str = "estimate_markets"
    description: str = "Add rough TAM/CAGR/fit estimates to ideas."
    args_schema: Type[EstimateInput] = EstimateInput

    def _run(self, ideas_json: str) -> str:
        iobj = _as_dict(ideas_json)
        ideas: List[Dict] = iobj.get("ideas", [])
        domain_hint = (iobj.get("domain") or "").lower()

        def domain_from_name(nm: str) -> str:
            s = (nm or "").lower()
            if any(k in s for k in ["charge", "ev", "grid", "battery"]): return "ev"
            if any(k in s for k in ["care", "clinic", "tele", "readmission", "patient"]): return "health"
            if any(k in s for k in ["pay", "aml", "treasury", "credit", "wealth", "chain"]): return "fintech"
            if any(k in s for k in ["crop", "irrigat", "pest", "soil", "carbon"]): return "agri"
            if any(k in s for k in ["route", "dock", "coldchain", "warehouse", "fleet", "logi"]): return "logistics"
            return domain_hint or "generic"

        est: List[Dict] = []
        for it in ideas:
            nm = (it.get("idea") or "")
            dom = domain_from_name(nm)

            # crude domain priors (tweak for thesis)
            priors = {
                "ev":        (50e9, 0.18, 8.0),
                "health":    (80e9, 0.16, 8.0),
                "fintech":   (60e9, 0.14, 7.5),
                "agri":      (30e9, 0.12, 7.5),
                "logistics": (40e9, 0.13, 7.8),
                "generic":   (10e9, 0.10, 7.0),
            }
            tam, cagr, fit = priors.get(dom, priors["generic"])

            est.append({
                "idea": it.get("idea"),
                "URL": it.get("URL"),
                "TAM": float(tam),
                "SAM": float(tam * 0.3),
                "SOM": float(tam * 0.05),
                "CAGR": float(cagr * 100),
                "strategic_fit": float(fit),
            })
        return json.dumps({"estimates": est}, ensure_ascii=False)


class ScoreAndFilterTool(BaseTool):
    name: str = "score_and_filter"
    description: str = "Compute score (size/growth/fit) and keep top_k, backfilling if needed."
    args_schema: Type[ScoreFilterInput] = ScoreFilterInput

    def _run(self, estimates_json: str, top_k: int = 10, min_score: float = 7.0) -> str:
        eobj = _as_dict(estimates_json)
        items: List[Dict] = eobj.get("estimates", [])
        raw_scored: List[Dict] = []

        for it in items:
            size = 9.0 if it["TAM"] >= 50_000_000_000 else 7.0
            growth = 8.0 if it["CAGR"] >= 15 else 6.0
            fit = float(it.get("strategic_fit", 8.0))
            score = round((size + growth + fit) / 3, 1)
            raw_scored.append({
                "idea": it["idea"],
                "URL": it["URL"],
                "score_breakdown": {
                    "market_size": size,
                    "market_growth": growth,
                    "strategic_fit": fit
                },
                "feasibility_score": round(score + 0.3, 1)
            })

        # sort by feasibility desc
        raw_scored.sort(key=lambda x: x["feasibility_score"], reverse=True)

        # keep those >= min_score
        keep = [s for s in raw_scored if (s["feasibility_score"] >= min_score)]

        # backfill if needed to reach top_k
        if len(keep) < max(1, int(top_k)):
            for s in raw_scored:
                if s not in keep:
                    keep.append(s)
                    if len(keep) >= top_k:
                        break

        return json.dumps({"scored": keep[: max(1, int(top_k))]}, ensure_ascii=False)


class GenerateInsightsTool(BaseTool):
    name: str = "generate_insights"
    description: str = "Add GTM/value/differentiation to scored ideas."
    args_schema: Type[InsightsInput] = InsightsInput

    def _run(self, scored_json: str, ideas_or_mapping_json: str) -> str:
        sobj = _as_dict(scored_json)
        scored: List[Dict] = sobj.get("scored", [])
        finals: List[Dict] = []

        for idx, s in enumerate(scored, start=1):
            idea = s["idea"]
            finals.append({
                "id": idx,
                "idea": idea,
                "summary": f"{idea} — concise product concept tailored to the domain.",
                "URL": s.get("URL") or f"https://{idea.lower().replace(' ', '')}.com",
                "score_breakdown": s["score_breakdown"],
                "feasibility_score": s["feasibility_score"],
                "insights": {
                    "go_to_market": "Pilot with early adopters; partnerships with domain incumbents; content + events.",
                    "justification": "Demand signals + gaps in current solutions indicate opportunity.",
                    "value_proposition": "Lower costs, faster decisions, better outcomes via AI-assisted workflows.",
                    "features": [
                        "Data ingestion/connectors", "Analytics & dashboards", "Alerting/automation",
                        "APIs & integrations", "Governance & audit"
                    ],
                    "positioning": f"The go-to {idea} solution for the target market.",
                    "differentiation": "Domain-focused workflows + clean UX + faster time-to-value."
                }
            })
        return json.dumps({"finals": finals}, ensure_ascii=False)


class WhiteSpaceTool(BaseTool):
    name: str = "white_space"
    description: str = "Add white-space analysis and company fit; final packaging."
    args_schema: Type[WhiteSpaceInput] = WhiteSpaceInput

    def _run(self, finals_json: str, company: str) -> str:
        fobj = _as_dict(finals_json)
        finals: List[Dict] = fobj.get("finals", [])
        ventures: List[Dict] = []

        for v in finals:
            ventures.append({
                **v,
                "white_space_analysis": {
                    "market_gap": "Generalized tools dominate; domain-specific, real-time, integrated solutions are scarce.",
                    "company_fit": f"Alignment with {company}'s strategy and assets; leverage data, distribution, and partnerships."
                }
            })
        return json.dumps({
            "ventures": ventures,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        }, ensure_ascii=False)
