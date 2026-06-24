from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import anthropic
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Report Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

@app.get("/")
def home():
    return {"message": "Report Generator API is running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    df = pd.read_csv(file_path, encoding='utf-8') if file.filename.endswith(".csv") else pd.read_excel(file_path)
    
    summary = {
        "rows": len(df),
        "columns": list(df.columns),
        "numeric_summary": {}
    }
    
    for col in df.select_dtypes(include='number').columns:
        summary["numeric_summary"][col] = {
            "min": float(round(df[col].min(), 2)),
            "max": float(round(df[col].max(), 2)),
            "mean": float(round(df[col].mean(), 2)),
            "total": float(round(df[col].sum(), 2))
        }
    
    return {
        "message": "File uploaded and analyzed successfully",
        "filename": file.filename,
        "summary": summary
    }

class ReportRequest(BaseModel):
    filename: str

@app.post("/generate-report")
async def generate_report(request: ReportRequest):
    file_path = f"uploads/{request.filename}"
    
    df = pd.read_csv(file_path) if request.filename.endswith(".csv") else pd.read_excel(file_path)
    
    summary = {}
    for col in df.select_dtypes(include='number').columns:
        summary[col] = {
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "mean": float(round(df[col].mean(), 2)),
            "total": float(df[col].sum())
        }
    
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1000,
        messages=[{
            "role": "user",
            "content": f"""You are a business analyst. Analyze this data and write a professional report narrative.

DATA SUMMARY:
{summary}

COLUMNS: {list(df.columns)}
ROWS: {len(df)}

Write a clear, professional 3-4 paragraph business report that:
1. Summarizes overall performance
2. Highlights key trends and insights
3. Identifies the best and worst performing metrics
4. Provides 2-3 actionable recommendations

Keep it concise and business-focused."""
        }]
    )
    
    return {
        "filename": request.filename,
        "summary": summary,
        "report": message.content[0].text
    }