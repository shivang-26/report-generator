from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import uuid
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in .env file")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

app = FastAPI(
    title="Project Report Generator API",
    description="API for generating and managing project reports with AI assistance",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class ProjectData(BaseModel):
    title: str
    authors: List[str]
    abstract: Optional[str] = None
    introduction: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None
    references: Optional[List[Dict[str, Any]]] = None
    template: str = "ieee"  # or "springer"

# Create output directory if it doesn't exist
os.makedirs("output", exist_ok=True)

async def generate_ai_text(prompt: str) -> str:
    """Generate text using Gemini API"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI text: {e}")
        return f"Error generating content: {str(e)}"

@app.get("/")
async def read_root():
    return {"message": "Welcome to Project Report Generator API"}

@app.post("/generate-report")
async def generate_report(project_data: ProjectData):
    """Generate a report in DOCX and PDF formats"""
    try:
        # Generate a unique filename
        file_id = str(uuid.uuid4())
        docx_path = f"output/{file_id}.docx"
        pdf_path = f"output/{file_id}.pdf"
        
        # TODO: Generate DOCX using project_data
        # TODO: Convert DOCX to PDF
        
        return {
            "status": "success",
            "message": "Report generated successfully",
            "data": {
                "docx_url": f"/download/{file_id}.docx",
                "pdf_url": f"/download/{file_id}.pdf"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download generated files"""
    file_path = f"output/{filename}"
    if os.path.exists(file_path):
        return FileResponse(
            file_path,
            media_type="application/octet-stream",
            filename=filename
        )
    raise HTTPException(status_code=404, detail="File not found")

# AI Endpoints
@app.post("/ai/abstract")
async def generate_abstract(text: str = Query(..., description="The content to generate an abstract for")):
    """Generate an abstract using AI"""
    prompt = f"""Generate a professional abstract (150-250 words) for a research paper based on the following content.
    Include the purpose, methodology, findings, and significance of the research.

    Content:
    {text}

    Abstract:"""
    
    abstract = await generate_ai_text(prompt)
    return {"abstract": abstract}

@app.post("/ai/conclusion")
async def generate_conclusion(text: str = Query(..., description="The content to generate a conclusion for")):
    """Generate a conclusion using AI"""
    prompt = f"""Write a comprehensive conclusion for a research paper based on the following content.
    The conclusion should summarize the key findings, discuss their implications, and suggest future research directions.

    Content:
    {text}

    Conclusion:"""
    
    conclusion = await generate_ai_text(prompt)
    return {"conclusion": conclusion}

@app.post("/ai/reword")
async def reword_text(text: str = Query(..., description="The text to improve")):
    """Improve grammar and flow of text"""
    prompt = f"""Improve the grammar, clarity, and flow of the following academic text while preserving its original meaning.
    Make it more professional and academic. Do not change the technical terms or specific information.

    Original text:
    {text}

    Improved version:"""
    
    rewritten = await generate_ai_text(prompt)
    return {"rewritten_text": rewritten}

@app.post("/ai/synopsis")
async def generate_synopsis(text: str = Query(..., description="The content to summarize")):
    """Generate a 2-page summary"""
    prompt = f"""Create a concise 2-page summary (approximately 1000 words) of the following content.
    Include the main points, methodology, results, and conclusions.

    Content:
    {text}

    Summary:"""
    
    synopsis = await generate_ai_text(prompt)
    return {"synopsis": synopsis}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)