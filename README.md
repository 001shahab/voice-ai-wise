# Fort Wise Voice AI Assistant

A voice-enabled AI assistant that can answer questions about Fort Wise using a knowledge base and natural voice interactions.

## Features

- **Voice Input**: Record questions using your microphone
- **Knowledge Retrieval**: Uses FAISS vector search to find relevant information
- **AI Response Generation**: Generates contextual answers using OpenAI's o4-mini-2025-04-16
- **Voice Output**: Converts responses to natural-sounding speech
- **Conversation History**: Supports follow-up questions with context memory
- **Clean Web Interface**: Intuitive UI with audio recording and playback
- **Custom Knowledge Base**: Upload your own knowledge base text file
- **Fort Wise Agent's Manual Integration**: Pre-configured to answer questions about Fort Wise
- **Fallback Responses**: Provides answers based on general knowledge when no context is found
- **Audio Explanation**: Includes an audio explanation of how the system works

## Architecture

The system consists of the following components:

1. **Web Interface**: Flask-based web application with voice recording capabilities
2. **Voice Processing Pipeline**:
   - Speech-to-Text: OpenAI Whisper API
   - Knowledge Retrieval: FAISS vector database
   - Answer Generation: OpenAI o4-mini-2025-04-16
   - Text-to-Speech: OpenAI TTS API
3. **Context Management**: Maintains conversation history for follow-up questions

## Technical Design

### Speech-to-Text
The system uses OpenAI's Whisper API to transcribe voice input accurately.

### Knowledge Retrieval
The application uses a pre-computed FAISS index to search for relevant information in the Fort Wise knowledge base.

### Answer Generation
OpenAI's o4-mini-2025-04-16 generates responses based on the retrieved context, ensuring answers are grounded in the knowledge base.

### Text-to-Speech
OpenAI's TTS API converts text responses into natural-sounding voice output.

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key

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

## Project Structure

```
fort_wise_voice_ai/
├── .env                        # Environment variables
├── .gitignore                  # Git ignore file
├── README.md                   # Project documentation
├── requirements.txt            # Python dependencies
├── app.py                      # Main application entry point
├── static/                     # Static files for web interface
│   ├── css/
│   │   └── style.css           # Custom CSS
│   ├── js/
│   │   └── app.js              # Frontend JavaScript
│   └── img/
│       └── logo_3S.png         # Project logo
├── templates/                  # HTML templates
│   └── index.html              # Main web interface
├── config/                     # Configuration files
│   └── settings.py             # Application settings
├── core/                       # Core functionality modules
│   ├── voice_processor.py      # Voice processing pipeline
│   ├── stt.py                  # Speech-to-text functionality
│   ├── tts.py                  # Text-to-speech functionality
│   ├── knowledge_base.py       # FAISS integration
│   ├── llm.py                  # LLM integration
│   └── context_manager.py      # Conversation context
├── utils/                      # Utility functions
│   ├── audio_utils.py          # Audio processing utilities
│   └── logging_utils.py        # Custom logging utilities
└── data/                       # Data directory
    ├── faiss_index/            # FAISS index files
    ├── knowledge_base.txt      # Knowledge base text
    └── recordings/             # Voice recordings
```

## Extension Ideas

1. **Multilingual Support**: Add language detection and multilingual responses
2. **Voice Customization**: Allow users to select different voices for responses
3. **Enhanced UI**: Add visual feedback, transcription display, and more
4. **Analytics**: Track common questions and response quality
5. **Deployment**: Deploy to cloud platforms with containerization

## Note on Data Privacy

This application processes voice data and sends it to OpenAI for transcription and response generation. Ensure you have appropriate privacy policies in place if deploying this application.

## Contributor

Designed and developed by Prof. Shahab Anbarjafari - Tartu, Estonia.
