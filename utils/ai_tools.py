import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

async def generate_ai_text(prompt: str, max_tokens: int = 500) -> Optional[str]:
    """Generate text using Gemini API"""
    if not GEMINI_API_KEY:
        return None
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI text: {e}")
        return None

async def generate_abstract(text: str) -> str:
    """Generate an abstract using AI"""
    prompt = f"""Generate a concise and professional abstract for a research paper based on the following content.
    The abstract should be 150-250 words and include the purpose, methodology, findings, and significance of the research.
    
    Content:
    {text}
    
    Abstract:"""
    result = await generate_ai_text(prompt)
    return result or "Could not generate abstract. Please try again later."

async def generate_conclusion(text: str) -> str:
    """Generate a conclusion using AI"""
    prompt = f"""Write a comprehensive conclusion for a research paper based on the following content.
    The conclusion should summarize the key findings, discuss their implications, and suggest future research directions.
    
    Content:
    {text}
    
    Conclusion:"""
    result = await generate_ai_text(prompt)
    return result or "Could not generate conclusion. Please try again later."

async def reword_text(text: str) -> str:
    """Improve grammar and flow of text using AI"""
    prompt = f"""Improve the grammar, clarity, and flow of the following academic text while preserving its original meaning.
    Make it more professional and academic. Do not change the technical terms or specific information.
    
    Original text:
    {text}
    
    Improved version:"""
    result = await generate_ai_text(prompt)
    return result or text  # Return original if AI fails

async def generate_synopsis(text: str) -> str:
    """Generate a 2-page summary of the content"""
    prompt = f"""Create a concise 2-page summary (approximately 1000 words) of the following content.
    Include the main points, methodology, results, and conclusions.
    
    Content:
    {text}
    
    Summary:"""
    result = await generate_ai_text(prompt, max_tokens=1000)
    return result or "Could not generate synopsis. Please try again later."
