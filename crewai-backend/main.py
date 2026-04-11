# main.py (only this function)
from typing import List
from agents import llm_json
from prompts import QUERY_EXPANSION  # whatever you currently import

def expand_queries(focus_area: str) -> List[str]:
    prompt = QUERY_EXPANSION.format(focus_area=focus_area)
    try:
        raw = llm_json(prompt)
        if isinstance(raw, dict) and isinstance(raw.get("queries"), list):
            qs = [q for q in raw["queries"] if isinstance(q, str)]
            if qs:
                return qs[:7]
    except Exception as e:
        print(f"[expand_queries] LLM failed, using heuristic fallback: {e}")

    # Heuristic, zero-LLM fallback so the pipeline keeps working
    return [
        f"{focus_area} trends 2024",
        f"{focus_area} top companies",
        f"{focus_area} market size and CAGR",
        f"{focus_area} government incentives",
        f"{focus_area} charging infrastructure",
        f"{focus_area} consumer behavior",
        f"{focus_area} forecasts 2025",
    ]
