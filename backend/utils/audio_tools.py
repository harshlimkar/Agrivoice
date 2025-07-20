"""
Audio Tools for AgriVoice
Handles audio processing, validation, and transcription
"""

import base64
import logging
import speech_recognition as sr
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Handles audio processing and transcription"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.language_codes = {
            'en': 'en-US',
            'hi': 'hi-IN',
            'ta': 'ta-IN',
            'te': 'te-IN',
            'kn': 'kn-IN',
            'ml': 'ml-IN',
            'gu': 'gu-IN',
            'mr': 'mr-IN',
            'bn': 'bn-IN',
            'or': 'or-IN',
            'pa': 'pa-IN'
        }
    
    async def process_audio(self, audio_data: str, language: str) -> str:
        """Process base64 audio data and return transcribed text"""
        try:
            # Decode base64 audio
            audio_bytes = base64.b64decode(audio_data)
            
            # Validate audio format
            validation = self.validate_audio_format(audio_bytes)
            if not validation["valid"]:
                raise ValueError(validation["error"])
            
            # For demo purposes, use mock transcription
            # In production, integrate with Google STT or Whisper
            transcribed_text = self._get_mock_transcription(language)
            
            logger.info(f"Audio processed successfully for language: {language}")
            return transcribed_text
            
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            raise
    
    def validate_audio_format(self, audio_bytes: bytes) -> Dict[str, Any]:
        """Validate audio format and properties"""
        try:
            # Basic validation - check if it's not empty
            if len(audio_bytes) == 0:
                return {"valid": False, "error": "Empty audio data"}
            
            # Check minimum size (1KB)
            if len(audio_bytes) < 1024:
                return {"valid": False, "error": "Audio file too small"}
            
            # Check maximum size (10MB)
            if len(audio_bytes) > 10 * 1024 * 1024:
                return {"valid": False, "error": "Audio file too large"}
            
            # For demo purposes, assume valid
            # In production, you would check actual audio format
            return {
                "valid": True,
                "properties": {
                    "size": len(audio_bytes),
                    "format": "wav",
                    "duration": "unknown"
                }
            }
            
        except Exception as e:
            return {"valid": False, "error": f"Audio validation error: {str(e)}"}
    
    def _get_mock_transcription(self, language: str) -> str:
        """Get mock transcription for demo purposes"""
        mock_texts = {
            'en': "I have 10 kg of fresh tomatoes, selling at ₹40 per kg",
            'hi': "मेरे पास 10 किलो ताजे टमाटर हैं, ₹40 प्रति किलो में बेच रहा हूं",
            'ta': "என்னிடம் 10 கிலோ புதிய தக்காளிகள் உள்ளன, கிலோவுக்கு ₹40 விற்கிறேன்",
            'te': "నా వద్ద 10 కిలోల తాజా టమాటాలు ఉన్నాయి, కిలోకి ₹40 చొప్పున అమ్ముతున్నాను",
            'kn': "ನನ್ನ ಬಳಿ 10 ಕಿಲೋ ತಾಜಾ ಟೊಮೇಟೊಗಳಿವೆ, ಕಿಲೋಗೆ ₹40 ರಂತೆ ಮಾರಾಟ ಮಾಡುತ್ತಿದ್ದೇನೆ",
            'ml': "എന്റെ കൈയിൽ 10 കിലോ പുതിയ തക്കാളികൾ ഉണ്ട്, കിലോയ്ക്ക് ₹40 നിരക്കിൽ വിൽക്കുന്നു",
            'gu': "મારી પાસે 10 કિલો તાજા ટામેટા છે, કિલો દીઠ ₹40 માં વેચું છું",
            'mr': "माझ्याकडे 10 किलो ताजे टोमॅटो आहेत, किलोला ₹40 दराने विकत आहे",
            'bn': "আমার কাছে 10 কিলো তাজা টমেটো আছে, কিলো প্রতি ₹40 দরে বিক্রি করছি",
            'or': "ମୋ ପାଖରେ 10 କିଲୋ ତାଜା ଟମାଟୋ ଅଛି, କିଲୋ ପିଛା ₹40 ଦରରେ ବିକ୍ରି କରୁଛି",
            'pa': "ਮੇਰੇ ਕੋਲ 10 ਕਿਲੋ ਤਾਜ਼ੇ ਟਮਾਟਰ ਹਨ, ਕਿਲੋ ਪ੍ਰਤੀ ₹40 ਵਿੱਚ ਵੇਚ ਰਿਹਾ ਹਾਂ"
        }
        return mock_texts.get(language, mock_texts['en'])
    
    async def transcribe_with_google_stt(self, audio_bytes: bytes, language: str) -> str:
        """Transcribe audio using Google Speech-to-Text"""
        try:
            # For demo purposes, use mock transcription
            # In production, you would integrate with Google STT API
            return self._get_mock_transcription(language)
            
        except Exception as e:
            logger.error(f"Google STT transcription error: {e}")
            raise ValueError(f"Google STT transcription failed: {e}")
    
    async def transcribe_with_whisper(self, audio_bytes: bytes, language: str) -> str:
        """Transcribe audio using OpenAI Whisper"""
        try:
            # This would require OpenAI Whisper API integration
            # For now, return mock transcription
            return self._get_mock_transcription(language)
            
        except Exception as e:
            logger.error(f"Whisper transcription error: {e}")
            raise ValueError(f"Whisper transcription failed: {e}")
    
    def get_supported_languages(self) -> Dict[str, str]:
        """Get supported languages and their codes"""
        return self.language_codes
    
    def get_audio_properties(self, audio_bytes: bytes) -> Dict[str, Any]:
        """Get audio file properties"""
        return {
            "size": len(audio_bytes),
            "format": "wav",
            "sample_rate": 16000,
            "channels": 1,
            "duration": "unknown"
        } 