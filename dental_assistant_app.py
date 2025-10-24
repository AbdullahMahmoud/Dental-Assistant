import streamlit as st
import base64
import io
from PIL import Image
import requests
from openai import OpenAI
import json

# Configure page
st.set_page_config(
    page_title="🦷 AI Dental Assistant",
    page_icon="🦷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .main-header p {
        color: #f0f0f0;
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
    }
    
    .upload-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px dashed #dee2e6;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .analysis-section {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )

# Initialize session state
if 'current_image' not in st.session_state:
    st.session_state.current_image = None
if 'image_analysis' not in st.session_state:
    st.session_state.image_analysis = None

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def analyze_dental_image(image, client):
    """Analyze dental image using OpenAI API"""
    try:
        # Convert image to base64
        img_base64 = encode_image_to_base64(image)
        
        # Create the analysis prompt
        analysis_prompt = """You are a professional dental assistant AI designed to analyze dental images and provide preliminary assessments. Please carefully examine the provided dental/teeth image and provide a comprehensive analysis following this structure:

**DENTAL ANALYSIS REPORT**

1. **VISUAL ASSESSMENT:**
   - Describe what you can observe in the image (teeth condition, gums, overall oral health appearance)
   - Note any visible abnormalities, discolorations, or concerning areas

2. **POTENTIAL ISSUES IDENTIFIED:**
   - List any dental problems you can identify (cavities, gum disease, tooth decay, misalignment, etc.)
   - Rate the severity of each issue (mild, moderate, severe)
   - Note any signs of infection, inflammation, or damage

3. **IMMEDIATE CONCERNS:**
   - Highlight any urgent issues that require immediate dental attention
   - Flag any signs of serious conditions (abscesses, severe decay, etc.)

4. **RECOMMENDATIONS:**
   - Suggest appropriate at-home care measures
   - Recommend over-the-counter treatments if applicable
   - Provide oral hygiene advice specific to the observed conditions

5. **DENTIST REFERRAL:**
   - Clearly state whether a dentist visit is recommended
   - If yes, specify the urgency level (routine, soon, urgent, emergency)
   - Suggest what type of dental specialist might be needed

6. **FOLLOW-UP CARE:**
   - Recommend timeline for re-evaluation
   - Suggest preventive measures to avoid future issues

**IMPORTANT DISCLAIMERS:**
- This is a preliminary assessment only and cannot replace professional dental examination
- Always consult with a licensed dentist for definitive diagnosis and treatment
- In case of severe pain, swelling, or emergency symptoms, seek immediate dental care
- This analysis is based on visual assessment only and may not detect all underlying issues

Please provide your analysis in a clear, professional, and easy-to-understand format."""

        # Make API call
        completion = client.chat.completions.create(
            model="qwen/qwen2.5-vl-32b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": analysis_prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": img_base64
                            }
                        }
                    ]
                }
            ]
        )
        
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}"

# Main app layout
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🦷 AI Dental Assistant</h1>
        <p>Professional dental image analysis and oral health guidance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📋 Quick Actions")
        
        if st.button("🔄 Clear Analysis", width='stretch'):
            st.session_state.current_image = None
            st.session_state.image_analysis = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This AI dental assistant can:
        - Analyze dental images
        - Identify potential issues
        - Provide treatment recommendations
        - Suggest when to see a dentist
        """)
        
        st.markdown("### ⚠️ Important")
        st.markdown("""
        This is a preliminary assessment tool only. Always consult with a licensed dentist for definitive diagnosis and treatment.
        """)
    
    # Main content area - Image Upload and Analysis
    st.markdown("### 📸 Upload Dental Image")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a dental image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image of teeth for analysis"
    )
    
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width='stretch')
        
        # Store current image in session state
        st.session_state.current_image = image
        
        # Analyze button
        if st.button("🔍 Analyze Image", width='stretch'):
            with st.spinner("Analyzing your dental image..."):
                client = get_openai_client()
                analysis = analyze_dental_image(image, client)
                st.session_state.image_analysis = analysis
            
            st.success("Analysis complete!")
            st.rerun()
    
    # Analysis results section
    if st.session_state.image_analysis:
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")
        
        with st.expander("View Full Analysis Report", expanded=True):
            st.markdown(st.session_state.image_analysis)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p><strong>🦷 AI Dental Assistant</strong> - Professional dental image analysis</p>
        <p><em>Remember: This tool provides preliminary assessments only. Always consult with a licensed dentist for definitive diagnosis and treatment.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":

    main()
