"""
Gemini AI Client for AgriVoice
Handles AI-powered product analysis and suggestions
"""

import google.generativeai as genai
import json
import logging
from typing import Dict, Any, Optional
import os

logger = logging.getLogger(__name__)

class GeminiAIClient:
    """Client for interacting with Google's Gemini AI"""
    
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            self.api_key = "demo_key"  # For demo purposes
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
    async def extract_product_info(self, text: str, language: str) -> Dict[str, Any]:
        """Extract structured product information from transcribed text"""
        try:
            prompt = self._create_extraction_prompt(text, language)
            response = await self._generate_text(prompt)
            return self._parse_product_extraction(response, text)
        except Exception as e:
            logger.error(f"Error extracting product info: {e}")
            return self._fallback_product_info(text)
    
    async def generate_suggestions(self, product_info: Dict[str, Any], 
                                 original_text: str, language: str) -> Dict[str, Any]:
        """Generate AI-powered suggestions for the product"""
        try:
            prompt = self._create_suggestions_prompt(product_info, original_text, language)
            response = await self._generate_text(prompt)
            return self._parse_ai_suggestions(response, language)
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return self._fallback_suggestions(language)
    
    async def generate_improvement_suggestions(self, product_info: Dict[str, Any], 
                                            language: str) -> Dict[str, Any]:
        """Generate improvement suggestions for unsold products"""
        try:
            prompt = self._create_improvement_prompt(product_info, language)
            response = await self._generate_text(prompt)
            return self._parse_improvement_suggestions(response, language)
        except Exception as e:
            logger.error(f"Error generating improvement suggestions: {e}")
            return self._fallback_improvement_suggestions(language)
    
    def _create_extraction_prompt(self, text: str, language: str) -> str:
        """Create prompt for product information extraction"""
        lang_name = self._get_language_name(language)
        
        return f"""
        Extract structured product information from this text in {lang_name}: "{text}"
        
        Return ONLY a JSON object with the following structure:
        {{
            "product": "product name",
            "quantity": "quantity with unit",
            "price": "price with currency",
            "price_per_unit": "price per unit if mentioned"
        }}
        
        Example: If text says "I have 10 kg of onions selling at ₹30 per kg"
        Return: {{"product": "onion", "quantity": "10 kg", "price": "₹30", "price_per_unit": "₹30/kg"}}
        
        Extract only the information that is explicitly mentioned in the text.
        """
    
    def _create_suggestions_prompt(self, product_info: Dict[str, Any], 
                                 original_text: str, language: str) -> str:
        """Create comprehensive AI prompt for suggestions generation"""
        lang_name = self._get_language_name(language)
        product = product_info.get("product", "product")
        quantity = product_info.get("quantity", "quantity")
        price = product_info.get("price", "price")
        
        return f"""
        A farmer has {quantity} of {product} and is selling them at {price}.
        
        Generate the following in {lang_name}:
        1. A short product description (2-3 sentences)
        2. Suggested minimum and maximum market price range for {product} today
        3. Suggestions on where the farmer can sell the {product} (e.g., local market, online agri-portal, nearby town)
        4. A simple promotional message or tip to attract buyers
        
        Return ONLY a JSON object with this structure:
        {{
            "description": "product description in {lang_name}",
            "price_range": "suggested price range",
            "where_to_sell": "market suggestions in {lang_name}",
            "selling_tip": "promotional tip in {lang_name}"
        }}
        
        Make the response practical, helpful, and culturally appropriate for Indian farmers.
        """
    
    def _create_improvement_prompt(self, product_info: Dict[str, Any], language: str) -> str:
        """Create prompt for improvement suggestions"""
        lang_name = self._get_language_name(language)
        product = product_info.get("product", "product")
        
        return f"""
        A farmer's {product} has not been sold for several days. 
        Generate improvement suggestions in {lang_name} to help sell the product.
        
        Consider:
        1. Pricing strategy adjustments
        2. Better product presentation
        3. Alternative selling channels
        4. Marketing improvements
        5. Quality enhancements
        
        Return ONLY a JSON object with this structure:
        {{
            "pricing_suggestions": "pricing improvement tips in {lang_name}",
            "presentation_tips": "how to present the product better in {lang_name}",
            "marketing_ideas": "marketing improvement suggestions in {lang_name}",
            "alternative_channels": "alternative selling channels in {lang_name}"
        }}
        """
    
    async def _generate_text(self, prompt: str) -> str:
        """Generate text using Gemini AI"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {e}")
            return ""
    
    def _parse_product_extraction(self, ai_response: str, original_text: str) -> Dict[str, Any]:
        """Parse AI response to extract structured product information"""
        try:
            if "{" in ai_response and "}" in ai_response:
                start = ai_response.find("{")
                end = ai_response.rfind("}") + 1
                json_str = ai_response[start:end]
                return json.loads(json_str)
            else:
                return self._fallback_product_info(original_text)
        except Exception as e:
            logger.error(f"Error parsing product extraction: {e}")
            return self._fallback_product_info(original_text)
    
    def _parse_ai_suggestions(self, ai_response: str, language: str) -> Dict[str, Any]:
        """Parse AI response to extract suggestions"""
        try:
            if "{" in ai_response and "}" in ai_response:
                start = ai_response.find("{")
                end = ai_response.rfind("}") + 1
                json_str = ai_response[start:end]
                return json.loads(json_str)
            else:
                return self._fallback_suggestions(language)
        except Exception as e:
            logger.error(f"Error parsing AI suggestions: {e}")
            return self._fallback_suggestions(language)
    
    def _parse_improvement_suggestions(self, ai_response: str, language: str) -> Dict[str, Any]:
        """Parse AI response to extract improvement suggestions"""
        try:
            if "{" in ai_response and "}" in ai_response:
                start = ai_response.find("{")
                end = ai_response.rfind("}") + 1
                json_str = ai_response[start:end]
                return json.loads(json_str)
            else:
                return self._fallback_improvement_suggestions(language)
        except Exception as e:
            logger.error(f"Error parsing improvement suggestions: {e}")
            return self._fallback_improvement_suggestions(language)
    
    def _fallback_product_info(self, text: str) -> Dict[str, Any]:
        """Fallback product information extraction"""
        return {
            "product": "unknown",
            "quantity": "unknown",
            "price": "unknown",
            "price_per_unit": "unknown",
            "original_text": text
        }
    
    def _fallback_suggestions(self, language: str) -> Dict[str, Any]:
        """Fallback AI suggestions"""
        lang_name = self._get_language_name(language)
        return {
            "description": f"Fresh product available in {lang_name}",
            "price_range": "Market price",
            "where_to_sell": f"Local market in {lang_name}",
            "selling_tip": f"Highlight freshness and quality in {lang_name}"
        }
    
    def _fallback_improvement_suggestions(self, language: str) -> Dict[str, Any]:
        """Fallback improvement suggestions"""
        lang_name = self._get_language_name(language)
        return {
            "pricing_suggestions": f"Consider competitive pricing in {lang_name}",
            "presentation_tips": f"Improve product presentation in {lang_name}",
            "marketing_ideas": f"Try different marketing approaches in {lang_name}",
            "alternative_channels": f"Explore alternative selling channels in {lang_name}"
        }
    
    def _get_language_name(self, language_code: str) -> str:
        """Get language name from language code"""
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
        return language_names.get(language_code, 'English')
    
    def get_api_status(self) -> Dict[str, Any]:
        """Get API status"""
        return {
            "status": "available" if self.api_key != "demo_key" else "demo_mode",
            "model": "gemini-pro",
            "api_key_configured": self.api_key != "demo_key"
        } 