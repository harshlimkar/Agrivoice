"""
Gemini API helper client
"""

import os
import asyncio
from typing import Dict, Any, Optional
import google.generativeai as genai
import os

class GeminiAI:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model = None
        self.is_initialized = False
        
        if self.api_key:
            self.initialize()
    
    def initialize(self):
        """Initialize Gemini AI client"""
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.is_initialized = True
        except Exception as e:
            print(f"Failed to initialize Gemini AI: {e}")
            self.is_initialized = False
    
    async def generate_text(self, prompt: str) -> str:
        """
        Generate text using Gemini AI
        
        Args:
            prompt: Input prompt
            
        Returns:
            Generated text
        """
        if not self.is_initialized or not self.model:
            return self.get_fallback_response(prompt)
        
        try:
            # Generate response
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            
            return response.text
            
        except Exception as e:
            print(f"Gemini AI error: {e}")
            return self.get_fallback_response(prompt)
    
    async def generate_description(self, text: str, language: str) -> str:
        """
        Generate product description
        
        Args:
            text: Transcribed text
            language: Language code
            
        Returns:
            Generated description
        """
        prompt = self.create_description_prompt(text, language)
        return await self.generate_text(prompt)
    
    async def generate_suggestions(self, description: str, language: str) -> str:
        """
        Generate improvement suggestions
        
        Args:
            description: Product description
            language: Language code
            
        Returns:
            Generated suggestions
        """
        prompt = self.create_suggestion_prompt(description, language)
        return await self.generate_text(prompt)
    
    def create_description_prompt(self, text: str, language: str) -> str:
        """
        Create prompt for description generation
        
        Args:
            text: Transcribed text
            language: Language code
            
        Returns:
            Formatted prompt
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
        
        return f"""
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
    
    def create_suggestion_prompt(self, description: str, language: str) -> str:
        """
        Create prompt for suggestion generation
        
        Args:
            description: Product description
            language: Language code
            
        Returns:
            Formatted prompt
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
        
        return f"""
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
    
    def get_fallback_response(self, prompt: str) -> str:
        """
        Get fallback response when AI is not available
        
        Args:
            prompt: Original prompt
            
        Returns:
            Fallback response
        """
        # Simple fallback responses based on prompt content
        if "product description" in prompt.lower():
            return "Fresh, high-quality product from local farm. Perfect for your daily needs!"
        elif "suggestions" in prompt.lower():
            return "1. Add better photos\n2. Offer competitive pricing\n3. Highlight freshness and quality"
        else:
            return "AI service is currently unavailable. Please try again later."
    
    def is_available(self) -> bool:
        """
        Check if AI service is available
        
        Returns:
            True if available
        """
        return self.is_initialized and self.api_key is not None
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        Get API status information
        
        Returns:
            Status information
        """
        return {
            "available": self.is_available(),
            "initialized": self.is_initialized,
            "has_api_key": self.api_key is not None
        } 