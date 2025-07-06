import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import Document


#Load environment variables
load_dotenv()


#Initialize Gemini LLM + Embeddings
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

embedding = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


#Document Loader
def load_document(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return PyPDFLoader(file_path).load()
    elif ext == ".txt":
        return TextLoader(file_path, encoding="utf-8").load()
    elif ext == ".docx":
        return Docx2txtLoader(file_path).load()
    else:
        raise ValueError("❌ Unsupported file format!")


#Custom Chunking Logic
def chunk_documents(docs, chunk_size=1000, overlap=200):
    """Split each document's content into smaller overlapping chunks."""
    all_chunks = []

    for doc in docs:
        text = doc.page_content
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            metadata = doc.metadata.copy()
            all_chunks.append(Document(page_content=chunk, metadata=metadata))
            start += chunk_size - overlap  # overlap for context retention

    return all_chunks


#LangChain QA Chain
def ask_with_langchain(retriever, question):
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    result = qa_chain.invoke({"query": question})
    return result["result"]  



#Main Q&A Flow
def ask_question_with_langchain(file_path, question):
    # Step 1: Load the document
    documents = load_document(file_path)

    # Step 2: Chunk using custom function
    chunks = chunk_documents(documents, chunk_size=1000, overlap=200)

    # Step 3: Create vector DB & retriever
    vectordb = Chroma.from_documents(chunks, embedding)
    retriever = vectordb.as_retriever()

    # Step 4: Ask the question
    return ask_with_langchain(retriever, question)
