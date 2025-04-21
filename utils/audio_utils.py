"""
Audio Utilities Module

This module provides utility functions for audio processing.
"""

import os
import logging
import librosa
import soundfile as sf
from pydub import AudioSegment
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

def validate_audio_duration(audio_path: str, max_duration: float) -> bool:
    """
    Validate that audio file doesn't exceed maximum duration.
    
    Args:
        audio_path: Path to the audio file
        max_duration: Maximum duration in seconds
        
    Returns:
        True if valid, False if too long
    """
    try:
        # Get audio duration
        duration = get_audio_duration(audio_path)
        
        # Check if duration is within limit
        if duration > max_duration:
            logger.warning(f"Audio duration ({duration:.2f}s) exceeds maximum ({max_duration}s)")
            return False
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating audio duration: {e}")
        # In case of error, assume it's invalid
        return False

def get_audio_duration(audio_path: str) -> float:
    """
    Get the duration of an audio file.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        Duration in seconds
    """
    try:
        # Use librosa to get duration
        duration = librosa.get_duration(path=audio_path)
        logger.debug(f"Audio duration: {duration:.2f} seconds")
        return duration
        
    except Exception as e:
        logger.error(f"Error getting audio duration: {e}")
        # Try with pydub as a fallback
        try:
            audio = AudioSegment.from_file(audio_path)
            duration = len(audio) / 1000.0  # Convert milliseconds to seconds
            logger.debug(f"Audio duration (pydub fallback): {duration:.2f} seconds")
            return duration
        except Exception as e2:
            logger.error(f"Error getting audio duration with pydub: {e2}")
            raise

def convert_audio_format(input_path: str, output_path: str, 
                         sample_rate: int = 16000) -> str:
    """
    Convert audio to a specific format (WAV, 16kHz, mono).
    
    Args:
        input_path: Path to the input audio file
        output_path: Path to save the converted audio
        sample_rate: Target sample rate
        
    Returns:
        Path to the converted audio file
    """
    try:
        # Load audio file
        y, sr = librosa.load(input_path, sr=sample_rate, mono=True)
        
        # Save as WAV
        sf.write(output_path, y, sample_rate)
        
        logger.info(f"Audio converted and saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error converting audio format: {e}")
        raise

def normalize_audio(audio_path: str, output_path: Optional[str] = None) -> str:
    """
    Normalize audio volume.
    
    Args:
        audio_path: Path to the audio file
        output_path: Path to save the normalized audio (if None, overwrite original)
        
    Returns:
        Path to the normalized audio file
    """
    if output_path is None:
        output_path = audio_path
    
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Normalize
        y_norm = librosa.util.normalize(y)
        
        # Save
        sf.write(output_path, y_norm, sr)
        
        logger.info(f"Audio normalized and saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error normalizing audio: {e}")
        raise

def trim_silence(audio_path: str, output_path: Optional[str] = None, 
                 top_db: int = 20) -> str:
    """
    Trim silence from beginning and end of audio.
    
    Args:
        audio_path: Path to the audio file
        output_path: Path to save the trimmed audio (if None, overwrite original)
        top_db: Threshold for silence detection in dB
        
    Returns:
        Path to the trimmed audio file
    """
    if output_path is None:
        output_path = audio_path
    
    try:
        # Load audio
        y, sr = librosa.load(audio_path, sr=None)
        
        # Trim silence
        y_trimmed, trim_indices = librosa.effects.trim(y, top_db=top_db)
        
        # Save
        sf.write(output_path, y_trimmed, sr)
        
        logger.info(f"Silence trimmed from audio and saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error trimming silence: {e}")
        raise

def get_audio_properties(audio_path: str) -> dict:
    """
    Get audio file properties.
    
    Args:
        audio_path: Path to the audio file
        
    Returns:
        Dictionary with audio properties
    """
    try:
        # Load audio file
        y, sr = librosa.load(audio_path, sr=None)
        
        # Get duration
        duration = librosa.get_duration(y=y, sr=sr)
        
        # Get number of channels (mono/stereo)
        channels = 1 if len(y.shape) == 1 else y.shape[0]
        
        return {
            "sample_rate": sr,
            "duration": duration,
            "channels": channels,
            "samples": len(y)
        }
        
    except Exception as e:
        logger.error(f"Error getting audio properties: {e}")
        raise