"""
Gemini API route for product description generation
"""

import asyncio
from typing import Dict, Any
from utils.ai_client import GeminiAI

async def generate_product_description(text: str, language: str, ai_client: GeminiAI) -> Dict[str, Any]:
    """
    Generate product description using Gemini AI
    
    Args:
        text: Transcribed text from voice input
        language: Language code
        ai_client: Gemini AI client instance
        
    Returns:
        Dict containing generated description
    """
    try:
        # Create prompt based on language
        prompt = create_description_prompt(text, language)
        
        # Generate description using AI
        description = await ai_client.generate_text(prompt)
        
        return {
            "success": True,
            "description": description,
            "language": language,
            "original_text": text
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Description generation error: {str(e)}",
            "language": language,
            "fallback_description": get_fallback_description(text, language)
        }

async def generate_suggestions(description: str, language: str, ai_client: GeminiAI) -> Dict[str, Any]:
    """
    Generate improvement suggestions using Gemini AI
    
    Args:
        description: Product description
        language: Language code
        ai_client: Gemini AI client instance
        
    Returns:
        Dict containing suggestions
    """
    try:
        # Create suggestion prompt
        prompt = create_suggestion_prompt(description, language)
        
        # Generate suggestions using AI
        suggestions = await ai_client.generate_text(prompt)
        
        return {
            "success": True,
            "suggestions": suggestions,
            "language": language
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Suggestion generation error: {str(e)}",
            "language": language,
            "fallback_suggestions": get_fallback_suggestions(language)
        }

def create_description_prompt(text: str, language: str) -> str:
    """
    Create prompt for description generation
    
    Args:
        text: Transcribed text
        language: Language code
        
    Returns:
        Formatted prompt string
    """
    language_names = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'gu': 'Gujarati',
        'mr': 'Marathi',
        'bn': 'Bengali',
        'or': 'Odia',
        'pa': 'Punjabi'
    }
    
    lang_name = language_names.get(language, 'English')
    
    prompt = f"""
    You are an AI assistant helping Indian farmers create product descriptions for their agricultural products.
    
    The farmer spoke in {lang_name} and said: "{text}"
    
    Please generate a compelling, detailed product description in {lang_name} that includes:
    1. Product name and type
    2. Quality indicators (fresh, organic, local, etc.)
    3. Quantity and pricing information
    4. Benefits and features
    5. Appeal to potential buyers
    
    Make it sound natural and appealing to customers. Keep it concise but informative.
    """
    
    return prompt

def create_suggestion_prompt(description: str, language: str) -> str:
    """
    Create prompt for suggestion generation
    
    Args:
        description: Product description
        language: Language code
        
    Returns:
        Formatted prompt string
    """
    language_names = {
        'en': 'English',
        'hi': 'Hindi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'gu': 'Gujarati',
        'mr': 'Marathi',
        'bn': 'Bengali',
        'or': 'Odia',
        'pa': 'Punjabi'
    }
    
    lang_name = language_names.get(language, 'English')
    
    prompt = f"""
    You are an AI assistant helping Indian farmers improve their product listings.
    
    Here is a product description in {lang_name}: "{description}"
    
    Please provide 2-3 specific suggestions to improve this product listing, such as:
    - Better pricing strategy
    - Enhanced product description
    - Marketing tips
    - Quality improvements
    - Customer appeal suggestions
    
    Provide practical, actionable advice in {lang_name}.
    """
    
    return prompt

