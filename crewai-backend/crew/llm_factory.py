# crew/llm_factory.py
import os
from crewai import LLM

def get_llm():
  return LLM(
    model=os.getenv("LLM_MODEL_PRIMARY", "mistral/mistral-small-latest"),
    temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
    fallback_models=[
      m.strip() for m in os.getenv("LLM_MODEL_FALLBACKS", "").split(",") if m.strip()
    ],
    max_retries=int(os.getenv("LITELLM_MAX_RETRIES", "6")),
    timeout=int(os.getenv("LITELLM_TIMEOUT", "120")),
  )
