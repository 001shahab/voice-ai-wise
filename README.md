# Fort Wise Voice AI Assistant

A voice-enabled AI assistant that can answer questions about Fort Wise using a knowledge base and natural voice interactions.

## Features

- **Voice Input**: Record questions using your microphone
- **Knowledge Retrieval**: Uses FAISS vector search to find relevant information
- **AI Response Generation**: Generates contextual answers using OpenAI's GPT-4o-mini
- **Voice Output**: Converts responses to natural-sounding speech
- **Conversation Context**: Remembers conversation history and personal information
- **Follow-up Questions**: Supports natural conversation flow with context memory
- **Clean Web Interface**: Intuitive UI with audio recording and playback
- **Custom Knowledge Base**: Upload your own knowledge base text file
- **Fort Wise Agent's Manual Integration**: Pre-configured to answer questions about Fort Wise
- **Fallback Responses**: Provides conversational answers when no context is found
- **Audio Explanation**: Includes an audio explanation of how the system works
- **Error Resilience**: Multiple layers of validation prevent system failures

## Architecture

The system consists of the following components:

1. **Web Interface**: Flask-based web application with voice recording capabilities
2. **Voice Processing Pipeline**:
   - Speech-to-Text: OpenAI Whisper API
   - Knowledge Retrieval: FAISS vector database
   - Answer Generation: OpenAI GPT-4o-mini
   - Text-to-Speech: OpenAI TTS API
3. **Context Management**: Maintains conversation history and user information

## Technical Design

### Speech-to-Text
The system uses OpenAI's Whisper API to transcribe voice input accurately, with forced English language detection.

### Knowledge Retrieval
The application uses FAISS index to search for relevant information in the Fort Wise knowledge base, with sophisticated chunking and relevance scoring.

### Answer Generation
OpenAI's GPT-4o-mini generates responses based on:
1. Retrieved context from the knowledge base
2. Conversation history for continuity
3. User information for personalization
4. General knowledge for fallback responses

### Text-to-Speech
OpenAI's TTS API converts text responses into natural-sounding voice output.

## Getting Started with Fort Wise Agent's Manual

This application comes pre-configured to work with the Fort Wise Agent's Manual, enabling it to answer questions about Fort Wise AI agency, its services, and products (especially Alara).

### Using the Fort Wise Knowledge Base

1. Make sure the file `Agent's manual.txt` is in the root directory of the project
2. Run the setup script to process the manual into the knowledge base:
   ```bash
   python manual_setup.py
   ```
3. Start the application:
   ```bash
   python app.py
   ```
4. Ask questions about Fort Wise, Alara, their services, or anything else mentioned in the manual

### Sample Questions

Try asking questions like:
- "What is Fort Wise?"
- "Who is Alara and what can it do?"
- "What pricing plans are available?"
- "What does the BANE process involve?"
- "How does Alara handle customer complaints?"
- "What integrations does Alara support?"

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key
- (Optional) ElevenLabs API key for about audio

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fort-wise-voice-ai.git
cd fort-wise-voice-ai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables by editing the `.env` file:
```
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here  # Optional, for about audio
```

5. Run the setup script to create necessary directories and files:
```bash
python setup.py
```

6. (Optional) Generate the About audio file using ElevenLabs:
```bash
python download_about_audio.py
```

7. Alternatively, you can place your own audio file at `static/img/ABOUT_THIS.mp3`

Note: The application will automatically create a sample knowledge base and FAISS index if none exists. You can also upload your own knowledge base through the web interface.

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Use the application:
   - Click the microphone button and ask your question
   - Listen to the voice response and view the text conversation
   - Upload your own knowledge base text file (optional)
   - Click the question mark icon for an audio explanation of the system
   - Reset the conversation if needed while keeping user information

## Project Structure

```
fort_wise_voice_ai/
├── .env                         # Environment variables
├── .gitignore                   # Git ignore file
├── README.md                    # Project documentation
├── app.py                       # Main application entry point
├── manual_setup.py              # Script to set up Fort Wise manual
├── setup.py                     # Environment setup script
├── download_about_audio.py      # Script to generate about audio
├── requirements.txt             # Python dependencies
├── static/                      # Static files for web interface
│   ├── css/
│   │   └── style.css            # Custom CSS
│   ├── js/
│   │   └── app.js               # Frontend JavaScript
│   └── img/
│       ├── logo_3S.png          # Project logo
│       └── ABOUT_THIS.mp3       # Audio explanation
├── templates/                   # HTML templates
│   └── index.html               # Main web interface
├── config/                      # Configuration files
│   └── settings.py              # Application settings
├── core/                        # Core functionality modules
│   ├── voice_processor.py       # Voice processing pipeline
│   ├── stt.py                   # Speech-to-text functionality
│   ├── tts.py                   # Text-to-speech functionality
│   ├── knowledge_base.py        # FAISS integration
│   ├── llm.py                   # LLM integration
│   └── context_manager.py       # Conversation context and user information
├── utils/                       # Utility functions
│   ├── audio_utils.py           # Audio processing utilities
│   └── logging_utils.py         # Custom logging utilities
└── data/                        # Data directory
    ├── faiss_index/             # FAISS index files
    ├── knowledge_base.txt       # Knowledge base text
    └── recordings/              # Voice recordings
```

## System Improvements

Recent improvements to the system include:

1. **Enhanced Conversation Handling**:
   - Remembers user names and other personal information
   - Maintains natural conversation flow with context awareness
   - Avoids robotic disclaimers for a more natural experience

2. **Error Resilience**:
   - Multi-level validation to prevent empty responses
   - Graceful recovery from API errors
   - Detailed logging for troubleshooting

3. **Better Knowledge Handling**:
   - Sophisticated chunking for more relevant context retrieval
   - Improved search algorithms for accurate responses
   - Better integration with external knowledge bases

4. **Personalization**:
   - Remembers and uses the user's name in responses
   - Preserves user information even when resetting conversation
   - Directly handles personal questions (e.g., "What's my name?")

## Contributor

Designed and developed by Prof. Shahab Anbarjafari - Tartu, Estonia.
