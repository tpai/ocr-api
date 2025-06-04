# OCR API Server

A simple API server that provides OCR (Optical Character Recognition) capabilities for images and PDF files using LM Studio and the RolmOCR model.

## Features

- **Image OCR**: Extract text from common image formats (JPG, PNG, BMP, TIFF, WebP)
- **PDF OCR**: Extract text from PDF files (both text-based and scanned PDFs)
- **LM Studio Integration**: Uses LM Studio for model selection and inference
- **FastAPI**: RESTful API with automatic documentation
- **File Validation**: Size limits and format validation
- **Error Handling**: Comprehensive error responses

## Prerequisites

- Python 3.8+
- LM Studio installed and running
- RolmOCR model loaded in LM Studio

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd ocr-api
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

## Configuration

Create a `.env` file based on `.env.example`:

```env
# LM Studio Configuration
LM_STUDIO_BASE_URL=http://localhost:1234
LM_STUDIO_MODEL_NAME=nielsgl/RolmOCR-8bit

# API Configuration
MAX_FILE_SIZE_MB=10
SUPPORTED_IMAGE_FORMATS=jpg,jpeg,png,bmp,tiff,webp
SUPPORTED_PDF_MAX_PAGES=50

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

## Usage

1. Start LM Studio and load the RolmOCR model
2. Start the API server:
```bash
python main.py
```

3. The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check
- `GET /` - Basic health check

### OCR Processing
- `POST /ocr` - Process uploaded file and extract text

## API Usage Examples

### Upload an image for OCR:
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@image.jpg"
```

### Upload a PDF for OCR:
```bash
curl -X POST "http://localhost:8000/ocr" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### Response Format:
```json
{
  "success": true,
  "filename": "image.jpg",
  "text": "Extracted text content",
  "confidence": 0.95,
  "processing_time": 2.1,
  "file_type": "image"
}
```

## API Documentation

Once the server is running, visit:
- Interactive API docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Testing

Run the test scripts:
```bash
# Test with sample files
python tests/test_api.py

# Test individual components
pytest tests/
```

## File Support

### Images
- Supported formats: JPG, JPEG, PNG, BMP, TIFF, WebP
- Maximum size: 10MB (configurable)
- Automatic resizing for large images

### PDFs
- Maximum pages: 50 (configurable)
- Text-based PDFs: Extract existing text
- Scanned PDFs: Convert pages to images for OCR
- Mixed PDFs: Handle both text and scanned content

## Error Handling

The API provides detailed error responses:
- 400: Invalid file format or corrupted file
- 413: File too large
- 500: Processing errors
- 503: LM Studio unavailable

## Troubleshooting

### LM Studio Connection Issues
1. Ensure LM Studio is running on the correct port (default: 1234)
2. Check that the RolmOCR model is loaded
3. Verify the model name in your configuration

### Performance Issues
1. Reduce image size or PDF page count
2. Adjust timeout settings in configuration
3. Monitor LM Studio resource usage

## Development

### Project Structure
```
ocr-api/
├── main.py              # FastAPI application
├── src/
│   ├── config.py        # Configuration management
│   ├── lm_studio_client.py  # LM Studio API client
│   ├── file_processor.py    # File processing utilities
│   └── ocr_service.py       # OCR orchestration
├── tests/               # Test scripts
├── memory-bank/         # Project documentation
└── requirements.txt     # Dependencies
```

### Adding New Features
1. Update the appropriate service class
2. Add tests in the `tests/` directory
3. Update API documentation
4. Update configuration if needed

## License

MIT License
