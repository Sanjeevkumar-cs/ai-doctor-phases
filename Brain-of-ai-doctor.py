#Step1: Setup GROQ API key
import os

GROQ_API_KEY=os.environ.get("GROQ_API_KEY")

#Step2: Convert image to required format

import base64
from tkinter import filedialog, Tk
from pathlib import Path

# Setup: This hides the annoying extra window Tkinter creates
root = Tk()
root.withdraw()

# 1. Selection: Pick the file via Windows/Mac/Linux explorer
path_string = filedialog.askopenfilename(title="Select Image")

if path_string:
    # 2. Conversion: Pathlib reads the bytes, base64 converts them
    binary_data = Path(path_string).read_bytes()
    encoded_text = base64.b64encode(binary_data).decode('utf-8')

    # 3. Output: Result
    print(f"Success! Image converted to {len(encoded_text)} characters.")
    print(f"Start of string: {encoded_text[:50]}...")
else:
    print("No file selected.")

root.destroy()

#Step3: Setup Multimodal LLM
from groq import Groq

query="Is there something wrong with my face?"
model = "meta-llama/llama-4-maverick-17b-128e-instruct"
#model="meta-llama/llama-4-scout-17b-16e-instruct"

client=Groq()
messages=[
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": query
            },
            {
                "type": "image_url",
                "image_url": {
                "url": f"data:image/jpeg;base64,{encoded_text}",},
            },
            ],
        }]
chat_completion=client.chat.completions.create(
messages=messages,
model=model
)

print(chat_completion.choices[0].message.content)