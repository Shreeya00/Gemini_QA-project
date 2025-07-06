import streamlit as st
from qa_engine import load_data, chunk_text, ask_question
import os

st.set_page_config(page_title="Ask CS Dataset via Gemini", layout="wide")
st.title("💬 Ask Questions from Your Dataset")

# File upload
uploaded_file = st.file_uploader("Upload a .txt file", type=["txt"])
question = st.text_input("Ask a question based on the data:")

if uploaded_file:
    # Save file to 'data' folder
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    # Load + chunk the content
    data = load_data(file_path)
    chunks = chunk_text(data)

    if question:
        with st.spinner("Getting answer from Gemini..."):
            answer = ask_question(question, chunks)
        st.success("Answer:")
        st.write(answer)
