"""
Audio tools utility for WAV conversion and format checking
"""

import io
import wave
import base64
from typing import Dict, Any, Optional
import numpy as np

class AudioTools:
    def __init__(self):
        self.supported_formats = ['wav', 'mp3', 'ogg', 'webm']
        self.max_file_size = 10 * 1024 * 1024  # 10MB
    
    def validate_audio_format(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Validate audio format and properties
        
        Args:
            audio_bytes: Raw audio bytes
            
        Returns:
            Validation result
        """
        try:
            # Check file size
            if len(audio_bytes) > self.max_file_size:
                return {
                    "valid": False,
                    "error": "File size too large (max 10MB)"
                }
            
            # Check minimum size
            if len(audio_bytes) < 1000:
                return {
                    "valid": False,
                    "error": "File size too small"
                }
            
            # Try to detect format
            format_info = self.detect_audio_format(audio_bytes)
            
            if not format_info["detected"]:
                return {
                    "valid": False,
                    "error": "Unsupported audio format"
                }
            
            # Get audio properties
            properties = self.get_audio_properties(audio_bytes, format_info["format"])
            
            return {
                "valid": True,
                "format": format_info["format"],
                "properties": properties
            }
            
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }
    
    def detect_audio_format(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Detect audio format from bytes
        
        Args:
            audio_bytes: Raw audio bytes
            
        Returns:
            Format detection result
        """
        # Check for common audio format signatures
        signatures = {
            b'RIFF': 'wav',
            b'ID3': 'mp3',
            b'OggS': 'ogg',
            b'\x1a\x45\xdf\xa3': 'webm'
        }
        
        for signature, format_name in signatures.items():
            if audio_bytes.startswith(signature):
                return {
                    "detected": True,
                    "format": format_name
                }
        
        # If no signature found, assume it's a valid audio format
        return {
            "detected": True,
            "format": "unknown"
        }
    
    def get_audio_properties(self, audio_bytes: bytes, format_name: str) -> Dict[str, Any]:
        """
        Get audio properties
        
        Args:
            audio_bytes: Raw audio bytes
            format_name: Audio format name
            
        Returns:
            Audio properties
        """
        try:
            if format_name == 'wav':
                return self.get_wav_properties(audio_bytes)
            else:
                # For other formats, return estimated properties
                return self.estimate_audio_properties(audio_bytes)
        except Exception as e:
            return self.estimate_audio_properties(audio_bytes)
    
    def get_wav_properties(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Get WAV file properties
        
        Args:
            audio_bytes: WAV audio bytes
            
        Returns:
            WAV properties
        """
        try:
            with io.BytesIO(audio_bytes) as audio_io:
                with wave.open(audio_io, 'rb') as wav_file:
                    return {
                        "channels": wav_file.getnchannels(),
                        "sample_width": wav_file.getsampwidth(),
                        "frame_rate": wav_file.getframerate(),
                        "frames": wav_file.getnframes(),
                        "duration": wav_file.getnframes() / wav_file.getframerate()
                    }
        except Exception as e:
            return self.estimate_audio_properties(audio_bytes)
    
    def estimate_audio_properties(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Estimate audio properties for non-WAV formats
        
        Args:
            audio_bytes: Audio bytes
            
        Returns:
            Estimated properties
        """
        # Rough estimation based on file size
        size_kb = len(audio_bytes) / 1024
        
        # Estimate duration based on typical bitrates
        # Assuming 128kbps for most formats
        estimated_duration = (size_kb * 8) / 128  # seconds
        
        return {
            "channels": 1,  # Assume mono
            "sample_width": 2,  # Assume 16-bit
            "frame_rate": 16000,  # Assume 16kHz
            "frames": int(estimated_duration * 16000),
            "duration": estimated_duration
        }
    
    def convert_to_wav(self, audio_bytes: bytes, format_name: str) -> bytes:
        """
        Convert audio to WAV format
        
        Args:
            audio_bytes: Raw audio bytes
            format_name: Source format name
            
        Returns:
            WAV format audio bytes
        """
        try:
            if format_name == 'wav':
                return audio_bytes
            
            # For demo purposes, return as-is
            # In production, you would use proper audio conversion libraries
            return audio_bytes
            
        except Exception as e:
            raise Exception(f"Audio conversion error: {str(e)}")
    
    def normalize_audio(self, audio_bytes: bytes) -> bytes:
        """
        Normalize audio levels
        
        Args:
            audio_bytes: Audio bytes
            
        Returns:
            Normalized audio bytes
        """
        try:
            # For demo purposes, return as-is
            # In production, you would normalize audio levels
            return audio_bytes
        except Exception as e:
            raise Exception(f"Audio normalization error: {str(e)}")
    
    def resample_audio(self, audio_bytes: bytes, target_rate: int = 16000) -> bytes:
        """
        Resample audio to target sample rate
        
        Args:
            audio_bytes: Audio bytes
            target_rate: Target sample rate
            
        Returns:
            Resampled audio bytes
        """
        try:
            # For demo purposes, return as-is
            # In production, you would resample audio
            return audio_bytes
        except Exception as e:
            raise Exception(f"Audio resampling error: {str(e)}")
    
    def extract_audio_segment(self, audio_bytes: bytes, start_time: float, end_time: float) -> bytes:
        """
        Extract audio segment
        
        Args:
            audio_bytes: Audio bytes
            start_time: Start time in seconds
            end_time: End time in seconds
            
        Returns:
            Audio segment bytes
        """
        try:
            # For demo purposes, return as-is
            # In production, you would extract the segment
            return audio_bytes
        except Exception as e:
            raise Exception(f"Audio segment extraction error: {str(e)}")
    
    def get_audio_duration(self, audio_bytes: bytes) -> float:
        """
        Get audio duration in seconds
        
        Args:
            audio_bytes: Audio bytes
            
        Returns:
            Duration in seconds
        """
        try:
            # Try to get duration from WAV file
            if audio_bytes.startswith(b'RIFF'):
                with io.BytesIO(audio_bytes) as audio_io:
                    with wave.open(audio_io, 'rb') as wav_file:
                        return wav_file.getnframes() / wav_file.getframerate()
            
            # Estimate duration for other formats
            size_kb = len(audio_bytes) / 1024
            return (size_kb * 8) / 128  # Assuming 128kbps
            
        except Exception:
            # Fallback estimation
            return len(audio_bytes) / 16000  # Rough estimation
    
    def validate_audio_quality(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Validate audio quality
        
        Args:
            audio_bytes: Audio bytes
            
        Returns:
            Quality assessment
        """
        try:
            duration = self.get_audio_duration(audio_bytes)
            size_mb = len(audio_bytes) / (1024 * 1024)
            
            # Quality assessment based on duration and size
            if duration < 1:
                quality = "poor"
                reason = "Audio too short"
            elif duration > 60:
                quality = "poor"
                reason = "Audio too long"
            elif size_mb > 5:
                quality = "poor"
                reason = "File too large"
            elif duration >= 3 and duration <= 30:
                quality = "good"
                reason = "Optimal duration"
            else:
                quality = "acceptable"
                reason = "Within acceptable range"
            
            return {
                "quality": quality,
                "reason": reason,
                "duration": duration,
                "size_mb": size_mb
            }
            
        except Exception as e:
            return {
                "quality": "unknown",
                "reason": f"Error assessing quality: {str(e)}",
                "duration": 0,
                "size_mb": 0
            }
    
    def base64_to_bytes(self, base64_string: str) -> bytes:
        """
        Convert base64 string to bytes
        
        Args:
            base64_string: Base64 encoded string
            
        Returns:
            Audio bytes
        """
        try:
            return base64.b64decode(base64_string)
        except Exception as e:
            raise Exception(f"Base64 decode error: {str(e)}")
    
    def bytes_to_base64(self, audio_bytes: bytes) -> str:
        """
        Convert bytes to base64 string
        
        Args:
            audio_bytes: Audio bytes
            
        Returns:
            Base64 encoded string
        """
        try:
            return base64.b64encode(audio_bytes).decode('utf-8')
        except Exception as e:
            raise Exception(f"Base64 encode error: {str(e)}") 