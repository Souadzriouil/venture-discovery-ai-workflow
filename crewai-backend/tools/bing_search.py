import requests
from bs4 import BeautifulSoup

def bing_top5(query: str):
    url = "https://www.bing.com/search"
    params = {"q": query, "count": 10}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(url, params=params, headers=headers, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for li in soup.select("li.b_algo")[:5]:
        a = li.select_one("h2 a")
        if not a:
            continue
        title = a.get_text(strip=True)
        link = a.get("href")
        if not (title and link):
            continue
        snippet_tag = li.select_one(".b_caption p") or li.select_one("p")
        snippet = snippet_tag.get_text(" ", strip=True) if snippet_tag else ""
        results.append({"title": title, "url": link, "snippet": snippet})
    return results
