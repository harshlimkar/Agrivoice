"""
Status route for sold status and suggestions
"""

import asyncio
from typing import Dict, Any, List
from datetime import datetime
from utils.supabase_client import SupabaseClient
from utils.ai_client import GeminiAI

async def check_product_status(mobile: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Check product status for a farmer
    
    Args:
        mobile: Farmer's mobile number
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing product status and statistics
    """
    try:
        # Get products from database
        products = await supabase_client.get_products_by_mobile(mobile)
        
        # Calculate statistics
        total_products = len(products)
        sold_products = len([p for p in products if p.get("status") == "sold"])
        pending_products = total_products - sold_products
        
        # Calculate sold percentage
        sold_percentage = (sold_products / total_products * 100) if total_products > 0 else 0
        
        return {
            "success": True,
            "statistics": {
                "total": total_products,
                "sold": sold_products,
                "pending": pending_products,
                "sold_percentage": round(sold_percentage, 2)
            },
            "products": products
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to check product status: {str(e)}",
            "statistics": {
                "total": 0,
                "sold": 0,
                "pending": 0,
                "sold_percentage": 0
            },
            "products": get_mock_products(mobile)
        }

async def generate_improvement_suggestions(products: List[Dict[str, Any]], language: str, ai_client: GeminiAI) -> Dict[str, Any]:
    """
    Generate improvement suggestions for products
    
    Args:
        products: List of products
        language: Language code
        ai_client: Gemini AI client instance
        
    Returns:
        Dict containing suggestions
    """
    try:
        # Filter pending products
        pending_products = [p for p in products if p.get("status") == "pending"]
        
        if not pending_products:
            return {
                "success": True,
                "suggestions": get_no_pending_suggestions(language),
                "language": language
            }
        
        # Create prompt for suggestions
        prompt = create_improvement_prompt(pending_products, language)
        
        # Generate suggestions using AI
        suggestions = await ai_client.generate_text(prompt)
        
        return {
            "success": True,
            "suggestions": suggestions,
            "language": language,
            "pending_count": len(pending_products)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to generate suggestions: {str(e)}",
            "suggestions": get_fallback_suggestions(language),
            "language": language
        }

async def update_product_status(product_id: str, status: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Update product status (sold/pending)
    
    Args:
        product_id: Product ID
        status: New status (sold/pending)
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing update result
    """
    try:
        # Update product status
        result = await supabase_client.update_product_status(product_id, status)
        
        return {
            "success": True,
            "product_id": product_id,
            "status": status,
            "message": f"Product status updated to {status}"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to update product status: {str(e)}"
        }

async def get_product_analytics(mobile: str, supabase_client: SupabaseClient) -> Dict[str, Any]:
    """
    Get detailed product analytics
    
    Args:
        mobile: Farmer's mobile number
        supabase_client: Supabase client instance
        
    Returns:
        Dict containing analytics
    """
    try:
        # Get products from database
        products = await supabase_client.get_products_by_mobile(mobile)
        
        # Calculate analytics
        analytics = calculate_product_analytics(products)
        
        return {
            "success": True,
            "analytics": analytics
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to get analytics: {str(e)}",
            "analytics": get_mock_analytics()
        }

def calculate_product_analytics(products: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate product analytics
    
    Args:
        products: List of products
        
    Returns:
        Dict containing analytics
    """
    if not products:
        return get_mock_analytics()
    
    # Calculate basic statistics
    total_products = len(products)
    sold_products = len([p for p in products if p.get("status") == "sold"])
    pending_products = total_products - sold_products
    
    # Calculate time-based analytics
    recent_products = [p for p in products if is_recent_product(p)]
    old_products = total_products - len(recent_products)
    
    # Calculate language distribution
    language_distribution = {}
    for product in products:
        lang = product.get("language", "en")
        language_distribution[lang] = language_distribution.get(lang, 0) + 1
    
    return {
        "total_products": total_products,
        "sold_products": sold_products,
        "pending_products": pending_products,
        "sold_percentage": round((sold_products / total_products * 100), 2) if total_products > 0 else 0,
        "recent_products": len(recent_products),
        "old_products": old_products,
        "language_distribution": language_distribution,
        "average_products_per_day": calculate_average_per_day(products)
    }

def is_recent_product(product: Dict[str, Any]) -> bool:
    """
    Check if product is recent (within 7 days)
    
    Args:
        product: Product data
        
    Returns:
        True if recent
    """
    try:
        created_at = datetime.fromisoformat(product.get("created_at", ""))
        days_old = (datetime.utcnow() - created_at).days
        return days_old <= 7
    except:
        return False

def calculate_average_per_day(products: List[Dict[str, Any]]) -> float:
    """
    Calculate average products per day
    
    Args:
        products: List of products
        
    Returns:
        Average products per day
    """
    if not products:
        return 0.0
    
    try:
        # Get date range
        dates = []
        for product in products:
            created_at = datetime.fromisoformat(product.get("created_at", ""))
            dates.append(created_at.date())
        
        if not dates:
            return 0.0
        
        min_date = min(dates)
        max_date = max(dates)
        days_range = (max_date - min_date).days + 1
        
        return round(len(products) / days_range, 2)
    except:
        return 0.0

def create_improvement_prompt(products: List[Dict[str, Any]], language: str) -> str:
    """
    Create prompt for improvement suggestions
    
    Args:
        products: List of pending products
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
    
    # Create product list for prompt
    product_list = []
    for product in products:
        product_list.append(f"- {product.get('name', 'Unknown')}: {product.get('description', 'No description')}")
    
    products_text = "\n".join(product_list)
    
    prompt = f"""
    You are an AI assistant helping Indian farmers improve their product listings.
    
    The farmer has {len(products)} pending products in {lang_name}:
    {products_text}
    
    Please provide specific, actionable suggestions to help sell these products, including:
    1. Pricing strategies
    2. Marketing improvements
    3. Product description enhancements
    4. Quality improvements
    5. Customer appeal suggestions
    
    Provide practical advice in {lang_name}. Focus on actionable steps the farmer can take immediately.
    """
    
    return prompt

def get_mock_products(mobile: str) -> List[Dict[str, Any]]:
    """
    Get mock products for demo purposes
    
    Args:
        mobile: Farmer's mobile number
        
    Returns:
        List of mock products
    """
    return [
        {
            "id": "1",
            "name": "Fresh Tomatoes",
            "description": "Fresh, high-quality tomatoes from local farm",
            "language": "en",
            "farmer_mobile": mobile,
            "status": "pending",
            "created_at": "2024-01-15T10:30:00Z",
            "suggestions": "Try adding better photos and highlighting freshness"
        },
        {
            "id": "2",
            "name": "Organic Rice",
            "description": "Premium quality organic rice",
            "language": "en",
            "farmer_mobile": mobile,
            "status": "sold",
            "created_at": "2024-01-14T15:45:00Z"
        },
        {
            "id": "3",
            "name": "Sweet Mangoes",
            "description": "Sweet and juicy mangoes from organic farms",
            "language": "en",
            "farmer_mobile": mobile,
            "status": "pending",
            "created_at": "2024-01-13T09:20:00Z",
            "suggestions": "Consider competitive pricing and quick delivery"
        }
    ]

def get_mock_analytics() -> Dict[str, Any]:
    """
    Get mock analytics for demo purposes
    
    Returns:
        Mock analytics data
    """
    return {
        "total_products": 3,
        "sold_products": 1,
        "pending_products": 2,
        "sold_percentage": 33.33,
        "recent_products": 2,
        "old_products": 1,
        "language_distribution": {"en": 3},
        "average_products_per_day": 1.0
    }

def get_no_pending_suggestions(language: str) -> str:
    """
    Get suggestions when no pending products
    
    Args:
        language: Language code
        
    Returns:
        Suggestions text
    """
    suggestions = {
        'en': "🎉 Great job! All your products are sold. Consider adding more products to increase your income.",
        'hi': "🎉 बहुत अच्छा! आपके सभी उत्पाद बिक गए हैं। अपनी आय बढ़ाने के लिए और उत्पाद जोड़ने पर विचार करें।",
        'ta': "🎉 மிகவும் நல்லது! உங்கள் அனைத்து பொருட்களும் விற்கப்பட்டுள்ளன. உங்கள் வருமானத்தை அதிகரிக்க மேலும் பொருட்களை சேர்ப்பதைக் கவனியுங்கள்.",
        'te': "🎉 చాలా మంచిది! మీ అన్ని ఉత్పత్తులు అమ్మబడ్డాయి. మీ ఆదాయాన్ని పెంచడానికి మరిన్ని ఉత్పత్తులను జోడించడాన్ని పరిగణించండి.",
        'kn': "🎉 ತುಂಬಾ ಒಳ್ಳೆಯದು! ನಿಮ್ಮ ಎಲ್ಲಾ ಉತ್ಪನ್ನಗಳು ಮಾರಾಟವಾಗಿವೆ. ನಿಮ್ಮ ಆದಾಯವನ್ನು ಹೆಚ್ಚಿಸಲು ಹೆಚ್ಚಿನ ಉತ್ಪನ್ನಗಳನ್ನು ಸೇರಿಸುವುದನ್ನು ಪರಿಗಣಿಸಿ.",
        'ml': "🎉 വളരെ നല്ലത്! നിങ്ങളുടെ എല്ലാ ഉത്പന്നങ്ങളും വിറ്റു. നിങ്ങളുടെ വരുമാനം വർദ്ധിപ്പിക്കാൻ കൂടുതൽ ഉത്പന്നങ്ങൾ ചേർക്കുന്നത് പരിഗണിക്കുക.",
        'gu': "🎉 ખૂબ સરસ! તમારા બધા ઉત્પાદનો વેચાઈ ગયા છે. તમારી આવક વધારવા માટે વધુ ઉત્પાદનો ઉમેરવાનું વિચારો.",
        'mr': "🎉 खूप छान! तुमचे सर्व उत्पादन विकले गेले आहेत. तुमचे उत्पन्न वाढवण्यासाठी अधिक उत्पादने जोडण्याचा विचार करा.",
        'bn': "🎉 খুব ভালো! আপনার সব পণ্য বিক্রি হয়ে গেছে। আপনার আয় বাড়াতে আরও পণ্য যোগ করার কথা ভাবুন।",
        'or': "🎉 ବହୁତ ଭଲ! ଆପଣଙ୍କ ସମସ୍ତ ଉତ୍ପାଦ ବିକ୍ରି ହୋଇଛି। ଆପଣଙ୍କ ଆୟ ବୃଦ୍ଧି ପାଇଁ ଅଧିକ ଉତ୍ପାଦ ଯୋଗ କରିବାକୁ ବିଚାର କରନ୍ତୁ।",
        'pa': "🎉 ਬਹੁਤ ਵਧੀਆ! ਤੁਹਾਡੇ ਸਾਰੇ ਉਤਪਾਦ ਵਿਕ ਗਏ ਹਨ। ਤੁਹਾਡੀ ਆਮਦਨੀ ਵਧਾਉਣ ਲਈ ਹੋਰ ਉਤਪਾਦ ਜੋੜਨ ਦੀ ਸੋਚੋ।"
    }
    
    return suggestions.get(language, suggestions['en'])

def get_fallback_suggestions(language: str) -> str:
    """
    Get fallback suggestions when AI fails
    
    Args:
        language: Language code
        
    Returns:
        Fallback suggestions
    """
    suggestions = {
        'en': "1. Add better photos\n2. Offer competitive pricing\n3. Highlight freshness and quality\n4. Respond quickly to inquiries\n5. Add detailed descriptions",
        'hi': "1. बेहतर फोटो जोड़ें\n2. प्रतिस्पर्धी मूल्य निर्धारण करें\n3. ताजगी और गुणवत्ता पर जोर दें\n4. जल्दी जवाब दें\n5. विस्तृत विवरण जोड़ें",
        'ta': "1. சிறந்த புகைப்படங்களைச் சேர்க்கவும்\n2. போட்டி விலைகளை வழங்கவும்\n3. புதுமை மற்றும் தரத்தை முன்னிலைப்படுத்தவும்\n4. விரைவில் பதிலளிக்கவும்\n5. விரிவான விளக்கங்களைச் சேர்க்கவும்",
        'te': "1. మెరుగైన ఫోటోలు జోడించండి\n2. పోటీ ధరలు అందించండి\n3. తాజగી మరియు నాణ్యతను నొక్కి చెప్పండి\n4. త్వరగా సమాధానం ఇవ్వండి\n5. వివరణాత్మక వివరాలను జోడించండి",
        'kn': "1. ಉತ್ತಮ ಫೋಟೋಗಳನ್ನು ಸೇರಿಸಿ\n2. ಸ್ಪರ್ಧಾತ್ಮಕ ಬೆಲೆ ನೀಡಿ\n3. ತಾಜಾತನ ಮತ್ತು ಗುಣಮಟ್ಟವನ್ನು ಒತ್ತಿ ಹೇಳಿ\n4. ತ್ವರಿತವಾಗಿ ಪ್ರತಿಕ್ರಿಯಿಸಿ\n5. ವಿವರವಾದ ವಿವರಣೆಗಳನ್ನು ಸೇರಿಸಿ",
        'ml': "1. മികച്ച ഫോട്ടോകൾ ചേർക്കുക\n2. മത്സര വില നൽകുക\n3. പുതുമയും ഗുണനിലവാരവും ഊന്നിപ്പറയുക\n4. വേഗത്തിൽ മറുപടി നൽകുക\n5. വിശദമായ വിവരണങ്ങൾ ചേർക്കുക",
        'gu': "1. વધુ સારા ફોટા ઉમેરો\n2. સ્પર્ધાત્મક કિંમત આપો\n3. તાજગી અને ગુણવત્તા પર ભાર મૂકો\n4. ઝડપથી જવાબ આપો\n5. વિગતવાર વર્ણનો ઉમેરો",
        'mr': "1. चांगले फोटो जोडा\n2. स्पर्धात्मक किंमत द्या\n3. ताजेपणा आणि गुणवत्तेवर भर द्या\n4. लवकर प्रतिसाद द्या\n5. तपशीलवार वर्णने जोडा",
        'bn': "1. আরও ভালো ছবি যোগ করুন\n2. প্রতিযোগিতামূলক মূল্য দিন\n3. সতেজতা এবং মানের উপর জোর দিন\n4. দ্রুত সাড়া দিন\n5. বিস্তারিত বিবরণ যোগ করুন",
        'or': "1. ଉତ୍ତମ ଫଟୋ ଯୋଡ଼ନ୍ତୁ\n2. ସପ୍ତକ ମୂଲ୍ୟ ଦିଅନ୍ତୁ\n3. ତାଜଗୀ ଏବଂ ଗୁଣବତ୍ତା ଉପରେ ଗୁରୁତ୍ୱ ଦିଅନ୍ତୁ\n4. ଶୀଘ୍ର ପ୍ରତିକ୍ରିୟା ଦିଅନ୍ତୁ\n5. ବିସ୍ତୃତ ବିବରଣୀ ଯୋଡ଼ନ୍ତୁ",
        'pa': "1. ਵਧੀਆ ਫੋਟੋ ਜੋੜੋ\n2. ਮੁਕਾਬਲੇ ਦੀ ਕੀਮਤ ਦਿਓ\n3. ਤਾਜ਼ਗੀ ਅਤੇ ਗੁਣਵੱਤਾ ਤੇ ਜ਼ੋਰ ਦਿਓ\n4. ਤੇਜ਼ੀ ਨਾਲ ਜਵਾਬ ਦਿਓ\n5. ਵਿਸਤ੍ਰਿਤ ਵੇਰਵੇ ਜੋੜੋ"
    }
    
    return suggestions.get(language, suggestions['en']) 