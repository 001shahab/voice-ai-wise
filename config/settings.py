"""
Application Settings Module

This module contains configuration settings for the Fort Wise Voice AI Assistant.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Application settings
APP_NAME = "Fort Wise Voice AI Assistant"
VERSION = "1.0.0"

# API keys (from environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio settings
MAX_AUDIO_DURATION = 30  # Maximum audio duration in seconds
ALLOWED_AUDIO_FORMATS = ['.wav', '.mp3', '.ogg', '.m4a', '.webm']

# STT settings
STT_MODEL = "whisper-1"  # OpenAI Whisper model

# LLM settings
LLM_MODEL = "gpt-4o-mini"  # As specified in requirements
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 500

# TTS settings
TTS_MODEL = "tts-1"  # OpenAI TTS model
TTS_VOICE = "alloy"  # Default voice
TTS_SPEED = 1.0      # Default speed

# Knowledge base settings
FAISS_INDEX_PATH = os.path.join('data', 'faiss_index', 'index.faiss')
KB_TEXT_PATH = os.path.join('data', 'knowledge_base.txt')
TOP_K_RESULTS = 5  # Number of context chunks to retrieve

# Context manager settings
MAX_HISTORY = 10  # Maximum conversation history to keep

# Flask settings
PORT = int(os.getenv("PORT", 5000))
FLASK_ENV = os.getenv("FLASK_ENV", "production")
DEBUG = FLASK_ENV == "development"

# File paths
RECORDINGS_DIR = os.path.join('data', 'recordings')
LOGS_DIR = 'logs'

# Ensure directories exist
for directory in [RECORDINGS_DIR, LOGS_DIR, os.path.dirname(FAISS_INDEX_PATH)]:
    os.makedirs(directory, exist_ok=True)