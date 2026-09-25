# AyurIPR — AI-Powered IPR & Regulatory Intelligence for Ayurveda

This project is a runnable prototype for an Ayurveda-focused IPR and regulatory intelligence assistant.

## Important upgrade: live internet retrieval

The **Ask AyurIPR** module is no longer limited to the four static quick questions or the small local source list.
For **any user question**, the backend now:

1. Searches the live public web at question time.
2. Prioritizes government, treaty and institutional domains relevant to the selected jurisdiction.
3. Also performs a broader web search so unfamiliar questions can still return useful sources.
4. Combines live results with the local indexed corpus.
5. Shows the number of live results, official-priority results, source URLs and snippets in the UI.
6. Uses an optional OpenAI model to synthesize a grounded answer when `OPENAI_API_KEY` is configured.
7. Falls back to an evidence-first extractive response if no API key is configured.
8. Clearly marks the output as information, not legal advice.

### Jurisdiction-aware source priorities

**India:** IP India, TKDL, AYUSH, FSSAI, National Biodiversity Authority/ABS, India Code and related government sources.

**International:** WIPO, WTO, CBD/Nagoya resources, EPO, USPTO and selected official regulatory sources.

## What it can answer

You can type questions such as:

- Can TKDL affect the patentability of my Ayurvedic formulation?
- Is my herbal product a cosmetic or an Ayurvedic medicine?
- Do I need ABS compliance for an Indian medicinal plant?
- Can I trademark the brand name of my Ayurvedic product?
- What is the difference between Ayurveda-Aahar and an Ayurvedic drug?
- How can I protect a new extraction process internationally?
- What requirements apply to exporting an Ayurvedic product to the EU?
- What does Section 3(p) mean for traditional knowledge?

The user is **not restricted to these examples**.

## Quick start — Windows PowerShell

### Terminal 1 — Backend

```powershell
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

If `python` is not recognized:

```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Terminal 2 — Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

API documentation: `http://localhost:8000/docs`.

## Optional grounded LLM answer

Create `backend/.env` from `.env.example` and add:

```env
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-5.6
```

Without an API key, live search still works and the application returns evidence-first results.

## Notes about live search

Live search depends on the public search provider and the user's internet connection. Search-engine HTML layouts can change. For a production deployment, replace the lightweight DuckDuckGo adapter with a licensed search API or an approved institutional connector and add authentication, rate limiting, caching, source-version tracking, citation entailment checks and legal review workflows.

The application must never treat a search snippet as a substitute for the actual statute, rule, treaty or official registry record.


## Free-form Ask AyurIPR + Live Web Search

The **Ask AyurIPR** box accepts free-form Ayurveda IPR/regulatory questions. The backend performs a live public-web search at question time, prioritizes configured authoritative domains, combines those results with the indexed corpus, and returns source links and a preliminary evidence-based response.

For local Vite development, CORS supports both `http://localhost:5173` and `http://127.0.0.1:5173` (plus 5174).

### Optional AI synthesis
Set `OPENAI_API_KEY` in `backend/.env` to enable LLM-based synthesis. Without a key, the application still performs live web search and displays grounded search evidence.

### Important
Live web retrieval is not a substitute for a complete legal corpus or professional legal advice. Verify current statutes, rules, treaty status, registry records, and official guidance before acting.
