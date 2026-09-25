# Run from the AyurIPR project root in PowerShell.
Start-Process powershell -ArgumentList '-NoExit','-Command','cd backend; if (!(Test-Path .venv)) { python -m venv .venv }; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt; uvicorn app.main:app --reload --port 8000'
Start-Process powershell -ArgumentList '-NoExit','-Command','cd frontend; npm install; npm run dev'
Write-Host 'AyurIPR starting... Backend: http://localhost:8000/docs  Frontend: http://localhost:5173'
