# Technical Context

## Technology Stack
- **Language**: Python (recommended for ML model integration)
- **Web Framework**: FastAPI (async, automatic OpenAPI docs, file upload support)
- **ML Framework**: Likely transformers/torch for OLM model loading
- **File Processing**: PIL/Pillow for images, PyMuPDF for PDFs
- **Model**: RolmOCR-8bit (8-bit quantized version for efficiency)

## Model Information
- **Integration**: LM Studio API for model selection and inference
- **Type**: OLM (Optical Language Model) for OCR tasks
- **Selection**: Dynamic model selection via LM Studio interface
- **Communication**: HTTP API calls to LM Studio local server

## System Requirements
- **Environment**: macOS (user system)
- **Python**: 3.8+ recommended
- **Memory**: Sufficient RAM for 8-bit quantized model
- **Storage**: Local model files (~GB range typical)

## Development Setup
- Virtual environment for Python dependencies
- Package requirements likely include:
  - fastapi
  - uvicorn (ASGI server)
  - python-multipart (file uploads)
  - pillow (image processing)
  - PyMuPDF (PDF processing)
  - requests (for LM Studio API calls)
  - python-dotenv (configuration management)

## API Design
- **Endpoint**: POST /ocr
- **Input**: multipart/form-data file upload
- **Output**: JSON with extracted text
- **Supported formats**: Images (JPG, PNG, etc.), PDF files

## Constraints
- Must work with existing model at specified path
- Simple implementation preferred
- Local processing only (no external APIs)
- CPU inference acceptable for this use case

## Unknowns to Investigate
- LM Studio API endpoints and authentication
- How to send images/PDFs to LM Studio for OCR
- Model selection mechanism in LM Studio
- Response format from LM Studio OCR inference
- Required preprocessing for images/PDFs before sending to LM Studio

## LM Studio Integration
- **API Endpoint**: Typically `http://localhost:1234` (default LM Studio port)
- **Model Selection**: Via LM Studio GUI or API calls
- **Inference**: HTTP POST requests with image data
- **Configuration**: Environment variables for LM Studio connection
