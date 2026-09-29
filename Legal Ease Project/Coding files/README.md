# LegalEase — AI-Powered Legal Document Generator

LegalEase is a Streamlit + FastAPI + Gemini application based on the supplied project specification.

## Architecture

Streamlit UI → FastAPI backend → Gemini AI → generated legal document → HTML preview / TXT / DOCX / PDF

The project keeps the specification's functional flow while using Google's current `google-genai` Python SDK. The model is configurable through `GEMINI_MODEL`.

## Features

- Select a document type
- Enter parties, terms, and effective date
- Generate a structured document with Gemini
- Preview generated HTML
- Edit generated content before export
- Download TXT, DOCX, or PDF
- FastAPI validation and health endpoint
- API error handling
- Unit tests for validation and document formatters
- CORS configuration for the Streamlit frontend

## Requirements

- Python 3.10+
- A Gemini API key
- VS Code (recommended)

## 1. Create the environment

### Windows PowerShell

```powershell
cd LegalEase
py -3.10 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 2. Configure Gemini

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and set:

```env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000
```

Do not commit `.env`.

## 3. Run the backend

Open VS Code terminal 1:

```powershell
cd LegalEase
.venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Check:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

## 4. Run Streamlit

Open VS Code terminal 2:

```powershell
cd LegalEase
.venv\Scripts\Activate.ps1
streamlit run frontend/app.py
```

Open the URL printed by Streamlit, normally:

```text
http://localhost:8501
```

## 5. Test

With the virtual environment active:

```powershell
python -m pytest -q
```

The tests do not call Gemini. They test validation and document generation locally.

## API example

```http
POST /generate
Content-Type: application/json
```

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Company A and Company B",
  "terms": "Confidential information should not be disclosed without authorization.",
  "effective_date": "2026-10-01"
}
```

Response:

```json
{
  "document_type": "Non-Disclosure Agreement",
  "content": "...",
  "html_preview": "<article>...</article>"
}
```

## Notes

The supplied documentation names Gemini 1.5 Pro. The implementation makes the model configurable because Gemini model availability changes over time. The current default in this project is `gemini-3.8-flash`; set `GEMINI_MODEL` to another model available to your API key if necessary.

LegalEase is a document drafting aid, not a substitute for review by a qualified legal professional. Generated text should be checked before signing or relying on it.
