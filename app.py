import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
API_KEY = "AIzaSyA1eARd71h_2xB4HB2TVMCPLd1_dwxfvdE" 
genai.configure(api_key=API_KEY)

# 2. UI Setup
st.set_page_config(page_title="ECE Math AI", page_icon="🔢")
st.title("🔢 AI Math to LaTeX Converter")
st.caption("Status: Cloud Integration Active")

# 3. Model Loading with Error Catching
try:
    # Explicitly using 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model Load Error: {e}")

uploaded_file = st.file_uploader("Upload Math Image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Image", use_container_width=True)
    
    if st.button('🚀 Convert Now'):
        with st.spinner('Processing via Google Cloud...'):
            try:
                # Direct Prompt
                response = model.generate_content([
                    "Convert this math to LaTeX. Output only the LaTeX code.", 
                    img
                ])
                
                if response.text:
                    clean_out = response.text.replace("```latex", "").replace("```", "").strip()
                    st.success("Success!")
                    st.latex(clean_out)
                    st.code(clean_out)
                else:
                    st.warning("No text detected.")
            except Exception as e:
                st.error(f"Execution Error: {e}")
                st.info("💡 Tip: Try recreating a new API Key from Google AI Studio.")
