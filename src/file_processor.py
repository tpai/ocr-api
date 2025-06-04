"""File processing utilities for handling images and PDFs"""
import io
from typing import Dict, Any
from fastapi import UploadFile, HTTPException
from PIL import Image
import fitz  # PyMuPDF
from src.config import Config

class FileProcessor:
    """Handles processing of uploaded files (images and PDFs)"""
    
    def __init__(self, config: Config):
        self.config = config
    
    async def validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file"""
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        if not self.config.is_supported_file(file.filename):
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type. Supported formats: {', '.join(self.config.SUPPORTED_IMAGE_FORMATS)}, pdf"
            )
        
        # Check file size (FastAPI provides content-length if available)
        if hasattr(file, 'size') and file.size and file.size > self.config.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413, 
                detail=f"File too large. Maximum size: {self.config.MAX_FILE_SIZE_MB}MB"
            )
    
    async def process_image(self, file: UploadFile) -> Dict[str, Any]:
        """Process image file and return image data"""
        try:
            # Read file content
            content = await file.read()
            
            # Validate file size after reading
            if len(content) > self.config.MAX_FILE_SIZE_BYTES:
                raise HTTPException(
                    status_code=413, 
                    detail=f"File too large. Maximum size: {self.config.MAX_FILE_SIZE_MB}MB"
                )
            
            # Validate that it's actually an image
            try:
                with Image.open(io.BytesIO(content)) as img:
                    # Convert to RGB if necessary (for JPEG compatibility)
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')
                    
                    # Resize if image is too large (optional optimization)
                    max_dimension = 2048
                    if max(img.size) > max_dimension:
                        img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
                    
                    # Save processed image to bytes
                    output_buffer = io.BytesIO()
                    img.save(output_buffer, format='JPEG', quality=85)
                    processed_content = output_buffer.getvalue()
                    
                    return {
                        "data": processed_content,
                        "format": img.format or "JPEG",
                        "size": img.size,
                        "mode": img.mode
                    }
                    
            except Exception as e:
                raise HTTPException(status_code=400, detail=f"Invalid image file: {str(e)}")
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    async def process_pdf(self, file: UploadFile) -> Dict[str, Any]:
        """Process PDF file and extract text/images"""
        try:
            # Read file content
            content = await file.read()
            
            # Validate file size
            if len(content) > self.config.MAX_FILE_SIZE_BYTES:
                raise HTTPException(
                    status_code=413, 
                    detail=f"File too large. Maximum size: {self.config.MAX_FILE_SIZE_MB}MB"
                )
            
            # Process PDF
            with fitz.open(stream=content, filetype="pdf") as pdf_doc:
                if len(pdf_doc) > self.config.SUPPORTED_PDF_MAX_PAGES:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"PDF too long. Maximum pages: {self.config.SUPPORTED_PDF_MAX_PAGES}"
                    )
                
                # Try to extract text first (for text-based PDFs)
                text_content = ""
                images = []
                
                for page_num in range(len(pdf_doc)):
                    page = pdf_doc[page_num]
                    
                    # Extract text
                    page_text = page.get_text().strip()
                    if page_text:
                        text_content += f"\n--- Page {page_num + 1} ---\n{page_text}"
                    
                    # If no text found, convert page to image for OCR
                    if not page_text:
                        # Render page as image
                        mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
                        pix = page.get_pixmap(matrix=mat)
                        img_data = pix.tobytes("jpeg")
                        
                        images.append({
                            "page": page_num + 1,
                            "data": img_data
                        })
                
                return {
                    "text_content": text_content.strip(),
                    "images": images,
                    "page_count": len(pdf_doc),
                    "has_text": bool(text_content.strip())
                }
                
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    async def get_file_info(self, file: UploadFile) -> Dict[str, Any]:
        """Get basic information about the file"""
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_type": self.config.get_file_type(file.filename or ""),
            "size": getattr(file, 'size', None)
        }
