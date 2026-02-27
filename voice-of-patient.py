import os
import speech_recognition as sr  # Library to handle Microphone input
from pydub import AudioSegment     # Library to convert audio formats (WAV -> MP3)
from io import BytesIO             # Helpers to handle data in memory
from groq import Groq              # The official Groq API client
from pathlib import Path

# --- CONFIG ---
audio_filepath = "patient_voice.mp3" 
stt_model = "whisper-large-v3"       # Using Groq's version of Whisper for fast transcription

# --- FUNCTIONS ---
def record_audio(file_path):
    recognizer = sr.Recognizer()
    
    # Opens the default system microphone
    with sr.Microphone() as source:
        print("🔴 [RECORDING] Please speak now...")
        
        # IMPORTANT: Calibrates the mic to the room's background noise.
        # Without this, the recognizer might think breathing or AC noise is speech.
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Listens until it detects a pause in speech (automatic endpointing)
        audio_data = recognizer.listen(source, timeout=10)
        
        # --- CONVERSION STEP (Crucial for API efficiency) ---
        # 1. Get raw WAV data from the microphone
        wav_data = audio_data.get_wav_data()
        
        # 2. Wrap the WAV data in a BytesIO object so Pydub can read it like a file
        audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
        
        # 3. Export as MP3. 
        # Sending MP3 to the API is much faster than sending raw WAV files due to smaller size.
        audio_segment.export(file_path, format="mp3", bitrate="128k")
        
        print(f"✅ Audio saved to {file_path}")

def transcribe_with_groq(model, file_path):
    # IMPORTANT: This line automatically looks for 'GROQ_API_KEY' in your environment.
    # Ensure you have your .env file set up or the variable exported!
    client = Groq() 
    
    # Read the audio file from the disk as binary bytes (required for network upload)
    audio_data = Path(file_path).read_bytes()

    print("⚙️ AI is thinking...")
    
    # Call the Groq Audio API
    transcription = client.audio.transcriptions.create(
            model=model,
            # The 'file' argument usually expects a tuple: (filename, file_content_bytes)
            file=(file_path, audio_data),
            language="en",          # Force English for better accuracy (optional)
            response_format="text"  # Returns just the string, not a JSON object
        )
    return transcription

# --- EXECUTION ---
# 1. Record the voice and save it to 'patient_voice.mp3'
record_audio(audio_filepath)

# 2. Send that specific file to Groq for transcription
text_result = transcribe_with_groq(stt_model, audio_filepath)

print(f"PATIENT SAID: {text_result}")