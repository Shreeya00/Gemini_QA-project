from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


# Load your text file
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Break long text into smaller chunks
def chunk_text(text, max_chars=1000):
    return [text[i:i + max_chars] for i in range(0, len(text), max_chars)]

# Ask Gemini model
def ask_question(question, chunks):
    context = "\n\n".join(chunks[:3])  # Use top 3 chunks
    prompt = f"""Use the context below to answer the question:

    Context:
    {context}

    Question: {question}
    Answer:"""

    response = model.generate_content(prompt)
    return response.text
