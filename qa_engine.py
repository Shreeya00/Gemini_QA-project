from dotenv import load_dotenv
import os
import google.generativeai as genai
import fitz  # PyMuPDF for PDFs
import docx  # for Word files

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Model setup
model = genai.GenerativeModel("models/gemini-1.5-flash")

# ---------- File Reading ----------
def load_data(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

# ---------- Chunking ----------
def chunk_text(text, max_chars=1000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

# ---------- Gemini Q&A ----------
def ask_question(question, chunks):
    context = "\n\n".join(chunks[:3])  # Use top 3 chunks
    prompt = f"""Use the context below to answer the question:

    Context:
    {context}

    Question: {question}
    Answer:"""

    response = model.generate_content(prompt)
    return response.text
