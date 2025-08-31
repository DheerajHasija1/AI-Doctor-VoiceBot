#Step1a: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False,
        tld='com'  # Added for stability
    )
    audioobj.save(output_filepath)
    print(f"File created: {output_filepath}, Size: {os.path.getsize(output_filepath)} bytes")


input_text="Hi this is Dheeraj   what up"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1b: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY=os.environ.get("ELEVEN_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.text_to_speech.convert(
        text=input_text,
        voice_id="pNInz6obpgDQGcFmaJgB",  # Aria voice ID
        output_format="mp3_22050_32",
        model_id="eleven_turbo_v2"
    )
    
    with open(output_filepath, 'wb') as f:
        for chunk in audio:
            f.write(chunk)
    print(f"ElevenLabs file created: {output_filepath}")

# text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3")



#Step2: Use Model for Text output to Voice

import subprocess
import platform
import time

# FIXED gTTS function with BLOCKING AUTO-PLAY + return path for UI
def text_to_speech_with_gtts(input_text, output_filepath):
    language="en"
    
    # Create audio object
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False,
        tld='com'  # Added for stability
    )
    
    # Save the file
    audioobj.save(output_filepath)
    print(f"File created: {output_filepath}, Size: {os.path.getsize(output_filepath)} bytes")
    
    # IMPORTANT: Wait for file to be completely written
    time.sleep(1.0)
    
    # Calculate audio duration for proper wait time
    from pydub import AudioSegment
    try:
        audio_segment = AudioSegment.from_mp3(output_filepath)
        duration_seconds = len(audio_segment) / 1000.0  # Convert to seconds
        print(f"Audio duration: {duration_seconds} seconds")
    except:
        duration_seconds = 10  # Default fallback
    
    # AUTO-PLAY the audio (BLOCKING - wait for complete playback)
    os_name = platform.system()
    try:
        print("🎵 Starting auto-play...")
        if os_name == "Windows":  # Windows
            subprocess.run(['powershell', '-c', f'Add-Type -AssemblyName presentationCore; $mediaPlayer = New-Object system.windows.media.mediaplayer; $mediaPlayer.open([uri]"{os.path.abspath(output_filepath)}"); $mediaPlayer.Play(); Start-Sleep {int(duration_seconds + 2)}'], shell=True)
        else:
            print("Unsupported operating system for auto-play")
            time.sleep(duration_seconds)  # Manual wait
        print("✅ Auto-play completed!")
    except Exception as e:
        print(f"Auto-play error occurred: {e}")
        time.sleep(duration_seconds)  # Fallback wait
    
    # Return file path for Gradio UI control
    return output_filepath


input_text="Hi this is Ai with Hassan, autoplay testing!"
# text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


# FIXED ElevenLabs function with BLOCKING AUTO-PLAY + return path for UI  
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    try:
        client = ElevenLabs(api_key=os.environ.get("ELEVEN_API_KEY"))
        
        # Generate audio
        audio = client.text_to_speech.convert(
            text=input_text,
            voice_id="pNInz6obpgDQGcFmaJgB",  # Aria voice ID
            output_format="mp3_22050_32",
            model_id="eleven_turbo_v2"
        )
        
        # Save audio
        elevenlabs.save(audio, output_filepath)
        print(f"ElevenLabs file created: {output_filepath}")
        
        # IMPORTANT: Wait for file to be completely written
        time.sleep(1.5)
        
        # Calculate audio duration for proper wait time
        from pydub import AudioSegment
        try:
            audio_segment = AudioSegment.from_mp3(output_filepath)
            duration_seconds = len(audio_segment) / 1000.0  # Convert to seconds
            print(f"Audio duration: {duration_seconds} seconds")
        except:
            duration_seconds = 10  # Default fallback
        
        # AUTO-PLAY the audio (BLOCKING - wait for complete playback)
        os_name = platform.system()
        try:
            print("🎵 Starting ElevenLabs auto-play...")
            if os_name == "Windows":  # Windows
                subprocess.run(['powershell', '-c', f'Add-Type -AssemblyName presentationCore; $mediaPlayer = New-Object system.windows.media.mediaplayer; $mediaPlayer.open([uri]"{os.path.abspath(output_filepath)}"); $mediaPlayer.Play(); Start-Sleep {int(duration_seconds + 2)}'], shell=True)
            else:
                print("Unsupported operating system for auto-play")
                time.sleep(duration_seconds)  # Manual wait
            print("✅ ElevenLabs auto-play completed!")
        except Exception as e:
            print(f"Auto-play error occurred: {e}")
            time.sleep(duration_seconds)  # Fallback wait
            
        # Return file path for Gradio UI control
        return output_filepath
            
    except Exception as e:
        print(f"ElevenLabs error: {e}")
        return None
