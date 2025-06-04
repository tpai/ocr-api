"""Configuration management for OCR API Server"""
import os


class Config:
    """Configuration class that loads settings from environment variables"""
    
    def __init__(self):
        # LM Studio Configuration
        self.LM_STUDIO_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234")
        self.LM_STUDIO_API_KEY = os.getenv("LM_STUDIO_API_KEY", "")
        self.LM_STUDIO_MODEL_NAME = os.getenv("LM_STUDIO_MODEL_NAME", "nielsgl/RolmOCR-8bit")
        
        # API Configuration
        self.MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
        self.MAX_FILE_SIZE_BYTES = self.MAX_FILE_SIZE_MB * 1024 * 1024
        
        # Supported file formats
        image_formats_str = os.getenv("SUPPORTED_IMAGE_FORMATS", "jpg,jpeg,png,bmp,tiff,webp")
        self.SUPPORTED_IMAGE_FORMATS = [fmt.strip().lower() for fmt in image_formats_str.split(",")]
        
        self.SUPPORTED_PDF_MAX_PAGES = int(os.getenv("SUPPORTED_PDF_MAX_PAGES", "50"))
        
        # Server Configuration
        self.HOST = os.getenv("HOST", "0.0.0.0")
        self.PORT = int(os.getenv("PORT", "8000"))
        self.DEBUG = os.getenv("DEBUG", "true").lower() == "true"
    
    def is_supported_image_format(self, filename: str) -> bool:
        """Check if the file extension is a supported image format"""
        if not filename:
            return False
        
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        return extension in self.SUPPORTED_IMAGE_FORMATS
    
    def is_pdf_file(self, filename: str) -> bool:
        """Check if the file is a PDF"""
        if not filename:
            return False
        
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        return extension == 'pdf'
    
    def is_supported_file(self, filename: str) -> bool:
        """Check if the file is supported (image or PDF)"""
        return self.is_supported_image_format(filename) or self.is_pdf_file(filename)
    
    def get_file_type(self, filename: str) -> str:
        """Get the file type category"""
        if self.is_supported_image_format(filename):
            return "image"
        elif self.is_pdf_file(filename):
            return "pdf"
        else:
            return "unsupported"
