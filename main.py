from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import uuid
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from motor.motor_asyncio import AsyncIOMotorCollection

# Import database and models
from database import connect_to_mongo, close_mongo_connection, get_reports_collection
from models import Report, ReportCreate, UserCreate, UserInDB, PyObjectId

# Load environment variables
load_dotenv()

# Initialize Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in environment variables")
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

# Database connection events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

# Helper function to get reports collection
async def get_reports() -> AsyncIOMotorCollection:
    return get_reports_collection()

async def generate_ai_text(prompt: str) -> str:
    """Generate text using Gemini API"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating AI text: {e}")
        return f"Error generating content: {str(e)}"

# Report endpoints
@app.post("/api/reports/", response_model=Report)
async def create_report(report: ReportCreate):
    """Create a new report"""
    reports_collection = await get_reports()
    report_dict = report.dict()
    report_dict["created_at"] = datetime.utcnow()
    report_dict["updated_at"] = datetime.utcnow()
    
    result = await reports_collection.insert_one(report_dict)
    created_report = await reports_collection.find_one({"_id": result.inserted_id})
    return created_report

@app.get("/api/reports/", response_model=List[Report])
async def list_reports(limit: int = 10, skip: int = 0):
    """List all reports with pagination"""
    reports_collection = await get_reports()
    reports = await reports_collection.find().skip(skip).limit(limit).to_list(length=limit)
    return reports

@app.get("/api/reports/{report_id}", response_model=Report)
async def get_report(report_id: str):
    """Get a specific report by ID"""
    reports_collection = await get_reports()
    try:
        report = await reports_collection.find_one({"_id": PyObjectId(report_id)})
        if report is None:
            raise HTTPException(status_code=404, detail="Report not found")
        return report
    except:
        raise HTTPException(status_code=400, detail="Invalid report ID")

# AI Endpoints
@app.post("/api/ai/abstract")
async def generate_abstract(text: str):
    """Generate an abstract using AI"""
    prompt = f"""Generate a professional abstract (150-250 words) for a research paper based on the following content.
    Include the purpose, methodology, findings, and significance of the research.

    Content:
    {text}

    Abstract:"""
    
    abstract = await generate_ai_text(prompt)
    return {"abstract": abstract}

@app.post("/api/ai/conclusion")
async def generate_conclusion(text: str):
    """Generate a conclusion using AI"""
    prompt = f"""Write a comprehensive conclusion for a research paper based on the following content.
    The conclusion should summarize the key findings, discuss their implications, and suggest future research directions.

    Content:
    {text}

    Conclusion:"""
    
    conclusion = await generate_ai_text(prompt)
    return {"conclusion": conclusion}

@app.post("/api/ai/reword")
async def reword_text(text: str):
    """Improve grammar and flow of text"""
    prompt = f"""Improve the grammar, clarity, and flow of the following academic text while preserving its original meaning.
    Make it more professional and academic. Do not change the technical terms or specific information.

    Original text:
    {text}

    Improved version:"""
    
    rewritten = await generate_ai_text(prompt)
    return {"rewritten_text": rewritten}

@app.post("/api/ai/synopsis")
async def generate_synopsis(text: str):
    """Generate a 2-page summary"""
    prompt = f"""Create a concise 2-page summary (approximately 1000 words) of the following content.
    Include the main points, methodology, results, and conclusions.

    Content:
    {text}

    Summary:"""
    
    synopsis = await generate_ai_text(prompt)
    return {"synopsis": synopsis}

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Service is running"}

# This is required for Vercel
def handler(event, context):
    return {
        "statusCode": 200,
        "body": "Hello from Vercel Python!"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
