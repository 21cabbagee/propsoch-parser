import streamlit as st
import os
from parser import extract_text_from_pdf
from google import genai

st.title("Propsoch Cost-Sheet & Risk Analyzer")
st.write("Upload a builder cost sheet or property agreement PDF to audit hidden charges and clauses.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    if st.button("Run AI Audit"):
        with st.spinner("Analyzing document for hidden traps..."):
            try:
                client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
                raw_text = extract_text_from_pdf("temp.pdf")
                
                prompt = f"""
                Analyze this real estate cost sheet. Find hidden charges, escalation clauses, and payment traps. Provide a risk breakdown.
                Text: {raw_text[:15000]}
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                st.markdown("### Audit Results")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
