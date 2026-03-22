import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
API_KEY = "AIzaSyA1eARd71h_2xB4HB2TVMCPLd1_dwxfvdE" 
genai.configure(api_key=API_KEY)

# 2. Model Setup
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. User Interface (UI)
st.set_page_config(page_title="ECE Math AI", page_icon="🔢")
st.title("🔢 AI Math to LaTeX Converter")
st.subheader("3rd Year ECE - Mini Project")

# File Upload Section
uploaded_file = st.file_uploader("Upload Math Image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Equation", use_container_width=True)
    
    if st.button('🚀 Convert Now'):
        with st.spinner('Analyzing mathematical structure...'):
            try:
                # Instruction to AI
                prompt = "Convert the mathematical expression in the image to LaTeX code. Output ONLY the LaTeX code starting and ending with $$."
                response = model.generate_content([prompt, img])
                
                # Cleaning output
                latex_out = response.text.replace("```latex", "").replace("```", "").strip()

                st.success("Conversion Successful!")
                # Rendering for the user
                st.latex(latex_out)
                # Showing code for the report
                st.code(latex_out, language='latex')
            except Exception as e:
                st.error(f"Cloud Error: {e}")
