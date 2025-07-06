import streamlit as st
from qa_engine import load_data, chunk_text, ask_question
import os
import tempfile

st.set_page_config(page_title="Ask Any Document via Gemini", layout="wide")
st.title("📚 Ask Questions from Your Documents")
st.markdown("Supports: `.txt`, `.pdf`, `.docx`")

# File upload
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
question = st.text_input("Ask a question based on the content:")

if uploaded_file:
    # Save to a temporary file
    file_ext = os.path.splitext(uploaded_file.name)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    # Load and chunk the content
    try:
        data = load_data(temp_path)
        chunks = chunk_text(data)

        if question:
            with st.spinner("Getting answer from Gemini..."):
                answer = ask_question(question, chunks)
            st.success("Answer:")
            st.write(answer)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
