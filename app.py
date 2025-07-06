import streamlit as st
from qa_engine import ask_question_with_langchain
import os
import tempfile

# Page settings
st.set_page_config(page_title="Ask Any Document via Gemini", layout="wide")
st.title("📚 Ask Questions from Your Documents")
st.markdown("Supports: `.txt`, `.pdf`, `.docx`")

# Upload file
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
question = st.text_input("Ask a question based on the document content:")

if uploaded_file:
    file_ext = os.path.splitext(uploaded_file.name)[1]

    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    try:
        if question.strip() != "":
            with st.spinner("💬 Thinking... Gemini is finding your answer..."):
                answer = ask_question_with_langchain(temp_path, question)
            st.success("✅ Answer:")
            st.write(answer)
        else:
            st.info("ℹ️ Please enter a question above.")

    except Exception as e:
        st.error(f"❌ An error occurred:\n`{str(e)}`")
