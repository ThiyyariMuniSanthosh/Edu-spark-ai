"""EduSpark AI - Stage 1: student doubt solver (text questions and PDF study material)."""
import streamlit as st

from ai_service import AIServiceError, ask_gemini, get_api_key
from pdf_utils import PDFError, extract_pdf_text

LANGUAGES = ["English", "Telugu", "Hindi", "Tamil", "Kannada", "Malayalam"]
MAX_QUESTION_CHARS = 2000

st.set_page_config(page_title="EduSpark AI", page_icon="⚡", layout="wide")

for key, default in {"history": [], "doc_text": None, "doc_name": None, "last_upload": None}.items():
    st.session_state.setdefault(key, default)

st.title("⚡ EduSpark AI")
st.caption("Learn Smarter. Teach Better. Grow Together.")

with st.sidebar:
    st.header("Settings")
    language = st.selectbox("Explanation language", LANGUAGES)

    st.subheader("Study material (optional)")
    uploaded = st.file_uploader("Upload a PDF", type=["pdf"])
    if uploaded is None:
        st.session_state.doc_text = None
        st.session_state.doc_name = None
        st.session_state.last_upload = None
    elif uploaded.name != st.session_state.last_upload:
        st.session_state.last_upload = uploaded.name
        try:
            with st.spinner("Reading PDF..."):
                st.session_state.doc_text = extract_pdf_text(uploaded.getvalue(), uploaded.name)
            st.session_state.doc_name = uploaded.name
            st.success(f"Loaded {uploaded.name}")
        except PDFError as exc:
            st.session_state.doc_text = None
            st.session_state.doc_name = None
            st.error(str(exc))
    if st.session_state.doc_name:
        st.info(f"Answering from: {st.session_state.doc_name}")

    st.divider()
    try:
        get_api_key()
        st.success("Gemini key found")
    except AIServiceError as exc:
        st.warning(str(exc))
    if st.button("Clear chat"):
        st.session_state.history = []
        st.rerun()

if not st.session_state.history:
    st.info("Ask a doubt below. Upload a PDF in the sidebar to get answers from your study material.")

for role, text in st.session_state.history:
    with st.chat_message("user" if role == "Student" else "assistant"):
        st.markdown(text)

question = (st.chat_input("Ask a doubt or a follow-up question") or "").strip()
if question:
    if len(question) > MAX_QUESTION_CHARS:
        st.error(f"Please keep questions under {MAX_QUESTION_CHARS} characters.")
    else:
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Thinking..."):
                    answer = ask_gemini(
                        question,
                        language,
                        st.session_state.doc_text,
                        st.session_state.history,
                    )
                st.markdown(answer)
                st.session_state.history.append(("Student", question))
                st.session_state.history.append(("Tutor", answer))
            except AIServiceError as exc:
                st.error(str(exc))
