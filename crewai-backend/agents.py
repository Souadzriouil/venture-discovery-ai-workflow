# agents.py
import os, re, json, time, random
from typing import Any, List
from httpx import HTTPStatusError
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI

# load .env once for the whole app
load_dotenv()

PRIMARY_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")
FALLBACK_MODELS: List[str] = [
    "mistral-small-latest",
    "open-mixtral-8x7b",
]

def _make_llm(model: str) -> ChatMistralAI:
    return ChatMistralAI(
        api_key=os.environ.get("MISTRAL_API_KEY"),
        model=model,
        temperature=0.2,
        max_retries=0,  # we handle retries ourselves
    )

_LLM = _make_llm(PRIMARY_MODEL)

def _safe_json(text: str) -> Any:
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"(\{.*\}|\[.*\])", text, re.S)
        if m:
            return json.loads(m.group(1))
        raise RuntimeError("LLM did not return valid JSON")

def llm_json(prompt: str) -> Any:
    # try primary with exponential backoff
    for attempt in range(4):
        try:
            msg = _LLM.invoke(prompt)
            return _safe_json(msg.content)
        except HTTPStatusError as e:
            if getattr(e, "response", None) and e.response.status_code == 429:
                time.sleep(1.5 * (2 ** attempt) + random.random())
                continue
            raise
        except Exception:
            time.sleep(1.0 * (attempt + 1))
            continue

    # fallbacks
    for m in [m for m in FALLBACK_MODELS if m != PRIMARY_MODEL]:
        try:
            alt = _make_llm(m)
            msg = alt.invoke(prompt)
            return _safe_json(msg.content)
        except Exception:
            continue

    raise RuntimeError(
        "All LLM calls failed (capacity/rate limit). "
        "Try MISTRAL_MODEL=mistral-small-latest or check your key."
    )

def get_llm() -> ChatMistralAI:
    return _LLM
