"""
Voice Processor Module

This module orchestrates the entire voice processing pipeline:
1. Speech-to-Text conversion
2. Knowledge retrieval from vector database
3. LLM response generation
4. Text-to-Speech conversion
"""

import os
import logging
import uuid
import time
from typing import List, Dict, Any, Optional

from core.stt import SpeechToText
from core.tts import TextToSpeech
from core.knowledge_base import KnowledgeBase
from core.llm import LanguageModel
from core.context_manager import ContextManager
from utils.audio_utils import validate_audio_duration

logger = logging.getLogger(__name__)

class VoiceProcessor:
    """Main class for voice processing pipeline."""
    
    def __init__(self):
        """Initialize voice processor components."""
        logger.info("Initializing Voice Processor...")
        
        # Initialize components
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.knowledge_base = KnowledgeBase()
        self.llm = LanguageModel()
        self.context_manager = ContextManager()
        
        # Set maximum audio duration (in seconds)
        self.max_audio_duration = 30  # 30 seconds as specified
        
        logger.info("Voice Processor initialized successfully")
    
    def speech_to_text(self, audio_path: str) -> str:
        """
        Convert speech to text.
        
        Args:
            audio_path: Path to the audio file
            
        Returns:
            Transcribed text
        """
        logger.info(f"Converting speech to text from {audio_path}")
        
        # Validate audio file length
        # Implementation in audio_utils to check duration
        
        try:
            transcribed_text = self.stt.transcribe(audio_path)
            return transcribed_text
        except Exception as e:
            logger.error(f"Error in speech-to-text conversion: {e}")
            raise
    
    def retrieve_context(self, query: str) -> List[Dict[str, Any]]:
        """
        Retrieve relevant context from knowledge base.
        
        Args:
            query: User query text
            
        Returns:
            List of relevant context chunks
        """
        logger.info(f"Retrieving context for query: {query}")
        
        try:
            # Get conversation history from context manager
            conversation_history = self.context_manager.get_history()
            
            # Retrieve relevant information from knowledge base
            context_chunks = self.knowledge_base.search(
                query, 
                n_results=5,
                conversation_history=conversation_history
            )
            
            return context_chunks
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            raise
    
    def generate_response(self, query: str, context: List[Dict[str, Any]]) -> str:
        """
        Generate response using LLM.
        
        Args:
            query: User query text
            context: Retrieved context chunks
            
        Returns:
            Generated response text
        """
        logger.info("Generating response with LLM")
        
        try:
            # Get conversation history
            conversation_history = self.context_manager.get_history()
            
            # Generate response
            response = self.llm.generate_response(
                query=query,
                context=context,
                conversation_history=conversation_history
            )
            
            # Update conversation context
            self.context_manager.add_exchange(query, response)
            
            return response
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def text_to_speech(self, text: str) -> str:
        """
        Convert text to speech.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Path to the generated audio file
        """
        logger.info("Converting text to speech")
        
        try:
            # Generate a unique filename
            filename = f"{uuid.uuid4()}.wav"
            output_path = os.path.join('data', 'recordings', filename)
            
            # Make sure directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Convert text to speech
            self.tts.synthesize(text, output_path)
            
            return output_path
        except Exception as e:
            logger.error(f"Error in text-to-speech conversion: {e}")
            raise
    
    def reset_context(self):
        """Reset the conversation context."""
        logger.info("Resetting conversation context")
        self.context_manager.reset()