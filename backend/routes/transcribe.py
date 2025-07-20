"""
Transcribe Routes
Handles speech-to-text conversion
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class TranscribeRequest(BaseModel):
    """Request model for transcription"""
    audio_data: str
    language: str = "en"

class TranscribeResponse(BaseModel):
    """Response model for transcription"""
    success: bool
    transcribed_text: str
    language: str
    confidence: Optional[float] = None
    error: Optional[str] = None

@router.post("/transcribe", response_model=TranscribeResponse)
async def transcribe_audio(request: TranscribeRequest):
    """Transcribe audio to text"""
    try:
        # This would integrate with the AudioProcessor
        # For now, return mock response
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
        
        transcribed_text = mock_texts.get(request.language, mock_texts['en'])
        
        return TranscribeResponse(
            success=True,
            transcribed_text=transcribed_text,
            language=request.language,
            confidence=0.95
        )
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 