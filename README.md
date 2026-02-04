# LLM Inference Gateway

## What This Is
An LLM Inference Gateway is a backend service that exposes a simple, stable API for chat or completion requests and routes them to one or more Large Language Model providers. It centralizes authentication, model selection, and provider-specific details so downstream apps stay decoupled from vendor SDKs.

## Why This Project Exists
Most teams start by calling a provider SDK directly from application code. That approach scales poorly as requirements grow (multiple providers, model routing, cost controls, retries, observability). This project provides a clean, production-minded gateway to:
- Standardize request/response formats across apps
- Keep provider logic in one place
- Enable future routing, guardrails, and policy enforcement
- Simplify migrations between providers or models

## Architecture Overview
High-level components:
- **API layer**: FastAPI routes under `backend/app/api` (current public route: `POST /api/chat`)
- **Service layer**: Orchestrates logic without provider specifics (`backend/app/services`)
- **Provider abstraction**: Base client interface + registry (`backend/app/providers`)
- **Provider implementation**: OpenAI client using the modern SDK (`backend/app/providers/openai_client.py`)
- **Configuration**: Centralized env-based settings with support for multiple environments (`backend/app/core/config.py`)

Request flow:
1. `POST /api/chat` receives a user message.
2. The endpoint injects an `LLMClient` via dependency injection.
3. Service layer maps the request into provider-neutral schemas.
4. Provider client calls the LLM and returns a normalized response.

## Run Locally
Prereqs:
- Python 3.11+
- An OpenAI API key (or a compatible gateway URL)

Setup:
1. Create and activate a virtual environment:
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1`
2. Install dependencies:
   - `pip install -r backend/requirements.txt`
3. Create an environment file:
   - `backend/.env.dev` (recommended)
   - Example values:
     - `ENVIRONMENT=dev`
     - `OPENAI_API_KEY=your_key`
     - `DEFAULT_MODEL=gpt-4o-mini`
     - `OPENAI_BASE_URL=https://api.openai.com/v1` (optional)
4. Run the server:
   - `cd backend`
   - `uvicorn app.main:app --reload --port 8000`

Test:
```
POST http://localhost:8000/api/chat
{
  "message": "Hello"
}
```

## Future Roadmap
- Multi-provider routing and fallback
- Streaming responses and tool-calling support
- Request/response logging, tracing, and metrics
- Rate limiting and cost controls
- Authn/authz (API keys or JWT)
- Configurable prompt templates and system policies
