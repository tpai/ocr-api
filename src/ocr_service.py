"""OCR service that coordinates file processing and model inference"""
from typing import Dict, Any
from fastapi import UploadFile, HTTPException
from src.lm_studio_client import LMStudioClient
from src.file_processor import FileProcessor

class OCRService:
    """Service that orchestrates OCR processing"""
    
    def __init__(self, lm_studio_client: LMStudioClient, file_processor: FileProcessor):
        self.lm_studio_client = lm_studio_client
        self.file_processor = file_processor
    
    async def process_file(self, file: UploadFile) -> Dict[str, Any]:
        """Process uploaded file and extract text using OCR"""
        
        # Validate file first
        await self.file_processor.validate_file(file)
        
        # Get file info
        file_info = await self.file_processor.get_file_info(file)
        file_type = file_info["file_type"]
        
        if file_type == "image":
            return await self._process_image_file(file)
        elif file_type == "pdf":
            return await self._process_pdf_file(file)
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_type}")
    
    async def _process_image_file(self, file: UploadFile) -> Dict[str, Any]:
        """Process image file for OCR"""
        try:
            # Process the image
            image_data = await self.file_processor.process_image(file)
            
            # Send to LM Studio for OCR
            ocr_result = await self.lm_studio_client.process_image_ocr(
                image_data["data"], 
                file.filename or "image"
            )
            
            return {
                "text": ocr_result["text"],
                "confidence": ocr_result["confidence"],
                "file_type": "image",
                "image_info": {
                    "format": image_data["format"],
                    "size": image_data["size"],
                    "mode": image_data["mode"]
                },
                "model_used": ocr_result.get("model_used")
            }
            
        except HTTPException:
            raise
        except Exception as e:
            # Provide simple error messages
            error_message = "Image processing failed"
            if "connect" in str(e).lower() or "connection" in str(e).lower():
                error_message = "OCR service unavailable"
            elif "timeout" in str(e).lower():
                error_message = "Processing timeout"
            elif "model" in str(e).lower():
                error_message = "OCR model error"
            raise HTTPException(status_code=500, detail=error_message)
    
    async def _process_pdf_file(self, file: UploadFile) -> Dict[str, Any]:
        """Process PDF file for OCR"""
        try:
            # Process the PDF
            pdf_data = await self.file_processor.process_pdf(file)
            
            combined_text = ""
            confidence_scores = []
            
            # If PDF has extractable text, process it
            if pdf_data["has_text"]:
                text_result = await self.lm_studio_client.process_text_ocr(pdf_data["text_content"])
                combined_text += text_result["text"]
                confidence_scores.append(text_result["confidence"])
            
            # Process any scanned pages (images)
            for image_info in pdf_data["images"]:
                try:
                    ocr_result = await self.lm_studio_client.process_image_ocr(
                        image_info["data"], 
                        f"{file.filename}_page_{image_info['page']}"
                    )
                    
                    if ocr_result["text"].strip():
                        if combined_text:
                            combined_text += f"\n\n--- Page {image_info['page']} (OCR) ---\n"
                        combined_text += ocr_result["text"]
                        confidence_scores.append(ocr_result["confidence"])
                        
                except Exception as e:
                    # Log error but continue with other pages
                    print(f"Failed to OCR page {image_info['page']}: {str(e)}")
                    continue
            
            # Calculate average confidence
            avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
            
            return {
                "text": combined_text.strip(),
                "confidence": avg_confidence,
                "file_type": "pdf",
                "pdf_info": {
                    "page_count": pdf_data["page_count"],
                    "has_extractable_text": pdf_data["has_text"],
                    "scanned_pages": len(pdf_data["images"])
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            # Provide simple error messages
            error_message = "PDF processing failed"
            if "connect" in str(e).lower() or "connection" in str(e).lower():
                error_message = "OCR service unavailable"
            elif "timeout" in str(e).lower():
                error_message = "Processing timeout"
            elif "model" in str(e).lower():
                error_message = "OCR model error"
            raise HTTPException(status_code=500, detail=error_message)
