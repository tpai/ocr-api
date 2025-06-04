# Product Context

## Problem Statement
Need a simple, local OCR service that can extract text from images and PDF files using a pre-trained OLM OCR model. This eliminates the need for external OCR services and provides privacy by keeping all processing local.

## User Goals
- Extract text from uploaded image files
- Extract text from uploaded PDF files
- Get results via simple REST API calls
- Process files locally without sending data to external services

## Use Cases
1. **Image OCR**: Upload JPG/PNG/other image files to extract visible text
2. **PDF OCR**: Upload PDF files to extract text content (especially from scanned PDFs)
3. **Batch Processing**: Process multiple files through API calls

## Value Proposition
- **Privacy**: All processing happens locally
- **Speed**: No network latency from external services
- **Cost**: No per-request charges from cloud OCR services
- **Reliability**: No dependency on external service availability

## User Experience Goals
- Simple HTTP POST endpoint for file uploads
- JSON response with extracted text
- Clear error messages for unsupported files
- Fast processing times
- Minimal setup required

## Technical Context
The RolmOCR model is specifically designed for OCR tasks and should provide good accuracy for both printed and handwritten text recognition.
