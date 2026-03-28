import os
import google.generativeai as genai


def generate_answer(question: str, context_chunks: list) -> str:

    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key or api_key == "your-gemini-key-here":
        return "[Error: Gemini API key not configured. Add GEMINI_API_KEY to src/.env]"
    
    genai.configure(api_key=api_key)
    
    context = "\n\n".join([
        f"[{i+1}] {chunk['text'][:500]}..."
        for i, chunk in enumerate(context_chunks)
    ])
    
    prompt = f"""Based on the following context, answer the question accurately.

Context:
{context}

Question: {question}

Provide a clear, concise answer based only on the context above."""

    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    model = genai.GenerativeModel(model_name)
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        return f"[Error calling Gemini: {str(e)}]"


def test_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No API key found")
        return
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    response = model.generate_content("Say hello in Arabic")
    print(response.text)