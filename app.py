import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
# Google AI Studio-la irundhu edutha PUDHU Key-ah inga podunga
API_KEY = "AIzaSyABSN1YRt2jaVcEQ8xHPjGy2_W5pOmgszw" 
genai.configure(api_key=API_KEY)

# 2. Force Version Mapping (404 Error Killer)
# Sila neram 'v1beta' mismatch aagum, adhunala namma direct path use panroam
MODEL_NAME = "models/gemini-1.5-flash"

st.set_page_config(page_title="ECE Math AI", page_icon="🔢")
st.title("🔢 AI Math to LaTeX Converter")
st.caption(f"System Status: Connected to {MODEL_NAME}")

uploaded_file = st.file_uploader("Upload Math Image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Equation", use_container_width=True)
    
    if st.button('🚀 Convert Now'):
        with st.spinner('Cloud Analysis in Progress...'):
            try:
                # Direct Initialization
                model = genai.GenerativeModel(model_name=MODEL_NAME)
                
                prompt = "Convert the mathematical expression in the image to LaTeX. Output ONLY the LaTeX code. Example: $$x^2 + y^2 = z^2$$"
                response = model.generate_content([prompt, img])
                
                if response.text:
                    clean_latex = response.text.replace("```latex", "").replace("```", "").strip()
                    st.success("Conversion Successful!")
                    st.latex(clean_latex)
                    st.code(clean_latex, language='latex')
                else:
                    st.error("AI could not read the image. Please try a clearer photo.")
            except Exception as e:
                # Indha error-la available models list varum, check pannunga
                st.error(f"Execution Error: {e}")
