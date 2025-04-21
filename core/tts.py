"""
Text-to-Speech Module

This module handles converting text to speech using OpenAI's TTS API.
"""

import os
import logging
import openai

logger = logging.getLogger(__name__)

class TextToSpeech:
    """Class for text-to-speech conversion using OpenAI's TTS API."""
    
    def __init__(self):
        """Initialize the TTS module."""
        # Get API key from environment
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        openai.api_key = self.api_key
        
        # TTS settings
        self.model = "tts-1"  # Default model
        self.voice = "ash"  # Default voice: options are 'alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'
        self.speed = 1.0      # Default speed (0.25 to 4.0)
        
        logger.info("Text-to-Speech module initialized")
    
    def synthesize(self, text: str, output_path: str, 
                  voice: str = None, speed: float = None) -> str:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save the audio file
            voice: Voice to use (defaults to self.voice)
            speed: Speech speed (defaults to self.speed)
            
        Returns:
            Path to the generated audio file
        """
        # Use default values if not specified
        voice = voice or self.voice
        speed = speed or self.speed
        
        logger.info(f"Converting text to speech using voice: {voice}, speed: {speed}")
        
        try:
            # Call OpenAI TTS API
            response = openai.audio.speech.create(
                model=self.model,
                voice=voice,
                input=text,
                speed=speed
            )
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Save to file
            response.stream_to_file(output_path)
            
            logger.info(f"Speech synthesis successful, saved to {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error during speech synthesis: {str(e)}")
            raise
    
    def set_voice(self, voice: str) -> None:
        """
        Set the voice to use for TTS.
        
        Args:
            voice: Voice to use ('alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer')
        """
        valid_voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
        if voice not in valid_voices:
            raise ValueError(f"Invalid voice '{voice}'. Must be one of {valid_voices}")
        
        self.voice = voice
        logger.info(f"Voice set to {voice}")
    
    def set_speed(self, speed: float) -> None:
        """
        Set the speech speed.
        
        Args:
            speed: Speech speed (0.25 to 4.0)
        """
        if not 0.25 <= speed <= 4.0:
            raise ValueError(f"Invalid speed '{speed}'. Must be between 0.25 and 4.0")
        
        self.speed = speed
        logger.info(f"Speed set to {speed}")