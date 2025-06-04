"""Unit tests for configuration module"""
import pytest
import os
from unittest.mock import patch
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.config import Config

class TestConfig:
    """Test the Config class"""
    
    def test_default_values(self):
        """Test that default configuration values are set correctly"""
        config = Config()
        
        assert config.LM_STUDIO_BASE_URL == "http://localhost:1234"
        assert config.LM_STUDIO_MODEL_NAME == "nielsgl/RolmOCR-8bit"
        assert config.MAX_FILE_SIZE_MB == 10
        assert config.MAX_FILE_SIZE_BYTES == 10 * 1024 * 1024
        assert config.HOST == "0.0.0.0"
        assert config.PORT == 8000
        assert config.DEBUG == True
    
    @patch.dict(os.environ, {
        'LM_STUDIO_BASE_URL': 'http://localhost:8080',
        'MAX_FILE_SIZE_MB': '20',
        'DEBUG': 'false'
    })
    def test_environment_variables_override(self):
        """Test that environment variables override defaults"""
        config = Config()
        
        assert config.LM_STUDIO_BASE_URL == "http://localhost:8080"
        assert config.MAX_FILE_SIZE_MB == 20
        assert config.MAX_FILE_SIZE_BYTES == 20 * 1024 * 1024
        assert config.DEBUG == False
    
    def test_supported_image_formats(self):
        """Test image format validation"""
        config = Config()
        
        # Test supported formats
        assert config.is_supported_image_format("test.jpg") == True
        assert config.is_supported_image_format("test.jpeg") == True
        assert config.is_supported_image_format("test.png") == True
        assert config.is_supported_image_format("test.bmp") == True
        assert config.is_supported_image_format("test.tiff") == True
        assert config.is_supported_image_format("test.webp") == True
        
        # Test case insensitivity
        assert config.is_supported_image_format("TEST.JPG") == True
        assert config.is_supported_image_format("Test.PNG") == True
        
        # Test unsupported formats
        assert config.is_supported_image_format("test.txt") == False
        assert config.is_supported_image_format("test.doc") == False
        assert config.is_supported_image_format("test") == False
        assert config.is_supported_image_format("") == False
        assert config.is_supported_image_format(None) == False
    
    def test_pdf_file_detection(self):
        """Test PDF file detection"""
        config = Config()
        
        # Test PDF files
        assert config.is_pdf_file("document.pdf") == True
        assert config.is_pdf_file("DOCUMENT.PDF") == True
        assert config.is_pdf_file("test.pdf") == True
        
        # Test non-PDF files
        assert config.is_pdf_file("document.doc") == False
        assert config.is_pdf_file("image.jpg") == False
        assert config.is_pdf_file("") == False
        assert config.is_pdf_file(None) == False
    
    def test_supported_file_detection(self):
        """Test overall supported file detection"""
        config = Config()
        
        # Test supported files
        assert config.is_supported_file("image.jpg") == True
        assert config.is_supported_file("document.pdf") == True
        assert config.is_supported_file("photo.png") == True
        
        # Test unsupported files
        assert config.is_supported_file("document.txt") == False
        assert config.is_supported_file("video.mp4") == False
        assert config.is_supported_file("") == False
    
    def test_file_type_detection(self):
        """Test file type categorization"""
        config = Config()
        
        assert config.get_file_type("image.jpg") == "image"
        assert config.get_file_type("photo.png") == "image"
        assert config.get_file_type("document.pdf") == "pdf"
        assert config.get_file_type("file.txt") == "unsupported"
        assert config.get_file_type("") == "unsupported"
    
    @patch.dict(os.environ, {
        'SUPPORTED_IMAGE_FORMATS': 'jpg,png'
    })
    def test_custom_image_formats(self):
        """Test custom image format configuration"""
        config = Config()
        
        assert config.is_supported_image_format("test.jpg") == True
        assert config.is_supported_image_format("test.png") == True
        assert config.is_supported_image_format("test.bmp") == False
        assert config.is_supported_image_format("test.tiff") == False

if __name__ == "__main__":
    pytest.main([__file__])