def get_fallback_description(text: str, language: str) -> str:
    """
    Get fallback description when AI fails
    
    Args:
        text: Original transcribed text
        language: Language code
        
    Returns:
        Fallback description
    """
    fallback_descriptions = {
        'en': f"Fresh, high-quality product: {text}. Perfect for your daily needs!",
        'hi': f"ताजा, उच्च गुणवत्ता वाला उत्पाद: {text}। आपकी दैनिक आवश्यकताओं के लिए बिल्कुल सही!",
        'ta': f"புதிய, உயர்தர தயாரிப்பு: {text}। உங்கள் தினசரி தேவைகளுக்கு சரியானது!",
        'te': f"తాజా, అధిక నాణ్యత ఉత్పత్తి: {text}। మీ రోజువారీ అవసరాలకు సరైనది!",
        'kn': f"ತಾಜಾ, ಉನ್ನತ ಗುಣಮಟ್ಟದ ಉತ್ಪನ್ನ: {text}। ನಿಮ್ಮ ದೈನಂದಿನ ಅಗತ್ಯತೆಗಳಿಗೆ ಸರಿಯಾಗಿದೆ!",
        'ml': f"പുതിയ, ഉയർന്ന നിലവാരമുള്ള ഉത്പന്നം: {text}। നിങ്ങളുടെ ദൈനിക ആവശ്യങ്ങൾക്ക് അനുയോജ്യമാണ്!",
        'gu': f"તાજા, ઉચ્ચ ગુણવત્તાના ઉત્પાદન: {text}। તમારી દૈનિક જરૂરિયાતો માટે એકદમ યોગ્ય!",
        'mr': f"ताजे, उच्च गुणवत्तेचे उत्पाद: {text}। तुमच्या दैनंदिन गरजांसाठी नेमके योग्य!",
        'bn': f"তাজা, উচ্চ মানের পণ্য: {text}। আপনার দৈনন্দিন প্রয়োজনের জন্য একদম উপযুক্ত!",
        'or': f"ତାଜା, ଉଚ୍ଚ ଗୁଣବତ୍ତାର ଉତ୍ପାଦ: {text}। ଆପଣଙ୍କ ଦୈନିକ ଆବଶ୍ୟକତା ପାଇଁ ଏକଦମ ଯୋଗ୍ୟ!",
        'pa': f"ਤਾਜ਼ਾ, ਉੱਚ ਗੁਣਵੱਤਾ ਦਾ ਉਤਪਾਦ: {text}। ਤੁਹਾਡੀਆਂ ਰੋਜ਼ਾਨਾ ਜ਼ਰੂਰਤਾਂ ਲਈ ਬਿਲਕੁਲ ਸਹੀ!"
    }
    
    return fallback_descriptions.get(language, fallback_descriptions['en'])

def get_fallback_suggestions(language: str) -> str:
    """
    Get fallback suggestions when AI fails
    
    Args:
        language: Language code
        
    Returns:
        Fallback suggestions
    """
    fallback_suggestions = {
        'en': "1. Add better photos\n2. Offer competitive pricing\n3. Highlight freshness and quality",
        'hi': "1. बेहतर फोटो जोड़ें\n2. प्रतिस्पर्धी मूल्य निर्धारण करें\n3. ताजगी और गुणवत्ता पर जोर दें",
        'ta': "1. சிறந்த புகைப்படங்களைச் சேர்க்கவும்\n2. போட்டி விலைகளை வழங்கவும்\n3. புதுமை மற்றும் தரத்தை முன்னிலைப்படுத்தவும்",
        'te': "1. మెరుగైన ఫోటోలు జోడించండి\n2. పోటీ ధరలు అందించండి\n3. తాజాదనం మరియు నాణ్యతను నొక్కి చెప్పండి",
        'kn': "1. ಉತ್ತಮ ಫೋಟೋಗಳನ್ನು ಸೇರಿಸಿ\n2. ಸ್ಪರ್ಧಾತ್ಮಕ ಬೆಲೆ ನೀಡಿ\n3. ತಾಜಾತನ ಮತ್ತು ಗುಣಮಟ್ಟವನ್ನು ಒತ್ತಿ ಹೇಳಿ",
        'ml': "1. മികച്ച ഫോട്ടോകൾ ചേർക്കുക\n2. മത്സര വില നൽകുക\n3. പുതുമയും ഗുണനിലവാരവും ഊന്നിപ്പറയുക",
        'gu': "1. વધુ સારા ફોટા ઉમેરો\n2. સ્પર્ધાત્મક કિંમત આપો\n3. તાજગી અને ગુણવત્તા પર ભાર મૂકો",
        'mr': "1. चांगले फोटो जोडा\n2. स्पर्धात्मक किंमत द्या\n3. ताजेपणा आणि गुणवत्तेवर भर द्या",
        'bn': "1. আরও ভালো ছবি যোগ করুন\n2. প্রতিযোগিতামূলক মূল্য দিন\n3. সতেজতা এবং মানের উপর জোর দিন",
        'or': "1. ଉତ୍ତମ ଫଟୋ ଯୋଡ଼ନ୍ତୁ\n2. ସପ୍ତକ ମୂଲ୍ୟ ଦିଅନ୍ତୁ\n3. ତାଜଗୀ ଏବଂ ଗୁଣବତ୍ତା ଉପରେ ଗୁରୁତ୍ୱ ଦିଅନ୍ତୁ",
        'pa': "1. ਵਧੀਆ ਫੋਟੋ ਜੋੜੋ\n2. ਮੁਕਾਬਲੇ ਦੀ ਕੀਮਤ ਦਿਓ\n3. ਤਾਜ਼ਗੀ ਅਤੇ ਗੁਣਵੱਤਾ ਤੇ ਜ਼ੋਰ ਦਿਓ"
    }
    
    return fallback_suggestions.get(language, fallback_suggestions['en']) 