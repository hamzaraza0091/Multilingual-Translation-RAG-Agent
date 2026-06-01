"""
app.py
FREE Multilingual RAG Translation Agent
Streamlit + Deep Translator + Local RAG

Run:
    streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from deep_translator import GoogleTranslator
from langdetect import detect

from rag_store import RAGStore


# ─────────────────────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Free Multilingual RAG Agent",
    page_icon="🌍",
    layout="centered",
)


# ─────────────────────────────────────────────────────────────
# Custom CSS
# ─────────────────────────────────────────────────────────────

st.markdown("""
<style>

.block-container {
    max-width: 850px;
    padding-top: 1.5rem;
}

.main-title {
    text-align:center;
    font-size:2rem;
    font-weight:700;
    margin-bottom:0.3rem;
}

.sub-title {
    text-align:center;
    color:gray;
    margin-bottom:2rem;
}

.user-bubble {
    background:#dbeafe;
    color:#1e3a8a;
    padding:12px 16px;
    border-radius:16px 4px 16px 16px;
    margin-bottom:10px;
    max-width:80%;
    margin-left:auto;
    white-space:pre-wrap;
}

.ai-bubble {
    background:#ffffff;
    border:1px solid #e5e7eb;
    padding:14px 18px;
    border-radius:4px 16px 16px 16px;
    margin-bottom:14px;
    max-width:80%;
    white-space:pre-wrap;
    box-shadow:0 1px 3px rgba(0,0,0,0.05);
}

.detected {
    font-size:0.75rem;
    color:#2563eb;
    margin-bottom:8px;
    font-weight:600;
}

.rag-note {
    margin-top:10px;
    padding-top:8px;
    border-top:1px solid #e5e7eb;
    color:#9ca3af;
    font-size:0.7rem;
}

.stats {
    background:#f9fafb;
    border:1px solid #e5e7eb;
    padding:10px 14px;
    border-radius:10px;
    margin-bottom:1rem;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# Supported Languages
# ─────────────────────────────────────────────────────────────

LANGUAGES = {
    "English": "en",
    "Urdu": "ur",
    "German": "de",
    "French": "fr",
    "Spanish": "es",
    "Arabic": "ar",
    "Hindi": "hi",
    "Japanese": "ja",
    "Chinese": "zh-cn",
    "Russian": "ru",
    "Turkish": "tr",
    "Italian": "it",
    "Korean": "ko",
}


# ─────────────────────────────────────────────────────────────
# Session State
# ─────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = []

if "rag" not in st.session_state:
    st.session_state.rag = RAGStore()

if "turns" not in st.session_state:
    st.session_state.turns = 0

if "last_language" not in st.session_state:
    st.session_state.last_language = None


rag = st.session_state.rag


# ─────────────────────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────────────────────

with st.sidebar:

    st.title("⚙️ Settings")

    target_language_name = st.selectbox(
        "🌍 Translate To",
        list(LANGUAGES.keys()),
        index=0
    )

    target_language = LANGUAGES[target_language_name]

    st.divider()

    st.subheader("📊 RAG Stats")

    st.metric(
        "Chunks Stored",
        rag.size
    )

    st.metric(
        "Conversation Turns",
        st.session_state.turns
    )

    if st.session_state.last_language:
        st.metric(
            "Last Detected",
            st.session_state.last_language
        )

    st.divider()

    if st.button("🗑️ Clear Memory", use_container_width=True):

        st.session_state.messages = []
        st.session_state.turns = 0
        st.session_state.last_language = None

        rag.clear()

        st.rerun()


# ─────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────

st.markdown(
    '<div class="main-title">🌍 Free Multilingual RAG Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Translation · Memory · Embeddings · Vector Retrieval</div>',
    unsafe_allow_html=True
)


# ─────────────────────────────────────────────────────────────
# Translation Function
# ─────────────────────────────────────────────────────────────

def translate_text(
    user_input: str,
    target_lang: str,
):

    try:
        detected = detect(user_input)

    except Exception:
        detected = "Unknown"

    try:

        translated = GoogleTranslator(
            source="auto",
            target=target_lang
        ).translate(user_input)

    except Exception as e:

        return {
            "detected_language": detected,
            "translation": f"Translation Error: {e}",
            "rag_note": "Translation failed.",
        }

    return {
        "detected_language": detected,
        "translation": translated,
        "rag_note": "Free translation completed successfully.",
    }


# ─────────────────────────────────────────────────────────────
# Chat Display
# ─────────────────────────────────────────────────────────────

for msg in st.session_state.messages:

    if msg["role"] == "user":

        st.markdown(
            f"""
            <div class="user-bubble">
                {msg["content"]}
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="ai-bubble">

                <div class="detected">
                    🌍 Detected Language:
                    {msg["detected_language"]}
                </div>

                {msg["translation"]}

                <div class="rag-note">
                    🗄️ {msg["rag_note"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ─────────────────────────────────────────────────────────────
# Input Form
# ─────────────────────────────────────────────────────────────

st.divider()

with st.form("chat_form", clear_on_submit=True):

    user_input = st.text_area(
        "Message",
        placeholder="Type text in any language...",
        height=120,
        label_visibility="collapsed",
    )

    submitted = st.form_submit_button(
        "Translate",
        use_container_width=True
    )


# ─────────────────────────────────────────────────────────────
# Process Message
# ─────────────────────────────────────────────────────────────

def process_message(text: str):

    text = text.strip()

    if not text:
        return

    # Save User Message
    st.session_state.messages.append({
        "role": "user",
        "content": text,
    })

    # Retrieve Similar Chunks
    retrieved = rag.retrieve(
        text,
        top_k=3
    )

    rag_chunks = [
        r["text"]
        for r in retrieved
    ]

    # Translate
    result = translate_text(
        text,
        target_language
    )

    # Save Detected Language
    st.session_state.last_language = result[
        "detected_language"
    ]

    # Add To RAG Store
    rag.add_document(
        original=text,
        translation=result["translation"],
        metadata={
            "source_language": result[
                "detected_language"
            ],
            "target_language": target_language,
        },
    )

    # Increase Turns
    st.session_state.turns += 1

    # Save Assistant Message
    st.session_state.messages.append({
        "role": "assistant",
        "detected_language": result[
            "detected_language"
        ],
        "translation": result[
            "translation"
        ],
        "rag_note": (
            f"{result['rag_note']} "
            f"{len(rag_chunks)} related chunk(s) retrieved."
        ),
    })


# ─────────────────────────────────────────────────────────────
# Run
# ─────────────────────────────────────────────────────────────

if submitted and user_input.strip():

    process_message(user_input)

    st.rerun()