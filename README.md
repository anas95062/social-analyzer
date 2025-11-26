# Social Media Content Analyzer

## Description
An AI-powered tool that analyzes social media posts (PDF/Image) and provides engagement strategies using Google Gemini and OCR.

## Setup Instructions
1. Clone the repository.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Install Tesseract OCR on your machine.
4. Create a `.env` file and add your API key:
   `GEMINI_API_KEY=your_key_here`
5. Run the app:
   `uvicorn main:app --reload`