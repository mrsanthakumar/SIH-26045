import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .schemas import ClassificationRequest, AssessmentRequest, ChatRequest, IngestRequest
from .classifier import classify
from .assessment import assess
from .models import Source, SessionLocal
from .knowledge import seed_sources
from .rag import retrieve
from .web_search import search_web
from .llm import synthesize

app = FastAPI(title="AyurIPR API", version="1.2.0")

# Local-development CORS: support both common Vite addresses.
# ALLOWED_ORIGINS can add more comma-separated origins.
def _cors_origins():
    defaults = {
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    }
    configured = os.getenv("ALLOWED_ORIGINS", "")
    defaults.update(x.strip().rstrip("/") for x in configured.split(",") if x.strip())
    return sorted(defaults)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    seed_sources()

@app.get("/api/health")
def health():
    return {"status":"ok","service":"AyurIPR API","live_web_search":True}

@app.get("/api/sources")
def sources(jurisdiction: str = "India"):
    db = SessionLocal()
    try:
        rows = db.query(Source).filter(Source.jurisdiction == jurisdiction).all()
        return [{"id":x.id,"title":x.title,"authority":x.authority,"section":x.section,"url":x.url,
                 "version":x.version,"verified":x.verified} for x in rows]
    finally:
        db.close()

@app.post("/api/classify")
def classify_product(req: ClassificationRequest):
    return classify(req)

@app.post("/api/assess")
def assessment(req: AssessmentRequest):
    return assess(req)

@app.post("/api/web-search")
def web_search(req: ChatRequest):
    results = search_web(req.question, req.jurisdiction, limit=8)
    return {"query": req.question, "jurisdiction": req.jurisdiction, "checked_at": datetime.now(timezone.utc).isoformat(),
            "results": results, "internet_checked": True}

@app.post("/api/chat")
def chat(req: ChatRequest):
    local = retrieve(req.question, req.jurisdiction)
    live = search_web(req.question, req.jurisdiction, limit=8)
    local_dicts = [{"title":s.title,"authority":s.authority,"section":s.section,"url":s.url,"version":s.version} for s in local]

    llm_answer = synthesize(req.question, req.jurisdiction, local, live)
    if llm_answer:
        answer = llm_answer
        confidence = 0.88 if any(x["official"] for x in live) else 0.70
    elif live:
        official = [x for x in live if x["official"]]
        answer = (
            f"I checked the live public web for this question under the {req.jurisdiction} framework. "
            f"I found {len(live)} live result(s), including {len(official)} prioritized official source(s). "
            "The evidence below is the basis for a preliminary answer. Read the linked source before taking action.\n\n"
            + "\n\n".join(
                f"• {x['title']} ({x['domain']}): {x['snippet'] or 'Open the source for the relevant provision or guidance.'}"
                for x in live[:5]
            )
        )
        confidence = 0.78 if official else 0.55
    elif local:
        answer = (
            f"Live web search was unavailable, so this answer uses the indexed {req.jurisdiction} corpus only. "
            "The result is preliminary and must be checked against the current official source.\n\n" +
            "\n\n".join(f"• {s.title}: {s.text}" for s in local[:5])
        )
        confidence = 0.52
    else:
        answer = "I could not find sufficient evidence in the live web search or the indexed corpus. Please refine the question or request human review."
        confidence = 0.20

    combined = []
    for x in live:
        combined.append({"title":x["title"],"authority":x["domain"],"section":"Live web result",
                         "url":x["url"],"version":"Checked now", "snippet":x["snippet"], "official":x["official"]})
    for x in local_dicts:
        if not any(y["url"] == x["url"] for y in combined):
            combined.append({**x, "snippet":"Indexed authoritative source", "official":True})

    return {
        "answer": answer,
        "confidence": confidence,
        "sources": combined[:12],
        "internet_checked": True,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "search_results": len(live),
        "official_results": sum(1 for x in live if x["official"]),
        "human_review": confidence < 0.75 or req.jurisdiction == "International",
        "disclaimer": "Information only — not legal advice. Verify the current law, regulations, registry records and professional advice before acting."
    }

@app.post("/api/admin/ingest")
def ingest(req: IngestRequest):
    db = SessionLocal()
    try:
        row = Source(**req.model_dump())
        db.add(row); db.commit(); db.refresh(row)
        return {"id":row.id,"status":"ingested"}
    finally:
        db.close()
