import sounddevice as sd
import numpy as np
import requests
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

def record_audio(duration=5, samplerate=16000):
    """Record audio from the microphone."""
    print(f"🎙️ Listening for {duration} seconds...")
    recording = sd.rec(int(duration * samplerate), 
                      samplerate=samplerate, 
                      channels=1,
                      dtype='int16')
    sd.wait()
    return recording

def save_audio(recording, filename="temp.wav"):
    """Save recording to WAV file."""
    import wave
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(recording.tobytes())
    return filename

def transcribe_with_deepgram(audio_file_path):
    """Send audio file to Deepgram API for transcription."""
    url = "https://api.deepgram.com/v1/listen?model=nova-2&punctuate=true"
    
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/wav"
    }
    
    with open(audio_file_path, 'rb') as audio_file:
        audio_data = audio_file.read()
    
    print("📄 Transcribing with Deepgram...")
    response = requests.post(url, headers=headers, data=audio_data)
    
    if response.status_code == 200:
        result = response.json()
        transcript = result['results']['channels'][0]['alternatives'][0]['transcript']
        print("📝 Text:", transcript)
        return transcript
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def record_and_transcribe(duration=5):
    try:
        # Record audio
        recording = record_audio(duration)
        
        # Save audio to temporary file
        audio_file = save_audio(recording)
        
        # Transcribe
        transcript = transcribe_with_deepgram(audio_file)
        return transcript
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        # Clean up temporary file
        if 'audio_file' in locals() and os.path.exists(audio_file):
            os.remove(audio_file)
        print("Processing complete")

if __name__ == "__main__":
    record_and_transcribe(duration=5)