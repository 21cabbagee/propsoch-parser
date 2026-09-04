import os
from google import genai
import pdfplumber

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def analyze_cost_sheet(pdf_path):
    print("Extracting text from document...")
    raw_text = extract_text_from_pdf(pdf_path)
    
    print("Analyzing with Gemini...")
    prompt = f"""
    You are an expert real estate auditor and consumer advocate. Analyze the following real estate builder cost-sheet or property agreement text. 
    Identify and extract:
    1. **Hidden or Additional Charges:** (e.g., PLC, maintenance deposits, club membership, legal charges, corpus fund).
    2. **Escalation Clauses:** Any clauses allowing the builder to increase prices unilaterally.
    3. **Payment Schedule Traps:** Construction-linked vs. time-linked plan anomalies or heavy front-loaded payments.
    4. **Summary & Verdict:** A quick risk score (Low/Medium/High) for the homebuyer.

    Document Text:
    {raw_text[:15000]}
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text
