"""Lightweight live-web retrieval for AyurIPR.

The app searches the public web at question time. Official government/treaty
sources are ranked first. If the search provider is unavailable, the local
indexed corpus is still used by the caller.
"""
import re
from urllib.parse import quote, urlparse
import httpx
from bs4 import BeautifulSoup

OFFICIAL_DOMAINS = {
    "India": [
        "ipindia.gov.in", "tkdl.res.in", "ayush.gov.in", "fssai.gov.in",
        "nbaindia.org", "absefiling.nic.in", "indiacode.nic.in", "egazette.nic.in"
    ],
    "International": [
        "wipo.int", "who.int", "wto.org", "cbd.int", "nagoya-protocol.org",
        "epo.org", "uspto.gov", "europa.eu"
    ],
}


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def _domain(url: str) -> str:
    return urlparse(url).netloc.lower().replace("www.", "")


def _official(url: str, jurisdiction: str) -> bool:
    d = _domain(url)
    return any(d == x or d.endswith("." + x) for x in OFFICIAL_DOMAINS.get(jurisdiction, []))


def search_web(query: str, jurisdiction: str = "India", limit: int = 8):
    """Search live web using DuckDuckGo Lite. Returns safe, display-ready results."""
    if not query.strip():
        return []

    # Two passes: official-domain-focused, then broader web coverage.
    domains = OFFICIAL_DOMAINS.get(jurisdiction, [])
    queries = []
    if domains:
        site_filter = " OR ".join(f"site:{d}" for d in domains[:5])
        queries.append(f"{query} ({site_filter})")
    queries.append(query)

    results = []
    seen = set()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/153 Safari/537.36"}

    for q in queries:
        try:
            url = "https://lite.duckduckgo.com/lite/?q=" + quote(q)
            r = httpx.get(url, headers=headers, timeout=12, follow_redirects=True)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.select("a.result-link"):
                href = a.get("href")
                title = _clean(a.get_text(" ", strip=True))
                if not href or not title or not href.startswith(("http://", "https://")):
                    continue
                d = _domain(href)
                if d in seen:
                    continue
                # Locate the nearest result container/snippet.
                container = a.parent
                for _ in range(3):
                    if container is not None and container.get_text(" ", strip=True):
                        break
                    container = container.parent if container else None
                snippet = ""
                if container:
                    text = _clean(container.get_text(" ", strip=True))
                    snippet = text.replace(title, "", 1).strip()
                seen.add(d)
                results.append({
                    "title": title[:240],
                    "url": href,
                    "domain": d,
                    "snippet": snippet[:900],
                    "official": _official(href, jurisdiction),
                    "source": "live_web",
                })
                if len(results) >= limit * 2:
                    break
        except Exception:
            continue
        if len(results) >= limit:
            break

    # Official sources first, then other sources.
    results.sort(key=lambda x: (not x["official"], x["domain"], x["title"]))
    return results[:limit]
