"""
Speech-to-Text Module

This module handles converting speech audio to text using OpenAI's Whisper API.
"""

import os
import logging
from typing import Optional
import openai
from utils.audio_utils import validate_audio_duration

logger = logging.getLogger(__name__)

class SpeechToText:
    """Class for speech-to-text conversion using OpenAI's Whisper API."""
    
    def __init__(self):
        """Initialize the STT module."""
        # Get API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        openai.api_key = self.api_key
        
        # Maximum duration for audio in seconds (safety check)
        self.max_duration = 30
        
        logger.info("Speech-to-Text module initialized")
    
    def transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        """
        Transcribe speech to text.
        
        Args:
            audio_path: Path to the audio file
            language: Optional language code (e.g., 'en', 'fr')
            
        Returns:
            Transcribed text
        """
        logger.info(f"Transcribing audio from {audio_path}")
        
        # Validate audio duration
        if not validate_audio_duration(audio_path, self.max_duration):
            error_msg = f"Audio exceeds maximum duration of {self.max_duration} seconds"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            # Open audio file
            with open(audio_path, "rb") as audio_file:
                # Call OpenAI Whisper API
                response = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="text"
                )
                
            transcribed_text = response
            
            logger.info(f"Transcription successful: {transcribed_text[:50]}...")
            return transcribed_text
            
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise