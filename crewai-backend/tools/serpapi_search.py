import os, time, requests
from requests.exceptions import RequestException
from tools.bing_search import bing_top5

def serpapi_top5(query: str):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        print("⚠️  SERPAPI_API_KEY missing → using Bing fallback")
        return bing_top5(query)

    url = "https://serpapi.com/search"
    params = {"engine": "google", "q": query, "num": 5, "api_key": api_key}

    last_err = None
    for attempt in range(3):
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            data = r.json()
            results = []
            for item in (data.get("organic_results") or [])[:5]:
                title = item.get("title")
                link  = item.get("link") or item.get("url")
                if not (title and link): continue
                results.append({"title": title, "url": link, "snippet": item.get("snippet","")})
            if not results:
                print("⚠️  SerpAPI returned 0 results → Bing fallback")
                return bing_top5(query)
            return results
        except RequestException as e:
            last_err = e
            sleep = 1.5 * (attempt + 1)
            print(f"⚠️  SerpAPI failed (attempt {attempt+1}/3): {e} → retry {sleep:.1f}s")
            time.sleep(sleep)

    print(f"⚠️  SerpAPI unavailable → Bing fallback. Last error: {last_err}")
    return bing_top5(query)
