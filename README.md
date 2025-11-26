# 🚀 Social Media Content Analyzer

An AI-powered web application that analyzes social media drafts (PDFs, Images, and Screenshots) to predict engagement, identify target audiences, and suggest viral improvements.

Built with **FastAPI** (Python), **Google Gemini AI**, and **Tesseract OCR**.

---

## 📋 Features
* **Multi-Format Support:** Drag & drop support for PDF documents and Image files (PNG, JPG, Screenshots).
* **OCR Integration:** Automatically extracts text from scanned documents and images using Tesseract.
* **AI Analysis:** Uses Google Gemini (Flash 2.5) to audit content.
* **Actionable Insights:** Generates a structured report including:
    * 🎯 Target Audience Profile
    * 📊 Engagement Scorecard (1-10)
    * 🚀 High-Impact Improvements
    * ✨ "Viral Rewrite" of the hook
    * #️⃣ Strategic Hashtags

---

## 🛠️ Prerequisites

Before running the project, you must have the following installed on your machine:

1.  **Python 3.10+**
2.  **Tesseract OCR** (Required for processing images)
    * **Windows:** [Download Installer (UB-Mannheim)](https://github.com/UB-Mannheim/tesseract/wiki)
        * *Important:* Note the installation path (usually `C:\Program Files\Tesseract-OCR`).
    * **macOS:** `brew install tesseract`
    * **Linux:** `sudo apt-get install tesseract-ocr`

---

## ⚙️ Installation & Setup

Follow these steps to get the project running locally.

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/social-media-analyzer.git](https://github.com/YOUR_USERNAME/social-media-analyzer.git)
cd social-media-analyzer

### 2. Create a Virtual Environment
It is recommended to run this project in a virtual environment to keep dependencies clean.

Windows:

Bash

python -m venv venv
venv\Scripts\activate
macOS / Linux:

Bash

python3 -m venv venv
source venv/bin/activate
### 3. Install Python Dependencies
Bash

pip install -r requirements.txt
### 4. Configure API Keys
Get a free Gemini API Key from Google AI Studio.

Create a file named .env in the root directory.

Add your key to the file:

Code snippet

GEMINI_API_KEY=your_actual_api_key_here
🚀 Running the Application
Start the local server:

Bash

uvicorn main:app --reload
Open your browser and navigate to:

[http://127.0.0.1:8000](http://127.0.0.1:8000)
Upload a file to see the analysis!