# api.py
import os, json
from typing import Optional, Dict, Any
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime, timezone

# --- keep your old runner for GET ---
from crew.crew_multistep import run_with_multi_crew

# --- direct tools for POST (timings) ---
from crew.multi_tools import (
    ExpandQueriesTool, SearchCollectTool, SummarizeDocsTool,
    IdeateVenturesTool, EstimateMarketsTool,
    ScoreAndFilterTool, GenerateInsightsTool, WhiteSpaceTool
)

# -------- token estimator (uses tiktoken if available; else fallback) --------
def _build_tokenizer():
    try:
        import tiktoken  # type: ignore
        enc = tiktoken.get_encoding("cl100k_base")  # works for GPT-4/3.5-ish
        def _tok_count(text: Optional[str]) -> int:
            if not text:
                return 0
            try:
                return len(enc.encode(text))
            except Exception:
                # very rare encoding edge case
                return max(0, len(text) // 4)
        return _tok_count
    except Exception:
        # heuristic: ~4 chars per token on average
        def _tok_count(text: Optional[str]) -> int:
            if not text:
                return 0
            return max(0, (len(text) + 3) // 4)
        return _tok_count

TOK_COUNT = _build_tokenizer()

# ------------------------------
# App + CORS
# ------------------------------
app = FastAPI(title="Venture Discovery API", version="1.3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------
# Defaults & helpers
# ------------------------------
DEFAULT_FOCUS = "Electric vehicle market in Europe"
DEFAULT_COMPANY = (
    "ACME Corp, leveraging its global logistics network, battery R&D department, and "
    "retail energy brand, pursues a strategy of expanding into sustainable energy solutions."
)
DEFAULT_NUM_IDEAS = 10

def _clean_str(val: Optional[str], default: str) -> str:
    if val is None:
        return default
    s = str(val).strip()
    if s == "" or s.lower() in {"undefined", "null", "none"}:
        return default
    return s

def _clean_int(val: Optional[str | int], default: int) -> int:
    if val is None:
        return default
    if isinstance(val, str):
        s = val.strip().lower()
        if s in {"", "undefined", "null", "none"}:
            return default
        try:
            n = int(s)
        except ValueError:
            return default
    else:
        n = int(val)
    return max(1, min(50, n))

class DiscoverResponse(BaseModel):
    ventures: list
    timestamp: str

# ------------------------------
# Health
# ------------------------------
@app.get("/api/health")
def health():
    return {"ok": True}

# ------------------------------
# Backward-compatible GET (uses your old runner)
# ------------------------------
@app.get("/api/discover", response_model=DiscoverResponse)
def discover_get(
    focus: Optional[str] = Query(None, description="Focus area, e.g. 'Electric vehicle market in Europe'"),
    company: Optional[str] = Query(None, description="Company name for fit analysis"),
    num_ideas: Optional[str] = Query(None, description="How many ideas (1-50)"),
):
    focus_clean = _clean_str(focus, DEFAULT_FOCUS)
    company_clean = _clean_str(company, DEFAULT_COMPANY)
    num_ideas_clean = _clean_int(num_ideas, DEFAULT_NUM_IDEAS)

    print("Using Tool chain (GET): expand_queries -> search_collect -> summarize_docs -> "
          "ideate_ventures -> estimate_markets -> score_and_filter -> generate_insights -> white_space")

    result = run_with_multi_crew(
        focus_area=focus_clean,
        company=company_clean,
        num_ideas=num_ideas_clean
    )
    return result  # must be {"ventures":[...], "timestamp":"..."}

# ------------------------------
# New POST with per-step timings + token counts
# ------------------------------
class DiscoverRequest(BaseModel):
    focus_area: str
    company: Optional[Dict[str, Any]] = None   # {"name","strategy","assets"}
    num_ideas: int = DEFAULT_NUM_IDEAS
    seed: Optional[int] = None
    request_id: Optional[str] = None
    eval_mode: Optional[bool] = None
    fast: Optional[bool] = None                 # if True, skip network fetch

@app.post("/api/discover")
def discover_post(req: DiscoverRequest):
    """
    Returns:
      {
        "ventures": [...],
        "timestamp": "...",
        "run_steps": [{"name","started_at","ended_at","tokens_in","tokens_out"}, ...],
        "usage": {"prompt_tokens": int, "completion_tokens": int, "total_tokens": int}
      }
    """
    num_ideas = max(1, min(50, int(req.num_ideas)))
    company_name = (req.company or {}).get("name") or ""

    run_steps = []
    usage_prompt = 0
    usage_completion = 0

    def _json_argblob(kwargs: Dict[str, Any]) -> str:
        # stringify inputs for token accounting; keep it bounded
        try:
            s = json.dumps(kwargs, ensure_ascii=False)
        except Exception:
            s = str(kwargs)
        # cap ultra-long blobs to avoid skew (optional)
        return s if len(s) <= 500_000 else s[:500_000]

    def step(name: str, tool, kwargs: Dict[str, Any]) -> str:
        nonlocal usage_prompt, usage_completion
        start = datetime.now(timezone.utc)

        # estimate tokens for inputs (prompt-like)
        in_blob = _json_argblob(kwargs)
        tokens_in = TOK_COUNT(in_blob)

        out = tool.run(**kwargs)

        end = datetime.now(timezone.utc)

        # estimate tokens for outputs (completion-like)
        tokens_out = TOK_COUNT(out)

        usage_prompt += tokens_in
        usage_completion += tokens_out

        run_steps.append({
            "name": name,
            "started_at": start.isoformat(),
            "ended_at": end.isoformat(),
            "tokens_in": tokens_in,
            "tokens_out": tokens_out
        })
        return out

    # 1) expand queries
    qjson = step("expand_queries", ExpandQueriesTool(), {"focus_area": req.focus_area})

    # 2) (optional) search & collect, else synth doc for speed
    if req.fast:
        docs_json = json.dumps({
            "docs": [{"url": "", "title": req.focus_area, "content": req.focus_area}]
        }, ensure_ascii=False)
        sjson = step("summarize_docs", SummarizeDocsTool(), {"docs_json": docs_json})
    else:
        djson = step("search_collect", SearchCollectTool(), {"queries_json": qjson})
        sjson = step("summarize_docs", SummarizeDocsTool(), {"docs_json": djson})

    # 3) ideate
    ij = step("ideate_ventures", IdeateVenturesTool(), {
        "summaries_json": sjson,
        "focus_area": req.focus_area,
        "company": company_name,
        "seed": req.seed
    })

    # 4) estimate
    ej = step("estimate_markets", EstimateMarketsTool(), {"ideas_json": ij})

    # 5) score & filter (guarantee exactly top_k via backfill logic in tool)
    sfj = step("score_and_filter", ScoreAndFilterTool(), {
        "estimates_json": ej,
        "top_k": num_ideas,
        "min_score": 7.0
    })

    # 6) insights
    finals = step("generate_insights", GenerateInsightsTool(), {
        "scored_json": sfj,
        "ideas_or_mapping_json": ij
    })

    # 7) white-space
    result = step("white_space", WhiteSpaceTool(), {
        "finals_json": finals,
        "company": company_name
    })

    out = json.loads(result)  # {"ventures":[...], "timestamp":"..."}

    total_tokens = usage_prompt + usage_completion
    out["run_steps"] = run_steps
    out["usage"] = {
        "prompt_tokens": usage_prompt,
        "completion_tokens": usage_completion,
        "total_tokens": total_tokens
    }
    return out

# ------------------------------
# Static Frontend
# ------------------------------
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
