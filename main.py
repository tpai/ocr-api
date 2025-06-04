import time
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

from src.config import Config
from src.lm_studio_client import LMStudioClient
from src.file_processor import FileProcessor
from src.ocr_service import OCRService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="OCR API Server",
    description="A simple API server for OCR using LM Studio and RolmOCR model",
    version="1.0.0"
)

# Initialize services
config = Config()
lm_studio_client = LMStudioClient(config)
file_processor = FileProcessor(config)
ocr_service = OCRService(lm_studio_client, file_processor)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "OCR API Server is running", "status": "healthy"}




@app.post("/ocr")
async def process_ocr(file: UploadFile = File(...)):
    """
    Process uploaded image or PDF file and extract text using OCR
    """
    start_time = time.time()
    
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Process the file and extract text
        result = await ocr_service.process_file(file)
        
        processing_time = time.time() - start_time
        
        return {
            "success": True,
            "filename": file.filename,
            "text": result["text"],
            "confidence": result.get("confidence", 0.0),
            "processing_time": round(processing_time, 2),
            "file_type": result.get("file_type", "unknown")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        # Provide simple error messages
        error_message = "Processing failed"
        if "connect" in str(e).lower() or "connection" in str(e).lower():
            error_message = "OCR service unavailable"
        elif "timeout" in str(e).lower():
            error_message = "Processing timeout"
        elif "model" in str(e).lower():
            error_message = "OCR model error"
        
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": error_message,
                "processing_time": round(processing_time, 2),
                "filename": file.filename if file.filename else "unknown"
            }
        )




if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.DEBUG
    )
