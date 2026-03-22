import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Configuration
# Google AI Studio-la irundhu edutha PUDHU Key-ah inga podunga
API_KEY = "AIzaSyABSN1YRt2jaVcEQ8xHPjGy2_W5pOmgszw" 
genai.configure(api_key=API_KEY)

# 2. Stable Model Setup (Explicitly naming the latest version)
# 'models/gemini-1.5-flash' badhila 'gemini-1.5-flash' nu direct-ah try panrom
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Model Load Error: {e}")

# --- UI Setup ---
st.set_page_config(page_title="ECE Math AI", page_icon="🔢")
st.title("🔢 AI Math to LaTeX Converter")
st.caption("Status: Cloud Integration Active (Stable)")

uploaded_file = st.file_uploader("Upload Math Image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Image", use_container_width=True)
    
    if st.button('🚀 Convert Now'):
        with st.spinner('Processing via Google Cloud...'):
            try:
                # Engineering Prompt
                prompt = "Convert this mathematical expression to LaTeX code. Output ONLY the LaTeX code. Do not include markdown blocks."
                
                # Using generation_config for extra stability
                response = model.generate_content([prompt, img])
                
                if response.text:
                    clean_latex = response.text.replace("$$", "").strip()
                    st.success("Conversion Successful!")
                    
                    st.markdown("#### Rendered Formula:")
                    st.latex(clean_latex)
                    
                    st.markdown("#### LaTeX Code (Copy for Report):")
                    st.code(clean_latex, language='latex')
                else:
                    st.warning("AI could not detect any math. Try a clearer photo.")
            except Exception as e:
                # Indha error message-la dhaan unga API-ku endha models support aagum-nu list varum
                st.error(f"Execution Error: {e}")
                st.info("💡 Tip: If 404 persists, please check if your API Key is from 'Google AI Studio'.")
