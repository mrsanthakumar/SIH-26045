import json
from .classifier import classify
from .rag import retrieve
from .models import Assessment, SessionLocal

DISCLAIMER = "Information only — not legal advice. Verify the current law, regulations, registry records and professional advice before acting."

def assess(data):
    classification = classify(data)
    q = data.question
    jurisdiction = data.market if data.market in ("India","International") else "India"
    sources = retrieve(q + " " + classification["category"], jurisdiction)
    findings = []
    lower = q.lower()

    if "patent" in lower or "ip" in lower:
        findings.append("Patentability should be assessed separately for novelty, inventive step, statutory exclusions and applicable biodiversity/traditional-knowledge issues.")
    if any(k in lower for k in ["traditional knowledge","tkdl","traditional"]):
        findings.append("Traditional-knowledge overlap should be checked before relying on patent protection; do not assume that a known traditional use is a new invention.")
    if any(k in lower for k in ["abs","biodiversity","biological resource","plant"]):
        findings.append("A preliminary ABS review may be necessary where Indian biological resources or associated traditional knowledge are involved.")
    if not findings:
        findings.append("The question needs to be mapped to the relevant IP and regulatory regimes after product classification.")

    if jurisdiction == "India" and classification["category"].startswith("Classical"):
        findings.append("For a classical formulation, investigate the traditional-knowledge exclusion and prior-art position before making a patent claim.")
    if classification["category"].startswith("Uncertain"):
        confidence = 0.45
    else:
        confidence = min(0.95, 0.65 + len(sources)*0.05)

    result = {
        "jurisdiction": jurisdiction,
        "classification": classification,
        "findings": findings,
        "sources": [
            {"title": s.title, "authority": s.authority, "section": s.section, "url": s.url, "version": s.version}
            for s in sources
        ],
        "confidence": confidence,
        "disclaimer": DISCLAIMER,
        "human_review": confidence < 0.75 or jurisdiction == "International"
    }
    db = SessionLocal()
    try:
        db.add(Assessment(question=q, jurisdiction=jurisdiction, product_category=classification["category"],
                          confidence=confidence, result_json=json.dumps(result)))
        db.commit()
    finally:
        db.close()
    return result
