import requests
from bs4 import BeautifulSoup

def fetch_clean(url: str) -> dict:
    try:
        r = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = (soup.title.string or "").strip() if soup.title else "Untitled"
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        text = " ".join(soup.get_text(" ").split())
        return {"url": url, "title": title, "content": text, "contentLength": len(text)}
    except Exception as e:
        return {"url": url, "title": "Error", "content": "", "error": str(e), "contentLength": 0}
