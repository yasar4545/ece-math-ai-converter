import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
API_KEY = "AIzaSyA1eARd71h_2xB4HB2TVMCPLd1_dwxfvdE" 
genai.configure(api_key=API_KEY)

# 2. UNIVERSAL STABLE MODEL NAME (Fixes 404 Error)
# 'gemini-1.5-flash' nu verum name mattum kudutha sila neram v1beta error varum
# Athunaala 'models/gemini-1.5-flash' nu full path kudukuroam
MODEL_NAME = "models/gemini-1.5-flash"

st.set_page_config(page_title="ECE Precision Math AI", page_icon="🔢")
st.title("🔢 AI Math to LaTeX Converter")
st.subheader("3rd Year ECE - Mini Project")

uploaded_file = st.file_uploader("Upload Math Image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Image", use_container_width=True)
    
    if st.button('🚀 Convert Now'):
        with st.spinner('Analyzing mathematical structure...'):
            try:
                # Initializing model with the full path
                model = genai.GenerativeModel(model_name=MODEL_NAME)
                
                prompt = "Convert this mathematical expression to LaTeX code. Output ONLY the LaTeX code starting and ending with $$."
                response = model.generate_content([prompt, img])
                
                if response.text:
                    latex_out = response.text.strip()
                    # Clean markdown formatting
                    clean_latex = latex_out.replace("```latex", "").replace("```", "").strip()

                    st.success("Conversion Successful!")
                    st.markdown("#### Rendered Formula:")
                    st.latex(clean_latex)
                    st.markdown("#### LaTeX Code:")
                    st.code(clean_latex, language='latex')
                else:
                    st.error("AI returned empty result. Please try a clearer photo.")
                    
            except Exception as e:
                # Intha error message-la available models list varum, check pannunga
                st.error(f"Cloud Error: {e}")
