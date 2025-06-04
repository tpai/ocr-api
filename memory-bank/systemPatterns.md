# System Patterns

## Architecture Overview
Simple monolithic API server with the following components:
- **Model Manager**: Loads and manages the RolmOCR model
- **File Handler**: Processes uploaded files (images/PDFs)
- **OCR Service**: Coordinates between file processing and model inference
- **API Layer**: FastAPI endpoints for external interface

## Key Design Patterns

### Model Loading Pattern
- Singleton pattern for model instance (load once, reuse)
- Lazy loading: model loaded on first request to optimize startup time
- Error handling for model loading failures

### File Processing Pattern
- Strategy pattern for different file types (Image vs PDF)
- Temporary file handling with cleanup
- Input validation and sanitization

### API Response Pattern
```json
{
  "success": true,
  "text": "extracted text content",
  "confidence": 0.95,
  "processing_time": 1.2
}
```

Error response:
```json
{
  "success": false,
  "error": "error description",
  "code": "ERROR_CODE"
}
```

## Component Relationships
```
FastAPI Router
    ↓
File Upload Handler
    ↓
File Type Detector
    ↓ (Image)        ↓ (PDF)
Image Processor → PDF Processor
    ↓                 ↓
    OCR Service ←──────┘
    ↓
RolmOCR Model
```

## Error Handling Strategy
- Input validation at API layer
- File type validation before processing
- Model inference error handling
- Graceful degradation for unsupported formats
- Proper HTTP status codes

## Performance Considerations
- Async/await for I/O operations
- File size limits to prevent memory issues
- Model inference optimization
- Cleanup of temporary files

## Security Patterns
- File type validation (prevent malicious uploads)
- File size limits
- Input sanitization
- No file storage (process and discard)
