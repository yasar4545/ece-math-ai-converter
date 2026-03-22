import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
API_KEY = "AIzaSyA1eARd71h_2xB4HB2TVMCPLd1_dwxfvdE" 
genai.configure(api_key=API_KEY)

# 2. DYNAMIC MODEL PICKER (To bypass 404 Error)
def get_working_model():
    try:
        # Unga API-ku permission irukura models-ah list panrom
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Priority order: Flash > Pro > First Available
        if 'models/gemini-1.5-flash' in available_models:
            return 'models/gemini-1.5-flash'
        elif 'models/gemini-pro-vision' in available_models:
            return 'models/gemini-pro-vision'
        else:
            return available_models[0]
    except:
        return "models/gemini-1.5-flash" # Default fallback

MODEL_NAME = get_working_model()

# --- UI Setup ---
st.set_page_config(page_title="ECE Precision Math AI", page_icon="🔢")
st.title("🔢 AI Math to LaTeX Converter")
st.info(f"Connected to Model: {MODEL_NAME}")

uploaded_file = st.file_uploader("Upload Math Image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Image", use_container_width=True)
    
    if st.button('🚀 Convert Now'):
        with st.spinner('Analyzing mathematical structure...'):
            try:
                model = genai.GenerativeModel(model_name=MODEL_NAME)
                prompt = "Convert this mathematical expression to LaTeX code. Output ONLY the LaTeX code starting and ending with $$."
                
                response = model.generate_content([prompt, img])
                
                if response.text:
                    latex_out = response.text.strip()
                    clean_latex = latex_out.replace("```latex", "").replace("```", "").strip()

                    st.success("Conversion Successful!")
                    st.latex(clean_latex)
                    st.code(clean_latex, language='latex')
                else:
                    st.warning("Empty response. Please try a clearer image.")
            except Exception as e:
                st.error(f"Execution Error: {e}")
