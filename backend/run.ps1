#!/usr/bin/env pwsh
Write-Host "Starting Code Alchemist FastAPI server..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000