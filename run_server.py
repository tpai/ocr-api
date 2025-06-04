#!/usr/bin/env python3
"""
Simple script to start the OCR API server with proper setup
"""
import os
import sys
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import fastapi
        import uvicorn
        import aiohttp
        import PIL
        import fitz
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists"""
    if not Path(".env").exists():
        print("⚠️  .env file not found")
        print("Creating .env from .env.example...")
        try:
            with open(".env.example", "r") as src:
                with open(".env", "w") as dst:
                    dst.write(src.read())
            print("✅ Created .env file")
            print("💡 You may want to edit .env with your specific settings")
        except Exception as e:
            print(f"❌ Could not create .env file: {e}")
            return False
    else:
        print("✅ .env file found")
    return True

def main():
    """Main startup function"""
    print("🚀 OCR API Server Startup")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Are you in the correct directory?")
        sys.exit(1)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check .env file
    if not check_env_file():
        sys.exit(1)
    
    print("\n📋 Pre-flight checklist:")
    print("1. ✅ Python dependencies installed")
    print("2. ✅ Configuration file ready")
    print("3. ⚠️  Make sure LM Studio is running with RolmOCR model loaded")
    print("4. ⚠️  Make sure the model name in .env matches your LM Studio model")
    
    print("\n🎯 Starting server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the server
        os.system("python main.py")
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()
