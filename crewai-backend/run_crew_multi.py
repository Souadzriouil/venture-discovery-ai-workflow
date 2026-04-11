import os, re, sys, json
from dotenv import load_dotenv

# ensure project root on sys.path (safeguard when running from subfolders)
ROOT = os.path.abspath(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from crew.crew_multistep import run_with_multi_crew

def _bool_mask(v: str) -> str:
    if not v: return "❌"
    return f"✅ ({v[:3]}...{v[-3:]})"

def _slug(s: str):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

if __name__ == "__main__":
    load_dotenv()
    print("MISTRAL_API_KEY:", _bool_mask(os.getenv("MISTRAL_API_KEY")))
    print("SERPAPI_API_KEY:", _bool_mask(os.getenv("SERPAPI_API_KEY")))

    focus = sys.argv[1] if len(sys.argv) > 1 else "Electric vehicle market in Europe"
    company = sys.argv[2] if len(sys.argv) > 2 else "ACME Europe"
    num_ideas = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    result = run_with_multi_crew(focus_area=focus, company=company, num_ideas=num_ideas)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    os.makedirs("outputs", exist_ok=True)
    ts = result.get("timestamp", "now").replace(":", "").replace("Z", "")
    out_path = f"outputs/{_slug(focus)}-{ts}-crew-multi.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Saved: {out_path}")
