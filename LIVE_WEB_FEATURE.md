# Live Web Question Answering

The Ask AyurIPR screen accepts free-form questions. The quick chips are only examples; they do not limit the questions that can be asked.

Every `/api/chat` request performs a live public-web search. Official domains are prioritized based on the jurisdiction, followed by broader web results. The response returns source URLs, snippets, result counts and the time checked.

## API test

PowerShell:

```powershell
$body = @{ question = "Does TKDL affect the patentability of my formulation?"; jurisdiction = "India"; language = "English" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/api/chat -Method Post -ContentType "application/json" -Body $body
```

Try any question, for example:

```powershell
$body = @{ question = "What regulations should I check before exporting an Ayurvedic herbal supplement to the EU?"; jurisdiction = "International"; language = "English" } | ConvertTo-Json
Invoke-RestMethod -Uri http://localhost:8000/api/chat -Method Post -ContentType "application/json" -Body $body
```

If the live search provider is unavailable, the backend falls back to the local indexed corpus rather than inventing an answer.

For production, use a licensed search API or official institutional connectors, add authentication/rate limits/caching, and implement stronger citation verification.
