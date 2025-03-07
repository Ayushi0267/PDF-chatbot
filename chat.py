import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

def chat_with_gemini(question, context):
    """Query Gemini API with a given question and context."""
    model = genai.GenerativeModel("gemini-1.5-pro")
    prompt = f"""
    Answer the question based on the provided context. If the answer is not available, say "answer is not available in the context."
    
    Context:
    {context}
    
    Question:
    {question}
    
    Answer:
    """
    response = model.generate_content(prompt)
    return response.text if response else "No response received."
