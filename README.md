# 🦷 AI Dental Assistant

A professional Streamlit application that uses AI to analyze dental images and provide preliminary oral health assessments.

🌐 **Live Demo**: [https://dental-assistant.streamlit.app/](https://dental-assistant.streamlit.app/)

## Features

- **Image Upload & Analysis**: Upload dental images for AI-powered analysis
- **Comprehensive Reports**: Get detailed dental assessments with visual observations, issue identification, and recommendations
- **Professional UI**: Clean, modern interface with medical-grade styling
- **Session Management**: Clear analysis and start new sessions
- **Safety Disclaimers**: Clear warnings about consulting licensed dentists

## Installation

1. Clone or download the project files
2. Create a conda environment with Python 3.10:
   ```bash
   conda create -n dental-assistant python=3.10
   conda activate dental-assistant
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run dental_assistant_app.py
   ```

2. Open your browser to the provided local URL (usually `http://localhost:8501`)

3. Upload a dental image using the file uploader

4. Click "Analyze Image" to get a comprehensive dental assessment

5. View the detailed analysis report with all recommendations

## How It Works

1. **Image Analysis**: The app uses OpenAI's vision model to analyze uploaded dental images
2. **Structured Reports**: Provides detailed analysis in 6 key areas:
   - Visual Assessment
   - Potential Issues Identified
   - Immediate Concerns
   - Recommendations
   - Dentist Referral
   - Follow-up Care

3. **Professional Reports**: Get comprehensive dental assessments with clear recommendations

## Important Disclaimers

⚠️ **This application provides preliminary assessments only and cannot replace professional dental examination.**

- Always consult with a licensed dentist for definitive diagnosis and treatment
- In case of severe pain, swelling, or emergency symptoms, seek immediate dental care
- This analysis is based on visual assessment only and may not detect all underlying issues

## Technical Details

- **Framework**: Streamlit
- **AI Model**: Qwen2.5-VL (via OpenRouter)
- **Image Processing**: PIL/Pillow
- **API**: OpenAI-compatible API

## File Structure

```
├── dental_assistant_app.py    # Main Streamlit application
├── app.py                     # Original OpenAI API code
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Customization

You can modify the analysis prompt in the `analyze_dental_image()` function to adjust the type of analysis provided. The app is designed to be easily customizable for different dental analysis needs.

