 #Step1a: Setup Text to Speech–TTS–model with gTTS

import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text="Hi this is Ai with sanjeev!"
output_filepath="gtts_testing.mp3"
print(f"✅ Success! Audio saved to: {output_filepath}")
text_to_speech_with_gtts_old(input_text=input_text, output_filepath=output_filepath)



# #Step1b: Setup Text to Speech–TTS–model with ElevenLabs

import os
from elevenlabs.client import ElevenLabs

# Use the environment variable loaded by Pipenv
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs_fixed(input_text, output_filepath):
    # Initialize the client
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    
    # This replaces the old client.generate()
    audio_stream = client.text_to_speech.convert(
        text=input_text,
        voice_id="FGY2WhTYpPnrIDTdsKH5",  # Replace with your desired voice ID
        model_id="eleven_multilingual_v2", # This works here!
        output_format="mp3_44100_128"
    )
    
    # Save the file correctly (iterating through the generator)
    with open(output_filepath, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
                
    print(f"✅ Success! Audio saved to: {output_filepath}")
text_to_speech_with_elevenlabs_fixed(input_text, "elevenlabs_testing.mp3")


#Step2a: Use gtts Model for Text output to Voice
import os
from gtts import gTTS
from playsound import playsound

def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    print(f"✅ Success! Audio saved to: {output_filepath}")
    
    # Autoplay the audio
    playsound(output_filepath)

# Test
text_to_speech_with_gtts("Hi this is AI with Sanjeev!", "gtts_testing_autoplay.mp3")

# step 2b: Use ElevenLabs for Text to Speech with Autoplay
import os
from elevenlabs.client import ElevenLabs
from playsound import playsound

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio_stream = client.text_to_speech.convert(
        text=input_text,
        voice_id="FGY2WhTYpPnrIDTdsKH5",  # Replace with your desired voice ID
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128"
    )
    with open(output_filepath, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
    print(f"✅ Success! Audio saved to: {output_filepath}")
    
    # Autoplay the audio
    playsound(output_filepath)

# Test
text_to_speech_with_elevenlabs("Hello Sanjeev, this is ElevenLabs speaking!", "elevenlabs_testing_autoplay.mp3")

