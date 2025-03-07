from transformers import pipeline
from langchain.text_splitter import RecursiveCharacterTextSplitter
from huggingface_hub import login
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
huggingface_token = os.getenv("HUGGINGFACE_TOKEN")

# Log in to Hugging Face (if needed for access to models)
if huggingface_token:
    login(token=huggingface_token)

# Load summarization model
summarizer = pipeline("summarization", model="facebook/distilbart-cnn-12-6")

def summarize_text(input_text):
    """Summarizes long text using BART with LangChain-based chunking."""
    
    def chunk_text(text):
        """Splits text into manageable chunks using LangChain."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024,   # Max chunk size (in characters)
            chunk_overlap=200,   # Overlap between chunks
            length_function=len
        )
        return text_splitter.split_text(text)

    # Split the input text into chunks
    chunks = chunk_text(input_text)
    
    summaries = []
    for chunk in chunks:
        # Determine appropriate max/min lengths for summarization
        input_len = len(chunk.split())   
        max_len = min(250, int(input_len * 0.7))
        min_len = max(50, max_len // 2)

        # Ensure max length is within limits
        if max_len > input_len:
            max_len = input_len - 1
            min_len = max(10, max_len // 3)

        # Generate summary for each chunk
        summary = summarizer(chunk, max_length=max_len, min_length=min_len, do_sample=False)[0]["summary_text"]
        summaries.append(summary.strip())  

    # Return combined summary
    return "\n".join(summaries)

