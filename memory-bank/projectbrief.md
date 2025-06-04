# OCR API Server Project Brief

## Project Overview
Create a simple API server that loads a local OLM OCR model and provides OCR capabilities for images and PDF files.

## Core Requirements
- Load local olmocr model from LM Studio
- API endpoints to analyze:
  - Image files (common formats: PNG, JPG, JPEG, etc.)
  - PDF files
- Simple REST API interface
- Return extracted text from uploaded files

## Technical Constraints
- Model location: LM Studio local installation
- Must be locally hosted
- Simple implementation preferred

## Success Criteria
- Server successfully loads the OCR model
- API accepts file uploads (images and PDFs)
- Returns accurate text extraction
- Basic error handling for unsupported files
- Clean, maintainable code structure

## Out of Scope
- Complex authentication
- Database storage
- Advanced image preprocessing
- Batch processing
- Web UI (API only)
