# Document Desk

Document Desk is a PDF question-answering dashboard. Upload a text-searchable PDF, wait for its temporary index to build, then ask questions and inspect the source pages behind each answer.

The bundled Agentic AI PDF is only an optional local example. The dashboard and API do not load it automatically.

## Features

- Upload one PDF at a time (up to 25 MB and 500 pages).
- Keep each upload in its own temporary index.
- Retrieve relevant passages and answer from those passages only.
- Show source excerpts with page numbers and a retrieval match score.
- Reject malformed, encrypted, oversized, and image-only PDFs with a useful message.
- Use OpenRouter for answer generation; embeddings run locally with Sentence Transformers.
- Delete documents after 60 minutes without activity, or when cleared/replaced.

Scanned PDFs need OCR before upload. OCR is not included.

## Run locally

Use Python 3.12 or another Python version supported by the dependencies.

1. Create a virtual environment and install dependencies:

    python -m venv .venv

Windows:

    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    Copy-Item .env.example .env

macOS/Linux:

    source .venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env

2. Put your OpenRouter key in .env:

    OPENROUTER_API_KEY=your_openrouter_api_key
    OPENROUTER_MODEL=openrouter/auto

3. Start the dashboard:

    streamlit run streamlit_app.py

The dashboard will be available at http://localhost:8501.

The key is needed only for answers. The dashboard can start and index a PDF without it.

## Deploy free with Streamlit Community Cloud

Streamlit Community Cloud can deploy this app from its GitHub repository at no charge. It connects to the repository and redeploys when a new commit is pushed.

1. Push this repository to a GitHub account.
2. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) with GitHub and choose **Create app**.
3. Select the repository, the main branch, and streamlit_app.py as the app file.
4. In **Advanced settings**, select Python 3.12.
5. In the app's **Settings → Secrets**, add a private app password and your OpenRouter key:

    APP_PASSWORD = "choose-a-private-passphrase"
    OPENROUTER_API_KEY = "your_openrouter_api_key"
    OPENROUTER_MODEL = "openrouter/auto"

6. Deploy the app.

Never commit .env or Streamlit secrets. The repository ignores both.

When an OpenRouter key is configured in Streamlit secrets, the dashboard requires APP_PASSWORD before it allows use of that key. Anyone with the password can use the app's model quota, so do not post the password publicly.

Free hosting has resource and availability limits. The app may sleep or restart; its active PDF sessions and indexes are temporary and will be lost on restart. Hosting is free, while OpenRouter model usage follows the selected model/provider's terms and pricing.

## Privacy and retention

- The uploaded PDF is parsed and indexed in the app process. It is not copied into the GitHub repository or saved as a persistent upload.
- Only the question and retrieved PDF passages are sent to OpenRouter to generate an answer. Review your model provider's data policies before uploading sensitive documents.
- The index is isolated by document ID, expires after 60 minutes without activity, and is held in process memory until deletion, expiration, or app restart.
- The in-memory document store is intended for a small demo. It limits the process to 10 active documents and evicts the least-recently-used document when full.

## REST API

The FastAPI API is available separately for local use:

    uvicorn app.main:app --reload

Interactive API docs are at http://127.0.0.1:8000/docs.

Upload a PDF:

    curl -F "file=@report.pdf" http://127.0.0.1:8000/documents

Use the returned document_id to ask a question:

    curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d '{"document_id":"DOCUMENT_ID","question":"Summarize the main points."}'

Delete a document session when you are done:

    curl -X DELETE http://127.0.0.1:8000/documents/DOCUMENT_ID

The optional API uses the same temporary in-memory document store. Do not expose it publicly without adding access control and abuse protection.

## Project layout

    app/
      api/             FastAPI upload, chat, and delete endpoints
      graph/           LangGraph question-answer workflow
      services/        PDF parsing, document storage, retrieval, embeddings, and LLM
    streamlit_app.py   PDF upload and chat dashboard
    scripts/           Optional local smoke-check scripts
    data/              Optional sample PDF; never loaded by the dashboard
    requirements.txt   Runtime dependencies

## License

See [LICENSE](LICENSE).
