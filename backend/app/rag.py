import os, re
from typing import List
from .models import Source, SessionLocal

STOP = {"the","a","an","is","are","can","i","we","to","of","for","in","on","my","and","with","this","that"}

def tokens(text):
    return [x for x in re.findall(r"[a-zA-Z0-9]+", text.lower()) if x not in STOP]

def retrieve(query: str, jurisdiction: str, limit: int = 6) -> List[Source]:
    db = SessionLocal()
    try:
        sources = db.query(Source).filter(Source.jurisdiction == jurisdiction).all()
        q = set(tokens(query))
        scored = []
        for s in sources:
            t = set(tokens((s.title or "") + " " + (s.section or "") + " " + (s.text or "")))
            score = len(q & t)
            if any(k in query.lower() for k in ["patent","traditional knowledge","tkdl"]) and "patent" in s.title.lower():
                score += 3
            if "abs" in query.lower() and "biodiversity" in s.title.lower():
                score += 4
            if "international" == jurisdiction.lower() and "wipo" in s.authority.lower():
                score += 2
            scored.append((score, s))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s for score, s in scored[:limit] if score > 0] or [s for _,s in scored[:limit]]
    finally:
        db.close()
