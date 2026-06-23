from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

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