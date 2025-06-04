"""
Test script for OCR API Server
Run this to test the API endpoints manually
"""
import asyncio
import aiohttp
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent))

API_BASE_URL = "http://localhost:8000"

async def test_health_check():
    """Test health check endpoint"""
    print("🔍 Testing health check endpoint...")
    
    async with aiohttp.ClientSession() as session:
        # Test basic health check
        try:
            async with session.get(f"{API_BASE_URL}/") as response:
                data = await response.json()
                print(f"✅ Basic health check: {response.status} - {data}")
        except Exception as e:
            print(f"❌ Basic health check failed: {str(e)}")

async def test_ocr_with_sample_image():
    """Test OCR with a generated sample image"""
    print("\n🔍 Testing OCR with sample image...")
    
    # Create a simple test image with PIL
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a simple image with text
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font, fallback to basic if not available
        try:
            font = ImageFont.truetype("Arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = "Hello, World!\nThis is a test image for OCR.\n12345 ABCDE"
        draw.text((20, 50), text, fill='black', font=font)
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        
        # Send to API
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field('file', img_bytes.getvalue(), 
                          filename='test_image.jpg', 
                          content_type='image/jpeg')
            
            async with session.post(f"{API_BASE_URL}/ocr", data=data) as response:
                result = await response.json()
                print(f"✅ OCR test: {response.status}")
                if result.get('success'):
                    print(f"   Extracted text: '{result.get('text')}'")
                    print(f"   Confidence: {result.get('confidence')}")
                    print(f"   Processing time: {result.get('processing_time')}s")
                else:
                    print(f"   Error: {result.get('error')}")
                    
    except ImportError:
        print("❌ PIL not available for image generation test")
    except Exception as e:
        print(f"❌ OCR test failed: {str(e)}")

async def test_invalid_file():
    """Test with invalid file"""
    print("\n🔍 Testing with invalid file...")
    
    async with aiohttp.ClientSession() as session:
        # Test with a text file (unsupported format)
        text_content = b"This is just plain text, not an image or PDF"
        
        data = aiohttp.FormData()
        data.add_field('file', text_content, 
                      filename='test.txt', 
                      content_type='text/plain')
        
        try:
            async with session.post(f"{API_BASE_URL}/ocr", data=data) as response:
                result = await response.json()
                print(f"✅ Invalid file test: {response.status}")
                print(f"   Expected error: {result.get('error', 'No error message')}")
        except Exception as e:
            print(f"❌ Invalid file test failed: {str(e)}")

async def test_file_size_limit():
    """Test file size limit"""
    print("\n🔍 Testing file size limit...")
    
    try:
        # Create a large dummy file (simulating oversized image)
        large_data = b"0" * (11 * 1024 * 1024)  # 11MB (over the 10MB limit)
        
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field('file', large_data, 
                          filename='large_image.jpg', 
                          content_type='image/jpeg')
            
            async with session.post(f"{API_BASE_URL}/ocr", data=data) as response:
                result = await response.json()
                print(f"✅ File size limit test: {response.status}")
                print(f"   Expected error: {result.get('error', 'No error message')}")
                
    except Exception as e:
        print(f"❌ File size limit test failed: {str(e)}")

async def main():
    """Run all tests"""
    print("🚀 Starting OCR API Tests")
    print("=" * 50)
    print(f"Testing API at: {API_BASE_URL}")
    print("Make sure the server is running with: python main.py")
    print("=" * 50)
    
    await test_health_check()
    await test_ocr_with_sample_image()
    await test_invalid_file()
    await test_file_size_limit()
    
    print("\n" + "=" * 50)
    print("🎯 Tests completed!")
    print("\nTo test with your own files:")
    print("curl -X POST 'http://localhost:8000/ocr' -F 'file=@your_image.jpg'")

if __name__ == "__main__":
    asyncio.run(main())
