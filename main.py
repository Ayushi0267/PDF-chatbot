import streamlit as st
import fitz  # PyMuPDF
import io
from chat import chat_with_gemini  
from summary import summarize_text  

# Make sure this is the first Streamlit command in the entire script
st.set_page_config(page_title="PDF Chatbot & Summarizer", layout="wide")

def handle_pdf_upload(file):
    """Extracts text from an uploaded PDF and summarizes it."""
    try:
        if not file.name.endswith(".pdf"):
            st.error("Uploaded file is not a PDF.")
            return

        pdf_bytes = file.getvalue()

        if not pdf_bytes:
            st.error("Uploaded PDF is empty.")
            return

        text = ""
        pdf_stream = io.BytesIO(pdf_bytes)
        with fitz.open(stream=pdf_stream) as pdf:
            for page_num in range(pdf.page_count):
                page = pdf.load_page(page_num)
                extracted_text = page.get_text()
                if extracted_text:
                    text += extracted_text + "\n"

        if not text.strip():
            st.error("No text found in the PDF.")
            return

        summary_text = summarize_text(text)

        # Display summary
        st.subheader("Summary:")
        st.text(summary_text)

        # Download summary
        st.download_button("Download Summary", summary_text, file_name="summary.txt")

    except Exception as e:
        st.error(f"Error: {e}")

def handle_chat(question):
    """Handles chat interaction with Gemini AI."""
    try:
        context = "Provide context from your PDF or predefined data."
        response = chat_with_gemini(question, context)
        st.write(f"**Question:** {question}")
        st.write(f"**Response:** {response}")
    except Exception as e:
        st.error(f"Error: {e}")

# Streamlit UI
st.title("📄 PDF Summarizer & Chatbot")

# PDF upload
st.subheader("Upload a PDF File:")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    handle_pdf_upload(uploaded_file)

# Chatbot interaction
st.subheader("Chat with Gemini AI:")
question = st.text_input("Ask a question about the PDFs:")
if question:
    handle_chat(question)

