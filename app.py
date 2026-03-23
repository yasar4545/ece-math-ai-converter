import streamlit as st
import google.generativeai as genai
from PIL import Image
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
else:
    st.error("API Key not found in Secrets! Please add it in Streamlit Settings.")

genai.configure(api_key=API_KEY)

@st.cache_resource
def load_working_model():
    try:
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if 'models/gemini-1.5-flash' in models: return 'models/gemini-1.5-flash'
        if 'models/gemini-1.5-pro' in models: return 'models/gemini-1.5-pro'
        return models[0]
    except:
        return "models/gemini-1.5-flash"

SELECTED_MODEL = load_working_model()

st.set_page_config(page_title="ECE Math AI", page_icon="🔢")
st.title("🔢 AI Math to LaTeX Converter")
st.info(f"System Connected to: {SELECTED_MODEL}")

uploaded_file = st.file_uploader("Upload Math Image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Input Equation", use_container_width=True)
    
    if st.button('🚀 Convert Now'):
        with st.spinner('Analyzing mathematical structure...'):
            try:
                model = genai.GenerativeModel(SELECTED_MODEL)
                prompt = "Convert the math in this image to LaTeX code. Output ONLY LaTeX starting and ending with $$."
                response = model.generate_content([prompt, img])
                
                if response.text:
                    clean_latex = response.text.replace("```latex", "").replace("```", "").strip()
                    st.success("Conversion Successful!")
                    st.latex(clean_latex)
                    st.code(clean_latex)
                else:
                    st.error("AI returned empty result.")
            except Exception as e:
                st.error(f"Execution Error: {e}")
