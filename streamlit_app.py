import hashlib
import hmac
import os

import streamlit as st
from openai import APIError

from app.config import MAX_PDF_UPLOAD_BYTES, get_openrouter_api_key
from app.graph.workflow import graph
from app.services.documents import document_store


st.set_page_config(
    page_title="Document Desk",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)


def read_hosted_secrets():
    """Read deployment secrets without ever rendering them in the UI."""
    try:
        api_key = st.secrets.get("OPENROUTER_API_KEY")
        app_password = st.secrets.get("APP_PASSWORD")
    except Exception:
        api_key = None
        app_password = None
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = str(api_key)
    return bool(get_openrouter_api_key()), bool(api_key), app_password


HAS_API_KEY, HOSTED_API_KEY, HOSTED_APP_PASSWORD = read_hosted_secrets()

st.markdown(
    """
    <style>
    :root {
      --ink: #192a36;
      --muted: #6c7a83;
      --paper: #f6f7f4;
      --line: #e2e7e2;
      --accent: #3d806c;
      --accent-soft: #e6f1eb;
    }
    .stApp { background: var(--paper); color: var(--ink); }
    [data-testid="stSidebar"] {
      background: #eef2ed;
      border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 1.4rem; }
    .block-container { max-width: 1120px; padding-top: 2.2rem; }
    .brand-mark {
      display: inline-flex; align-items: center; justify-content: center;
      width: 2.3rem; height: 2.3rem; border-radius: .75rem;
      color: white; background: var(--accent); font-size: 1.15rem;
      margin-right: .55rem; vertical-align: middle;
    }
    .brand-name { font-size: 1.18rem; font-weight: 700; color: var(--ink); }
    .eyebrow {
      color: var(--accent); font-size: .72rem; font-weight: 700;
      letter-spacing: .14em; text-transform: uppercase; margin-bottom: .55rem;
    }
    .hero-copy { color: var(--muted); font-size: 1.04rem; margin-top: -.5rem; }
    .upload-note { color: var(--muted); font-size: .82rem; line-height: 1.5; }
    [data-testid="stMetric"] {
      background: #fff; border: 1px solid var(--line);
      padding: .85rem 1rem; border-radius: .9rem;
    }
    [data-testid="stChatMessage"] {
      border: 1px solid var(--line); border-radius: 1rem;
      background: #fff; padding: .9rem 1rem;
    }
    .empty-card {
      border: 1px dashed #b8c9be; border-radius: 1.1rem; background: #fff;
      padding: 2rem; margin-top: 1.2rem;
    }
    .small-muted { color: var(--muted); font-size: .88rem; }
    div.stButton > button[kind="secondary"] { border-radius: .7rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

for key, initial in (
    ("document_id", None),
    ("document_hash", None),
    ("last_upload_hash", None),
    ("upload_error", None),
    ("uploader_epoch", 0),
    ("messages", []),
):
    st.session_state.setdefault(key, initial)

if HOSTED_API_KEY:
    if not HOSTED_APP_PASSWORD:
        st.error(
            "Add APP_PASSWORD in Streamlit Community Cloud → App settings → "
            "Secrets before enabling OpenRouter for a hosted app."
        )
        st.stop()
    if not st.session_state.get("access_granted", False):
        with st.form("document_desk_access"):
            entered_password = st.text_input(
                "App password",
                type="password",
                autocomplete="current-password",
            )
            submitted = st.form_submit_button("Unlock Document Desk")
        if submitted and hmac.compare_digest(
            entered_password.encode("utf-8"),
            str(HOSTED_APP_PASSWORD).encode("utf-8"),
        ):
            st.session_state.access_granted = True
            st.rerun()
        if submitted:
            st.error("That password did not match.")
        st.stop()

st.markdown(
    '<span class="brand-mark">D</span><span class="brand-name">Document Desk</span>',
    unsafe_allow_html=True,
)
st.markdown('<div class="eyebrow">Your private reading workspace</div>', unsafe_allow_html=True)
st.title("Ask your documents.")
st.markdown(
    '<div class="hero-copy">Upload a PDF, then explore it with answers linked to the pages they came from.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown("### Your document")
    st.caption("Each upload gets its own temporary index.")

    if st.session_state.document_id and st.button(
        "Clear current PDF",
        use_container_width=True,
    ):
        document_store.delete(st.session_state.document_id)
        st.session_state.document_id = None
        st.session_state.document_hash = None
        st.session_state.last_upload_hash = None
        st.session_state.upload_error = None
        st.session_state.messages = []
        st.session_state.uploader_epoch += 1
        st.rerun()

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
        accept_multiple_files=False,
        key=f"pdf_upload_{st.session_state.uploader_epoch}",
        help="Text-searchable PDFs up to 25 MB are supported.",
    )
    st.markdown(
        '<div class="upload-note">Uploads are processed in memory. Scanned PDFs need OCR before upload.</div>',
        unsafe_allow_html=True,
    )

    if uploaded_file is not None:
        pdf_bytes = uploaded_file.getvalue()
        upload_hash = hashlib.sha256(pdf_bytes).hexdigest()
        if upload_hash != st.session_state.last_upload_hash:
            st.session_state.last_upload_hash = upload_hash
            st.session_state.upload_error = None
            if len(pdf_bytes) > MAX_PDF_UPLOAD_BYTES:
                st.session_state.upload_error = "PDF files must be 25 MB or smaller."
            else:
                with st.spinner("Reading PDF and creating its private index…"):
                    try:
                        new_record = document_store.add_pdf(
                            pdf_bytes,
                            uploaded_file.name,
                        )
                        previous_id = st.session_state.document_id
                        st.session_state.document_id = new_record.document_id
                        st.session_state.document_hash = upload_hash
                        st.session_state.messages = []
                        if previous_id:
                            document_store.delete(previous_id)
                    except ValueError as exc:
                        st.session_state.upload_error = str(exc)
                    except Exception:
                        st.session_state.upload_error = (
                            "The index could not be built. Check the app logs and retry."
                        )

        if st.session_state.upload_error:
            st.error(st.session_state.upload_error)
            if st.button("Retry indexing", use_container_width=True):
                st.session_state.last_upload_hash = None
                st.rerun()
        elif st.session_state.document_hash == upload_hash:
            st.success("PDF ready to chat with.")

    if st.session_state.document_id:
        st.divider()
        st.markdown("**Privacy**")
        st.caption(
            "Only the passages retrieved for a question are sent to OpenRouter. "
            "The PDF and its index are temporary."
        )
        st.caption("A session expires after 60 minutes without activity.")

record = (
    document_store.get(st.session_state.document_id)
    if st.session_state.document_id
    else None
)
if st.session_state.document_id and record is None:
    st.session_state.document_id = None
    st.session_state.document_hash = None
    st.session_state.last_upload_hash = None
    st.session_state.messages = []
    if uploaded_file is not None:
        st.rerun()

if record:
    metric_columns = st.columns(3)
    metric_columns[0].metric("PDF", record.filename)
    metric_columns[1].metric("Pages indexed", record.page_count)
    metric_columns[2].metric("Text passages", record.chunk_count)
    st.divider()

    if not HAS_API_KEY:
        st.info(
            "Add OPENROUTER_API_KEY to your local .env file, or add it under "
            "App settings → Secrets on Streamlit Community Cloud to enable answers."
        )
else:
    st.markdown(
        """
        <div class="empty-card">
          <div class="eyebrow">Start here</div>
          <h3>Your document is the source of truth.</h3>
          <p class="small-muted">
            Add a PDF from the left panel. Once its text is indexed, ask for a
            summary, a definition, a comparison, or a detail from a specific page.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message["role"] == "assistant":
            for index, source in enumerate(message.get("sources", []), start=1):
                page = source.get("page")
                page_label = f"Page {page}" if page is not None else "Page unknown"
                with st.expander(
                    f"Source {index} · {page_label} · "
                    f"{source['relevance']:.0%} match"
                ):
                    st.text(source["text"])

if record:
    if not st.session_state.messages:
        st.markdown(
            '<div class="small-muted">Try: “Summarize the main ideas” or “What does the document say about …?”</div>',
            unsafe_allow_html=True,
        )

    question = st.chat_input(
        "Ask a question about this PDF…",
        max_chars=2000,
        disabled=not HAS_API_KEY,
    )
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching the PDF and drafting an answer…"):
                try:
                    result = graph.invoke(
                        {
                            "question": question,
                            "vector_db": record.vector_db,
                        }
                    )
                    answer = result["answer"]
                    sources = result["sources"]
                    st.markdown(answer)
                    for index, source in enumerate(sources, start=1):
                        page = source.get("page")
                        page_label = f"Page {page}" if page is not None else "Page unknown"
                        with st.expander(
                            f"Source {index} · {page_label} · "
                            f"{source['relevance']:.0%} match"
                        ):
                            st.text(source["text"])
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "sources": sources,
                        }
                    )
                except ValueError as exc:
                    st.error(str(exc))
                except APIError:
                    st.error("The language model request failed. Please try again.")
                except Exception:
                    st.error("Something went wrong while answering. Please try again.")
