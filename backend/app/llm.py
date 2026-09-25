import os
from typing import List, Dict


def synthesize(question: str, jurisdiction: str, local_sources: List[Dict], web_sources: List[Dict]) -> str | None:
    """Optional grounded answer using OpenAI when OPENAI_API_KEY is configured."""
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=key)
        model = os.getenv("OPENAI_MODEL", "gpt-5.6")
        evidence = []
        for s in web_sources:
            evidence.append(f"WEB | {s.get('title')} | {s.get('url')} | {s.get('snippet')}")
        for s in local_sources:
            evidence.append(f"INDEXED | {s.title} | {s.url} | {s.text}")
        prompt = f"""You are AyurIPR, a source-grounded Ayurveda IPR/regulatory information assistant.
Jurisdiction: {jurisdiction}
Question: {question}

Use ONLY the evidence below. Do not invent laws, sections, treaty status, dates, fees, or conclusions.
If evidence is insufficient, say so clearly. Distinguish current law from guidance, registry information,
and treaty/adoption information. Give a concise preliminary answer with: Direct answer, Applicable authority,
Why it matters, What to check next, and Source references. State that the result is information, not legal advice.

EVIDENCE:
""" + "\n".join(evidence)
        resp = client.chat.completions.create(
            model=model,
            temperature=0.1,
            messages=[
                {"role": "system", "content": "Be precise, conservative, and citation-oriented. Never fabricate authority."},
                {"role": "user", "content": prompt},
            ],
        )
        return resp.choices[0].message.content.strip()
    except Exception:
        return None
