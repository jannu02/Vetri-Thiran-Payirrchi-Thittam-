import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")

DOCUMENT_TYPES = [
    "Contract",
    "Agreement",
    "Non-Disclosure Agreement",
    "Service Agreement",
    "Employment Agreement",
    "Lease Agreement",
    "Other Legal Document",
]

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1200px; padding-top: 2rem; }
    .brand { font-size: 2.3rem; font-weight: 700; margin-bottom: 0; }
    .subtitle { color: #666; margin-top: 0.2rem; }
    .legal-document {
        background: white;
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 28px;
        line-height: 1.65;
        color: #222;
    }
    .legal-document h1 { text-align: center; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="brand">⚖️ LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-powered legal document drafting workspace</div>',
    unsafe_allow_html=True,
)

st.info(
    "LegalEase creates drafts from the information you provide. "
    "Review the generated document carefully before signing or relying on it."
)

if "content" not in st.session_state:
    st.session_state.content = ""
if "document_type" not in st.session_state:
    st.session_state.document_type = "Non-Disclosure Agreement"

left, right = st.columns([1, 1.25], gap="large")

with left:
    st.subheader("Document Details")

    document_type = st.selectbox(
        "Document type",
        DOCUMENT_TYPES,
        index=DOCUMENT_TYPES.index(st.session_state.document_type)
        if st.session_state.document_type in DOCUMENT_TYPES
        else 0,
    )

    parties = st.text_area(
        "Parties involved",
        placeholder="Example: Company A and Company B",
        height=100,
    )

    terms = st.text_area(
        "Terms and conditions",
        placeholder="Describe the obligations, restrictions, payment terms, confidentiality terms, etc.",
        height=220,
    )

    effective_date = st.date_input(
        "Effective date",
        value=date.today(),
    )

    generate = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True,
    )

    if generate:
        if not parties.strip() or not terms.strip():
            st.error("Please enter both parties and terms.")
        else:
            payload = {
                "document_type": document_type,
                "parties": parties,
                "terms": terms,
                "effective_date": effective_date.isoformat(),
            }

            with st.spinner("Generating your draft with Gemini..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/generate",
                        json=payload,
                        timeout=120,
                    )
                    response.raise_for_status()
                    data = response.json()
                    st.session_state.document_type = data["document_type"]
                    st.session_state.content = data["content"]
                    st.success("Document generated.")
                except requests.RequestException as exc:
                    detail = "Backend request failed."
                    if getattr(exc, "response", None) is not None:
                        try:
                            detail = exc.response.json().get("detail", detail)
                        except Exception:
                            pass
                    st.error(detail)

with right:
    st.subheader("Document Preview & Editing")

    if st.session_state.content:
        edited = st.text_area(
            "Edit the generated document",
            value=st.session_state.content,
            height=560,
            key="document_editor",
        )
        st.session_state.content = edited

        st.caption(
            "The text above is the source used for all downloads. "
            "Make your final edits before exporting."
        )

        preview_tab, raw_tab = st.tabs(["Preview", "Plain Text"])

        with preview_tab:
            from backend.services.html_formatter import format_html_preview
            st.markdown(
                format_html_preview(st.session_state.content),
                unsafe_allow_html=True,
            )

        with raw_tab:
            st.code(st.session_state.content, language="text")

        st.divider()
        st.subheader("Download")

        export_cols = st.columns(3)

        for col, fmt in zip(export_cols, ["txt", "docx", "pdf"]):
            with col:
                if st.button(
                    f"Prepare {fmt.upper()}",
                    use_container_width=True,
                    key=f"prepare_{fmt}",
                ):
                    try:
                        payload = {
                            "document_type": st.session_state.document_type,
                            "content": st.session_state.content,
                        }
                        response = requests.post(
                            f"{BACKEND_URL}/export/{fmt}",
                            json=payload,
                            timeout=60,
                        )
                        response.raise_for_status()
                        st.session_state[f"download_{fmt}"] = response.content
                    except requests.RequestException as exc:
                        st.error(f"{fmt.upper()} export failed: {exc}")

        for fmt, mime in [
            ("txt", "text/plain"),
            ("docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
            ("pdf", "application/pdf"),
        ]:
            data = st.session_state.get(f"download_{fmt}")
            if data:
                st.download_button(
                    f"Download {fmt.upper()}",
                    data=data,
                    file_name=f"legalease_document.{fmt}",
                    mime=mime,
                    use_container_width=True,
                    key=f"download_button_{fmt}",
                )
    else:
        st.markdown(
            """
            ### Your generated document will appear here

            1. Select a document type.
            2. Enter the parties.
            3. Describe the terms.
            4. Choose the effective date.
            5. Click **Generate Document**.
            """
        )
