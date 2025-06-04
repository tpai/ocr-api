"""LM Studio client for communicating with LM Studio API"""
import aiohttp
import base64
from typing import Dict, List, Any
from src.config import Config

class LMStudioClient:
    """Client for communicating with LM Studio API"""
    
    def __init__(self, config: Config):
        self.config = config
        self.base_url = config.LM_STUDIO_BASE_URL.rstrip('/')
        self.api_key = config.LM_STUDIO_API_KEY
        self.model_name = config.LM_STUDIO_MODEL_NAME
        
    
    async def process_image_ocr(self, image_data: bytes, filename: str) -> Dict[str, Any]:
        """Process image for OCR using LM Studio"""
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare the request payload for vision model
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Please extract all text from this image. Return only the extracted text without any additional formatting or commentary."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }
            
            async with aiohttp.ClientSession() as session:
                headers = self._get_headers()
                headers["Content-Type"] = "application/json"
                
                async with session.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        # Extract text from response
                        if "choices" in result and len(result["choices"]) > 0:
                            extracted_text = result["choices"][0]["message"]["content"].strip()
                            
                            return {
                                "text": extracted_text,
                                "confidence": 0.9,  # Default confidence for now
                                "model_used": self.model_name
                            }
                        else:
                            raise Exception("No response from model")
                    else:
                        error_text = await response.text()
                        raise Exception(f"LM Studio API error: HTTP {response.status} - {error_text}")
                        
        except Exception as e:
            raise Exception(f"OCR processing failed: {str(e)}")
    
    async def process_text_ocr(self, text_content: str) -> Dict[str, Any]:
        """Process text content that was pre-extracted from PDF"""
        try:
            # For PDFs that already have text, we might want to clean it up
            # using the model, or just return it as-is
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": f"Please clean up and format this extracted text, removing any unnecessary whitespace or formatting artifacts while preserving the original meaning:\n\n{text_content}"
                    }
                ],
                "temperature": 0.1,
                "max_tokens": 2000
            }
            
            async with aiohttp.ClientSession() as session:
                headers = self._get_headers()
                headers["Content-Type"] = "application/json"
                
                async with session.post(
                    f"{self.base_url}/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        
                        if "choices" in result and len(result["choices"]) > 0:
                            cleaned_text = result["choices"][0]["message"]["content"].strip()
                            
                            return {
                                "text": cleaned_text,
                                "confidence": 0.95,  # Higher confidence for text cleanup
                                "model_used": self.model_name
                            }
                        else:
                            # Fallback to original text if model fails
                            return {
                                "text": text_content,
                                "confidence": 0.8,
                                "model_used": "fallback"
                            }
                    else:
                        # Fallback to original text if API fails
                        return {
                            "text": text_content,
                            "confidence": 0.8,
                            "model_used": "fallback"
                        }
                        
        except Exception:
            # Fallback to original text if processing fails
            return {
                "text": text_content,
                "confidence": 0.8,
                "model_used": "fallback"
            }
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests"""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
