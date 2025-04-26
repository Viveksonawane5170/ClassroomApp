import os
import requests
from dotenv import load_dotenv
import tempfile
import sys
from moviepy import VideoFileClip

# Load environment variables
load_dotenv()
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

def extract_audio(video_path):
    """Extract audio using moviepy (no ffmpeg required)"""
    try:
        temp_audio = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_audio.close()
        
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(temp_audio.name, fps=16000, codec='pcm_s16le')
        return temp_audio.name
    except Exception as e:
        print(f"Error extracting audio: {str(e)}")
        return None

def transcribe_with_deepgram(audio_file_path):
    """Send audio to Deepgram API"""
    url = "https://api.deepgram.com/v1/listen?model=nova-2&punctuate=true"
    headers = {"Authorization": f"Token {DEEPGRAM_API_KEY}"}
    
    try:
        with open(audio_file_path, 'rb') as f:
            response = requests.post(url, headers=headers, data=f)
            if response.status_code == 200:
                return response.json()['results']['channels'][0]['alternatives'][0]['transcript']
            print(f"API Error: {response.text}")
            return None
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None

def main():
    if not DEEPGRAM_API_KEY:
        print("Missing Deepgram API key in .env file")
        return

    video_path = input("Enter video file path: ").strip('"')
    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        return

    audio_file = extract_audio(video_path)
    if not audio_file:
        return

    transcript = transcribe_with_deepgram(audio_file)
    
    
    os.unlink(audio_file)  # Clean up

    from groq import Groq

    client = Groq()

    # The text you want to summarize
    input_text = transcript
    if not input_text:
        print("No text to summarize.")
        return

    completion = client.chat.completions.create(
        model="llama3-70b-8192",  # Updated model name
        messages=[
            {
                "role": "user",
                "content": f"Please provide a brief summary of the following text:\n\n{input_text}. Also at the end give this was from which subject for example: Biology, Chemistry, etc."
            }
        ],
        temperature=0.3,  # Lower temperature for more focused summaries
        max_tokens=1024,
        top_p=1,
        stream=False,  # No need to stream for summaries
        stop=None,
    )

    print(completion.choices[0].message.content)



if __name__ == "__main__":
    main()