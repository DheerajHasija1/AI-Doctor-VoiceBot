# AI Doctor: Voice & Vision Medical Assistant 🏥

A multimodal AI system that combines voice interaction and medical image analysis to provide preliminary medical consultations using LLaMA-4 and Groq infrastructure.

## Key Features 🌟

- **Voice Interface**: Natural speech input/output with noise handling
- **Image Analysis**: Medical image processing using vision-language models
- **AI Diagnosis**: Powered by LLaMA-4 Scout 17B for medical analysis
- **Real-time**: Fast processing with Groq's infrastructure
- **User-friendly**: Clean Gradio UI with comprehensive displays

## Tech Stack 🛠️

- Python 3.9+, Gradio 5.34.2
- LLaMA-4, Whisper-large-v3
- Speech Recognition, PyAudio
- Google TTS/ElevenLabs
- Base64 Image Processing

## Quick Start 🚀

```bash
git clone [repository-url]
cd AI-Doctor-VoiceBot
pip install -r requirements.txt
python app.py
```

Access at: http://localhost:7860

## Flow Overview 📋

1. Voice/Image Input → 2. Speech-to-Text → 3. Image Analysis → 
4. AI Medical Processing → 5. Voice Response → 6. UI Display

## Disclaimer ⚠️

For preliminary consultation only. Not a replacement for professional medical advice.

---
*Built with Groq & Gradio*
