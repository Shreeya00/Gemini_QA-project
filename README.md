#  Gemini Q&A on Uploaded Files

A Streamlit-based web app that uses **Google's Gemini 1.5 API** to answer questions based on any uploaded `.txt`,`pdf` or `docx` dataset — perfect for use cases like academic notes, cheat sheets, articles, or domain-specific documentation.

---

##  Features

-  Upload any `.txt`,`.pdf` or `.docx` file (e.g., Computer Science topics)
-  Ask natural language questions based on the uploaded data
-  Uses **Gemini 1.5 Flash** for fast and cost-efficient responses
-  Integrated with Google Generative AI API (`google-generativeai`)
-  Supports long documents via chunking (auto-splitting of text)
- 🖥 Built using Python + Streamlit + dotenv for clean API handling

---
##  Demo Video

Click the button below to watch the demo:

👉 [Watch Demo Video on Google Drive](https://drive.google.com/file/d/1lffAI0PyHkTHXQuIlrBG4GsuTw0V6azQ/view?usp=sharing)

---

##  Project Structure
```bash
gemini_qa_project/
├── app.py              # Streamlit frontend (file upload + Q&A interface)
├── qa_engine.py        # Gemini API logic and text chunking
├── .env                # Environment file to store API key (excluded from Git)
├── requirements.txt    # Required Python libraries
├── data/               # Folder where uploaded .txt files are saved
└── demo.gif            # (Optional) Demo recording or image


