#!/usr/bin/env python3
"""
Demo script for the multilingual AI backend system
Shows practical usage examples for Indian farmers
"""

import asyncio
import json
import base64
from datetime import datetime

# Mock the utility modules for demo purposes
class MockGeminiAI:
    def __init__(self):
        self.is_available = True
    
    async def extract_product_info(self, text: str, language: str):
        """Mock product extraction"""
        mock_responses = {
            'en': {"product": "tomato", "quantity": "10 kg", "price": "₹40", "price_per_unit": "₹40/kg"},
            'hi': {"product": "टमाटर", "quantity": "10 किलो", "price": "₹40", "price_per_unit": "₹40/किलो"},
            'ta': {"product": "தக்காளி", "quantity": "10 கிலோ", "price": "₹40", "price_per_unit": "₹40/கிலோ"},
            'te': {"product": "టమాట", "quantity": "10 కిలోలు", "price": "₹40", "price_per_unit": "₹40/కిలో"}
        }
        return mock_responses.get(language, mock_responses['en'])
    
    async def generate_product_response(self, product_info: dict, language: str):
        """Mock AI response generation"""
        mock_responses = {
            'en': {
                "description": "Fresh, organic tomatoes from local farm. Perfect for daily cooking needs.",
                "price_range": "₹35 - ₹45 per kg",
                "where_to_sell": "Local vegetable market or nearby town center",
                "selling_tip": "Highlight the organic nature and freshness to attract health-conscious buyers."
            },
            'hi': {
                "description": "ताजे, जैविक टमाटर स्थानीय खेत से। दैनिक खाना पकाने के लिए बिल्कुल सही।",
                "price_range": "₹35 - ₹45 प्रति किलो",
                "where_to_sell": "स्थानीय सब्जी मंडी या पास के शहर केंद्र",
                "selling_tip": "जैविक प्रकृति और ताजगी पर जोर देकर स्वास्थ्य-जागरूक खरीदारों को आकर्षित करें।"
            },
            'ta': {
                "description": "புதிய, கரிம தக்காளிகள் உள்ளூர் பண்ணையில் இருந்து. தினசரி சமையல் தேவைகளுக்கு சரியானது.",
                "price_range": "₹35 - ₹45 கிலோவுக்கு",
                "where_to_sell": "உள்ளூர் காய்கறி சந்தை அல்லது அருகிலுள்ள நகர மையம்",
                "selling_tip": "கரிம தன்மை மற்றும் புதுமையை முன்னிலைப்படுத்தி ஆரோக்கிய உணர்வுள்ள வாங்குபவர்களை ஈர்க்கவும்."
            },
            'te': {
                "description": "స్థానిక పొలం నుండి తాజా, సేంద్రీయ టమాటాలు. రోజువారీ వంటకాలకు చాలా బాగుంటాయి.",
                "price_range": "₹35 - ₹45 కిలోకి",
                "where_to_sell": "స్థానిక కూరగాయల మార్కెట్ లేదా సమీప పట్టణ కేంద్రం",
                "selling_tip": "సేంద్రీయ స్వభావం మరియు తాజాదనాన్ని నొక్కి చెప్పి ఆరోగ్య-అవగాహన ఉన్న కొనుగోలుదారులను ఆకర్షించండి."
            }
        }
        return mock_responses.get(language, mock_responses['en'])

class MockSupabaseClient:
    def __init__(self):
        self.is_available = True
    
    async def insert_product(self, product_data: dict):
        """Mock product storage"""
        return {
            "id": "demo_product_123",
            "farmer_mobile": product_data.get("farmer_mobile"),
            "status": "active",
            "created_at": datetime.now().isoformat()
        }

