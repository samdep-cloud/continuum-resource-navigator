# Continuum Resource Navigator

An LLM-powered resource-navigation service that helps clinical staff identify support services relevant to an individual’s stated needs, explain potential matches, and clarify missing information.

## Why this project

Finding appropriate support services requires staff to interpret an individual’s needs, search resource information, and check eligibility requirements. Continuum Resource Navigator supports that workflow by comparing an inquiry against a supplied resource catalog and returning structured recommendations for staff review.

The project draws on firsthand experience with resource-navigation teams supporting behavioral-health operations.

## Current functionality

- FastAPI `/ask` endpoint with typed request and response models.
- Structured model output validated against a Pydantic schema.
- Resource matching using a small fictional service catalog supplied in the model context.
- Follow-up questions for vague inquiries or missing eligibility information.
- Checks that reject resource IDs absent from the catalog.
- Token usage and estimated per-call cost reporting.
- API timeout and provider-error handling.
- Streamlit interface for submitting inquiries and reviewing results.

## How it works

1. A staff member enters an inquiry describing the individual’s needs.
2. FastAPI validates the request.
3. The service supplies the inquiry, catalog, and matching instructions to the model.
4. The model returns a structured answer.
5. The service checks resource IDs and calculates estimated usage cost.
6. Streamlit displays the result, potential matches, and clarification questions.

The current version supplies the full catalog directly in context. Retrieval-augmented generation is a future iteration.

## Technology

Python 3.12 · FastAPI · Pydantic · OpenAI SDK · Streamlit · Requests

## Run locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Create a local `.env` file:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

The `.env` file must remain excluded from version control.

Start the API:

```bash
python -m uvicorn main:app --reload
```

In a second terminal, activate the same virtual environment and start the UI:

```bash
source .venv/bin/activate
python -m streamlit run streamlit_app.py
```

Open the local URL printed by Streamlit. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

The UI defaults to an API address of `http://127.0.0.1:8000`. Set `API_BASE_URL` to connect it to another deployment.

## API example

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"inquiry":"An adult in Example County needs groceries because they cannot afford enough food."}'
```

The response includes:

- `answer.message`: a brief explanation of the result.
- `answer.matches`: resource IDs and reasons for potential matches.
- `answer.follow_up_questions`: questions about information needed for matching.
- `tokens_used`: total tokens reported for the model call.
- `cost_usd`: estimated model-call cost based on configured token rates.

## Initial manual checks

| Scenario | Behavior checked |
|---|---|
| Blank or whitespace-only inquiry | Request rejected before a model call |
| Vague financial need | Clarification requested |
| Grocery need in Example County | Food resource returned |
| Grocery need outside the service area | No match returned |
| API unavailable | Connection error displayed in the UI |

These checks establish initial behavior; they are not a comprehensive evaluation suite.

## Scope and limitations

This prototype uses fictional resources and fictional inquiries. Recommendations require staff review and do not establish eligibility, current availability, or a completed referral.

The service does not diagnose, classify clinical risk, or determine whether someone should receive clinical care. Model-generated explanations can contain errors even when they satisfy the response schema.

API usage incurs charges. Cost estimates depend on the configured model rates. Deployment URLs are shared privately rather than published in this repository.

## Next iterations

- Retrieval over a larger resource collection with source citations.
- Repeatable evaluations for matching, clarification, and unsupported claims.
- More precise eligibility explanations.
- Resource names and supporting catalog details in the interface.