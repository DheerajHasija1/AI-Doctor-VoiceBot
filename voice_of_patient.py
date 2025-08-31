# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup Audio recorder (ffmpeg & portaudio)
# ffmpeg, portaudio, pyaudio
import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Simplified function to record audio from the microphone and save it as an MP3 file.
    Args:
    file_path (str): Path to save the recorded audio file.
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    """
    recognizer = sr.Recognizer()
    
    # Adjust settings for better performance
    recognizer.energy_threshold = 200  # More sensitive
    recognizer.pause_threshold = 1.0   # 1 second pause (original setting)
    
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=2)  # Longer calibration
            logging.info(f"Energy threshold set to: {recognizer.energy_threshold}")
            logging.info("Start speaking now... ")
            
            # Record the audio
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            # Convert the recorded audio to an MP3 file
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

#Step2: Setup Speech to text–STT–model for transcription
import os
from groq import Groq   

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3"

def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    client = Groq(api_key=GROQ_API_KEY)
    
    with open(audio_filepath, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model=stt_model,
            file=audio_file,
            language="en"
        )
    return transcription.text

# Main execution
audio_filepath = "patient_voice_test_for_patient.mp3"

# Record audio - use original simple settings
record_audio(file_path=audio_filepath, timeout=15, phrase_time_limit=None)

# Transcribe audio
transcription_text = transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
print("Transcription:")
print(transcription_text)