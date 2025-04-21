"""
Download About Audio Script

This script downloads the 'ABOUT_THIS.mp3' audio file using Eleven Labs API.
It should be run once to create the audio file for the About section.
"""

import os
import requests
import logging
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Eleven Labs API key
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    logger.error("ELEVENLABS_API_KEY not found in .env file")
    ELEVENLABS_API_KEY = input("Enter your Eleven Labs API key: ")

# Constants
CHUNK_SIZE = 1024
URL = "https://api.elevenlabs.io/v1/text-to-speech/x3BDucQEJ0iGCd8bCaPy"
OUTPUT_FILE = os.path.join('static', 'img', 'ABOUT_THIS.mp3')

# About text
ABOUT_THIS = """
Hi. This is Shahab. Let me tell you about my code.
What it does? 
Our solution is a talking assistant that you use through a web page. You click a button, speak a question out loud, and it gives you an answer in its own voice. It also shows the conversation as text, so you can read along or follow up with more questions.
How it listens and understands? 
1. Recording your question: When you press the microphone icon, your browser captures your voice.  
2. Turning speech into text: The recording is sent to a speech‑to‑text service (OpenAI's Whisper), which writes down exactly what you said.  
3. Finding the right information: Behind the scenes, there's a big "library" of Fort Wise facts stored in a searchable database. A tool called FAISS quickly finds the pieces most relevant to your question.
How it thinks of an answer? 
The bits of information the search finds are stitched together and handed to a small AI (GPT‑4o‑mini and O4-mini). This AI writes a clear, accurate answer based on what it found, making sure it sticks to the Fort Wise facts.
How it talks back to you? 
The text answer from the AI is sent to a text‑to‑speech service (OpenAI's TTS). That service converts the text into a natural‑sounding voice recording, which you hear right in your browser.
Keeping the conversation going:  
Every question and answer you exchange is remembered, so if you ask a follow‑up ("What about…?"), it knows the context of what you've already talked about.
Setting it up and running it:  
1. Get the code: Download or clone the project to your computer.  
2. Install what you need: You need Python and a few libraries (all listed in a requirements file).  
3. Add your secret key: Tell the app your OpenAI key by putting it in a simple settings file.  
4. Start the app: Run the main program.  
5. Use the web page: Open your browser to "localhost:8000," click the microphone, and start asking questions.
How it's organized (behind the scenes)? 
- A small web app handles the user interface.  
- Separate parts handle recording audio, transcribing it, searching the Fort Wise knowledge base, generating answers, and speaking the answers.  
- Utilities help with audio processing and keeping logs.
That's the big picture: you talk, the system listens and converts your voice to text, finds the right facts, writes an answer, and speaks it back—while remembering the flow of your conversation.
"""

def main():
    """
    Download the about audio file from Eleven Labs API.
    """
    # Create directories if they don't exist
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Check if the file already exists
    if os.path.exists(OUTPUT_FILE):
        logger.info(f"Audio file already exists at {OUTPUT_FILE}")
        overwrite = input("Audio file already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            logger.info("Aborted. Keeping existing file.")
            return
    
    # Set up headers
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    # Set up data
    data = {
        "text": ABOUT_THIS,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.45,
            "similarity_boost": 0.89,
            "style": 0.42,
            "use_speaker_boost": True
        }
    }
    
    try:
        logger.info("Sending request to Eleven Labs API...")
        response = requests.post(URL, json=data, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            logger.info("Request successful, saving audio file...")
            
            # Write the audio file
            with open(OUTPUT_FILE, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Audio file saved to {OUTPUT_FILE}")
        else:
            logger.error(f"Request failed with status code {response.status_code}")
            logger.error(f"Response: {response.text}")
    
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")

if __name__ == "__main__":
    main()