import os
import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION ---
# WINDOWS USERS: If you get a "Tesseract not found" error, uncomment the line below and update the path:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

# Mount the static directory to serve the HTML file
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# --- HELPER FUNCTIONS ---
def extract_text_from_pdf(file_bytes):
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        raise ValueError(f"PDF Error: {str(e)}")

def extract_text_from_image(file_bytes):
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # English language by default
        return pytesseract.image_to_string(image)
    except Exception as e:
        raise ValueError(f"OCR Error: {str(e)}")

# --- API ENDPOINT ---
@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}") # Debug print
    content = await file.read()
    extracted_text = ""

    try:
        # 1. Extract Text
        if file.content_type == "application/pdf":
            extracted_text = extract_text_from_pdf(content)
        elif file.content_type.startswith("image/"):
            extracted_text = extract_text_from_image(content)
        else:
            raise HTTPException(status_code=400, detail="File type not supported. Use PDF or Image.")

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text found in document. Is it empty?")

        # 2. Analyze with Gemini
        model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
        # ... inside analyze_document function ...
        
        prompt = f"""
        Act as a Senior Social Media Strategist & Copywriter. 
        Analyze the text extracted from a user's document/post below.
        
        EXTRACTED TEXT:
        "{extracted_text[:4000]}"
        
        YOUR GOAL:
        Provide a brutal yet constructive audit to maximize viral potential and engagement. 
        
        STRICT OUTPUT FORMAT (Use Markdown):
        
        ## 🎯 Target Audience Profile
        - **Who they are:** (e.g., "Corporate burnouts looking for escape," "Gen Z tech enthusiasts")
        - **What they want:** (The core desire this post addresses)

        ## 📊 Engagement Scorecard
        **Score:** [X]/10
        - **✅ What works:** (One sentence on the strong point)
        - **⚠️ The Weakness:** (One sentence on the biggest friction point)

        ## 🚀 3 High-Impact Improvements
        *(Be specific. Don't just say "be shorter," say "Cut the first paragraph.")*
        
        **1. The Hook (First 3 seconds)**
        - **Problem:** [Analyze the opening]
        - **Fix:** [Specific instruction]
        
        **2. The Structure (Readability)**
        - **Problem:** [Analyze the layout/flow]
        - **Fix:** [Specific instruction, e.g., "Use bullet points here"]
        
        **3. The Call-to-Action (CTA)**
        - **Problem:** [Analyze the ending]
        - **Fix:** [Specific instruction]

        ## ✨ "Viral Rewrite" Suggestion
        *(Rewrite the first 2 sentences of their post to be punchier and more engaging)*
        > "[Insert your rewritten hook here]"

        ## #️⃣ Hashtag Strategy
        - **Broad:** #Tag1 #Tag2
        - **Niche:** #Tag3 #Tag4 #Tag5
        """
        
        response = model.generate_content(prompt)
        
        return {
            "success": True,
            "original_text_snippet": extracted_text[:200] + "...",
            "analysis": response.text
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))