class MultilingualSystemDemo:
    def __init__(self):
        self.ai_client = MockGeminiAI()
        self.supabase_client = MockSupabaseClient()
    
    async def demo_complete_pipeline(self):
        """Demonstrate the complete voice processing pipeline"""
        print("🌾 AgriVoice Multilingual AI System Demo")
        print("=" * 50)
        
        # Demo scenarios for different languages
        scenarios = [
            {
                "language": "en",
                "farmer_name": "Rajesh Kumar",
                "mobile": "9876543210",
                "scenario": "English-speaking farmer from Punjab"
            },
            {
                "language": "hi", 
                "farmer_name": "राम प्रताप सिंह",
                "mobile": "9876543211",
                "scenario": "Hindi-speaking farmer from Uttar Pradesh"
            },
            {
                "language": "ta",
                "farmer_name": "முத்துசாமி",
                "mobile": "9876543212", 
                "scenario": "Tamil-speaking farmer from Tamil Nadu"
            },
            {
                "language": "te",
                "farmer_name": "వెంకటేశ్వర రావు",
                "mobile": "9876543213",
                "scenario": "Telugu-speaking farmer from Andhra Pradesh"
            }
        ]
        
        for scenario in scenarios:
            print(f"\n👨‍🌾 Farmer: {scenario['farmer_name']}")
            print(f"📱 Mobile: {scenario['mobile']}")
            print(f"🌍 Scenario: {scenario['scenario']}")
            print("-" * 50)
            
            # Step 1: Voice Input (simulated)
            voice_input = self.get_mock_voice_input(scenario['language'])
            print(f"🎤 Voice Input: {voice_input}")
            
            # Step 2: Product Extraction
            product_info = await self.ai_client.extract_product_info(voice_input, scenario['language'])
            print(f"📦 Extracted Product Info:")
            print(f"   Product: {product_info['product']}")
            print(f"   Quantity: {product_info['quantity']}")
            print(f"   Price: {product_info['price']}")
            print(f"   Price per unit: {product_info['price_per_unit']}")
            
            # Step 3: AI Response Generation
            ai_response = await self.ai_client.generate_product_response(product_info, scenario['language'])
            print(f"🤖 AI Generated Response:")
            print(f"   Description: {ai_response['description']}")
            print(f"   Price Range: {ai_response['price_range']}")
            print(f"   Where to Sell: {ai_response['where_to_sell']}")
            print(f"   Selling Tip: {ai_response['selling_tip']}")
            
            # Step 4: Store in Database
            storage_result = await self.store_product(product_info, ai_response, voice_input, scenario)
            print(f"💾 Stored in Database: {storage_result['id']}")
            
            # Step 5: Final Response to Farmer
            final_response = self.create_final_response(product_info, ai_response, scenario['language'], voice_input)
            print(f"📱 Final Response to Farmer:")
            print(f"   Product: {final_response['product']}")
            print(f"   Quantity: {final_response['quantity']}")
            print(f"   Price: {final_response['price']}")
            print(f"   Description: {final_response['description']}")
            print(f"   Suggested Price Range: {final_response['suggested_price_range']}")
            print(f"   Market Suggestion: {final_response['market_suggestion']}")
            print(f"   Selling Tip: {final_response['selling_tip']}")
            
            print("\n" + "="*50)
    
    def get_mock_voice_input(self, language: str) -> str:
        """Get mock voice input for different languages"""
        mock_inputs = {
            'en': "I have 10 kg of fresh tomatoes, selling at ₹40 per kg",
            'hi': "मेरे पास 10 किलो ताजे टमाटर हैं, ₹40 प्रति किलो में बेच रहा हूं",
            'ta': "என்னிடம் 10 கிலோ புதிய தக்காளிகள் உள்ளன, கிலோவுக்கு ₹40 விற்கிறேன்",
            'te': "నా వద్ద 10 కిలోల తాజా టమాటాలు ఉన్నాయి, కిలోకి ₹40 చొప్పున అమ్ముతున్నాను"
        }
        return mock_inputs.get(language, mock_inputs['en'])
    
    async def store_product(self, product_info: dict, ai_response: dict, voice_input: str, scenario: dict) -> dict:
        """Store product in database"""
        product_data = {
            "farmer_mobile": scenario['mobile'],
            "product_info": json.dumps(product_info),
            "ai_response": json.dumps(ai_response),
            "transcribed_text": voice_input,
            "language": scenario['language'],
            "audio_url": None,
            "created_at": datetime.now().isoformat(),
            "status": "active"
        }
        
        return await self.supabase_client.insert_product(product_data)
    
    def create_final_response(self, product_info: dict, ai_response: dict, language: str, voice_input: str) -> dict:
        """Create final response for the farmer"""
        return {
            "success": True,
            "product": product_info.get("product", ""),
            "quantity": product_info.get("quantity", ""),
            "price": product_info.get("price", ""),
            "description": ai_response.get("description", ""),
            "suggested_price_range": ai_response.get("price_range", ""),
            "market_suggestion": ai_response.get("where_to_sell", ""),
            "selling_tip": ai_response.get("selling_tip", ""),
            "language": language,
            "transcribed_text": voice_input
        }
    
    async def demo_api_endpoints(self):
        """Demonstrate API endpoint usage"""
        print("\n🔌 API Endpoints Demo")
        print("=" * 30)
        
        # Demo API request/response format
        api_demo = {
            "endpoint": "POST /api/complete-voice-process",
            "request": {
                "audio_data": "base64_encoded_audio_string",
                "language": "ta"
            },
            "response": {
                "success": True,
                "product": "தக்காளி",
                "quantity": "10 கிலோ",
                "price": "₹40",
                "description": "புதிய, கரிம தக்காளிகள் உள்ளூர் பண்ணையில் இருந்து.",
                "suggested_price_range": "₹35 - ₹45 கிலோவுக்கு",
                "market_suggestion": "உள்ளூர் காய்கறி சந்தை அல்லது அருகிலுள்ள நகர மையம்",
                "selling_tip": "கரிம தன்மை மற்றும் புதுமையை முன்னிலைப்படுத்தி ஆரோக்கிய உணர்வுள்ள வாங்குபவர்களை ஈர்க்கவும்.",
                "language": "ta",
                "transcribed_text": "என்னிடம் 10 கிலோ புதிய தக்காளிகள் உள்ளன, கிலோவுக்கு ₹40 விற்கிறேன்"
            }
        }
        
        print(f"📡 Endpoint: {api_demo['endpoint']}")
        print(f"📤 Request: {json.dumps(api_demo['request'], indent=2)}")
        print(f"📥 Response: {json.dumps(api_demo['response'], indent=2)}")
    
    async def demo_language_support(self):
        """Demonstrate language support"""
        print("\n🌍 Language Support Demo")
        print("=" * 30)
        
        languages = [
            ("en", "English", "I have 10 kg of tomatoes"),
            ("hi", "Hindi", "मेरे पास 10 किलो टमाटर हैं"),
            ("ta", "Tamil", "என்னிடம் 10 கிலோ தக்காளிகள் உள்ளன"),
            ("te", "Telugu", "నా వద్ద 10 కిలోల టమాటాలు ఉన్నాయి"),
            ("kn", "Kannada", "ನನ್ನ ಬಳಿ 10 ಕಿಲೋ ಟೊಮೇಟೊಗಳಿವೆ"),
            ("ml", "Malayalam", "എന്റെ കൈയിൽ 10 കിലോ തക്കാളികൾ ഉണ്ട്"),
            ("gu", "Gujarati", "મારી પાસે 10 કિલો ટામેટા છે"),
            ("mr", "Marathi", "माझ्याकडे 10 किलो टोमॅटो आहेत"),
            ("bn", "Bengali", "আমার কাছে 10 কিলো টমেটো আছে"),
            ("or", "Odia", "ମୋ ପାଖରେ 10 କିଲୋ ଟମାଟୋ ଅଛି"),
            ("pa", "Punjabi", "ਮੇਰੇ ਕੋਲ 10 ਕਿਲੋ ਟਮਾਟਰ ਹਨ")
        ]
        
        for code, name, example in languages:
            print(f"🔤 {code} ({name}): {example}")
    
    async def run_demo(self):
        """Run the complete demo"""
        print("🚀 Starting Multilingual AI System Demo")
        print("=" * 50)
        
        try:
            # Demo complete pipeline
            await self.demo_complete_pipeline()
            
            # Demo API endpoints
            await self.demo_api_endpoints()
            
            # Demo language support
            await self.demo_language_support()
            
            print("\n✅ Demo completed successfully!")
            print("\n💡 Key Features Demonstrated:")
            print("   • Voice input in multiple Indian languages")
            print("   • Structured product information extraction")
            print("   • AI-powered descriptions and suggestions")
            print("   • Multilingual response generation")
            print("   • Database storage and retrieval")
            print("   • Complete end-to-end pipeline")
            
        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")
            import traceback
            traceback.print_exc()

async def main():
    """Main demo function"""
    demo = MultilingualSystemDemo()
    await demo.run_demo()

if __name__ == "__main__":
    print("🌾 AgriVoice Multilingual AI System Demo")
    print("=" * 50)
    asyncio.run(main()) 