// AgriVoice - Language Detection
// Handles language dropdown logic and language-specific features

class LanguageDetector {
    constructor() {
        this.currentLanguage = 'en';
        this.languageCodes = {
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
        };
        
        this.languageNames = {
            'en': 'English',
            'hi': 'हिंदी',
            'ta': 'தமிழ்',
            'te': 'తెలుగు',
            'kn': 'ಕನ್ನಡ',
            'ml': 'മലയാളം',
            'gu': 'ગુજરાતી',
            'mr': 'मराठी',
            'bn': 'বাংলা',
            'or': 'ଓଡ଼ିଆ',
            'pa': 'ਪੰਜਾਬੀ'
        };
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.detectUserLanguage();
        this.updateLanguageDisplay();
    }

    setupEventListeners() {
        const languageSelect = document.getElementById('languageSelect');
        
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.currentLanguage = e.target.value;
                this.updateLanguageDisplay();
                this.updateFontFamily();
                this.updatePlaceholders();
                this.updateWelcomeMessage();
            });
        }

        // Add language change buttons if they exist
        const languageButtons = document.querySelectorAll('[data-language]');
        languageButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const language = e.target.dataset.language;
                this.changeLanguage(language);
            });
        });
    }

    detectUserLanguage() {
        // Try to detect user's preferred language
        const userLanguage = navigator.language || navigator.userLanguage;
        const detectedLanguage = this.detectLanguageFromCode(userLanguage);
        
        if (detectedLanguage && detectedLanguage !== 'en') {
            this.currentLanguage = detectedLanguage;
            this.updateLanguageSelect();
        }
    }

    detectLanguageFromCode(languageCode) {
        // Map browser language codes to our supported languages
        const languageMap = {
            'hi': 'hi', 'hi-IN': 'hi', 'hi-US': 'hi',
            'ta': 'ta', 'ta-IN': 'ta', 'ta-US': 'ta',
            'te': 'te', 'te-IN': 'te', 'te-US': 'te',
            'kn': 'kn', 'kn-IN': 'kn', 'kn-US': 'kn',
            'ml': 'ml', 'ml-IN': 'ml', 'ml-US': 'ml',
            'gu': 'gu', 'gu-IN': 'gu', 'gu-US': 'gu',
            'mr': 'mr', 'mr-IN': 'mr', 'mr-US': 'mr',
            'bn': 'bn', 'bn-IN': 'bn', 'bn-US': 'bn',
            'or': 'or', 'or-IN': 'or', 'or-US': 'or',
            'pa': 'pa', 'pa-IN': 'pa', 'pa-US': 'pa'
        };
        
        return languageMap[languageCode] || 'en';
    }

    changeLanguage(language) {
        if (this.languageCodes[language]) {
            this.currentLanguage = language;
            this.updateLanguageSelect();
            this.updateLanguageDisplay();
            this.updateFontFamily();
            this.updatePlaceholders();
            this.updateWelcomeMessage();
            
            // Trigger custom event for other components
            const event = new CustomEvent('languageChanged', { 
                detail: { language: language } 
            });
            document.dispatchEvent(event);
        }
    }

    updateLanguageSelect() {
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.value = this.currentLanguage;
        }
    }

    updateLanguageDisplay() {
        // Update any language-specific UI elements
        const languageElements = document.querySelectorAll('[data-language-text]');
        languageElements.forEach(element => {
            const key = element.dataset.languageText;
            const text = this.getLocalizedText(key);
            if (text) {
                element.textContent = text;
            }
        });
    }

    updateFontFamily() {
        // Update font family based on selected language
        const body = document.body;
        const languageClass = `language-${this.currentLanguage}`;
        
        // Remove existing language classes
        body.classList.remove('language-hi', 'language-ta', 'language-te', 'language-kn', 
                           'language-ml', 'language-gu', 'language-mr', 'language-bn', 
                           'language-or', 'language-pa');
        
        // Add current language class
        if (this.currentLanguage !== 'en') {
            body.classList.add(languageClass);
        }
    }

    updatePlaceholders() {
        // Update input placeholders based on language
        const placeholders = this.getPlaceholders();
        
        Object.keys(placeholders).forEach(selector => {
            const element = document.querySelector(selector);
            if (element) {
                element.placeholder = placeholders[selector];
            }
        });
    }

    updateWelcomeMessage() {
        const welcomeElements = document.querySelectorAll('.welcome-message');
        const greetings = {
            'en': 'Welcome!',
            'hi': 'स्वागत है!',
            'ta': 'வணக்கம்!',
            'te': 'స్వాగతం!',
            'kn': 'ಸುಸ್ವಾಗತ!',
            'ml': 'സ്വാഗതം!',
            'gu': 'સ્વાગત છે!',
            'mr': 'स्वागत आहे!',
            'bn': 'স্বাগতম!',
            'or': 'ସ୍ୱାଗତ!',
            'pa': 'ਸੁਆਗਤ ਹੈ!'
        };
        
        welcomeElements.forEach(element => {
            element.textContent = greetings[this.currentLanguage] || greetings['en'];
        });
    }

    getLocalizedText(key) {
        const translations = {
            'welcome': {
                'en': 'Welcome!',
                'hi': 'स्वागत है!',
                'ta': 'வணக்கம்!',
                'te': 'స్వాగతం!',
                'kn': 'ಸುಸ್ವಾಗತ!',
                'ml': 'സ്വാഗതം!',
                'gu': 'સ્વાગત છે!',
                'mr': 'स्वागत आहे!',
                'bn': 'স্বাগতম!',
                'or': 'ସ୍ୱାଗତ!',
                'pa': 'ਸੁਆਗਤ ਹੈ!'
            },
            'record': {
                'en': 'Click to start recording',
                'hi': 'रिकॉर्डिंग शुरू करने के लिए क्लिक करें',
                'ta': 'பதிவு செய்ய கிளிக் செய்யவும்',
                'te': 'రికార్డింగ్ ప్రారంభించడానికి క్లిక్ చేయండి',
                'kn': 'ರೆಕಾರ್ಡಿಂಗ್ ಪ್ರಾರಂಭಿಸಲು ಕ್ಲಿಕ್ ಮಾಡಿ',
                'ml': 'റെക്കോർഡിംഗ് ആരംഭിക്കാൻ ക്ലിക്ക് ചെയ്യുക',
                'gu': 'રેકોર્ડિંગ શરૂ કરવા માટે ક્લિક કરો',
                'mr': 'रेकॉर्डिंग सुरू करण्यासाठी क्लिक करा',
                'bn': 'রেকর্ডিং শুরু করতে ক্লিক করুন',
                'or': 'ରେକର୍ଡିଂ ଆରମ୍ଭ କରିବାକୁ କ୍ଲିକ୍ କରନ୍ତୁ',
                'pa': 'ਰਿਕਾਰਡਿੰਗ ਸ਼ੁਰੂ ਕਰਨ ਲਈ ਕਲਿਕ ਕਰੋ'
            },
            'mobile': {
                'en': 'Enter your mobile number',
                'hi': 'अपना मोबाइल नंबर दर्ज करें',
                'ta': 'உங்கள் மொபைல் எண்ணை உள்ளிடவும்',
                'te': 'మీ మొబైల్ నంబర్‌ని నమోదు చేయండి',
                'kn': 'ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಂಖ್ಯೆಯನ್ನು ನಮೂದಿಸಿ',
                'ml': 'നിങ്ങളുടെ മൊബൈൽ നമ്പർ നൽകുക',
                'gu': 'તમારો મોબાઇલ નંબર દાખલ કરો',
                'mr': 'तुमचा मोबाईल नंबर टाका',
                'bn': 'আপনার মোবাইল নম্বর লিখুন',
                'or': 'ଆପଣଙ୍କ ମୋବାଇଲ ନମ୍ବର ଦର୍ଶାନ୍ତୁ',
                'pa': 'ਆਪਣਾ ਮੋਬਾਈਲ ਨੰਬਰ ਦਰਜ ਕਰੋ'
            }
        };
        
        return translations[key]?.[this.currentLanguage] || translations[key]?.['en'];
    }

    getPlaceholders() {
        return {
            '#mobileNumber': this.getLocalizedText('mobile'),
            '#farmerName': this.getLocalizedText('name') || 'Enter your full name',
            '#villageCity': this.getLocalizedText('village') || 'Enter your village or city name',
            '#productName': this.getLocalizedText('productName') || 'Enter product name',
            '#productPrice': this.getLocalizedText('price') || 'Enter price',
            '#productQuantity': this.getLocalizedText('quantity') || 'e.g., 1kg, 5 pieces'
        };
    }

    getLanguageCode() {
        return this.languageCodes[this.currentLanguage] || 'en-US';
    }

    getLanguageName() {
        return this.languageNames[this.currentLanguage] || 'English';
    }

    // Voice recognition language setup
    setupVoiceRecognition() {
        if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            
            recognition.lang = this.getLanguageCode();
            recognition.continuous = false;
            recognition.interimResults = false;
            
            return recognition;
        }
        return null;
    }

    // Validate language support
    isLanguageSupported(language) {
        return this.languageCodes.hasOwnProperty(language);
    }

    // Get all supported languages
    getSupportedLanguages() {
        return Object.keys(this.languageCodes);
    }

    // Format language for display
    formatLanguageDisplay(languageCode) {
        const languageName = this.languageNames[languageCode];
        const englishName = this.getEnglishLanguageName(languageCode);
        
        if (languageCode === 'en') {
            return englishName;
        }
        
        return `${englishName} - ${languageName}`;
    }

    getEnglishLanguageName(languageCode) {
        const englishNames = {
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
        };
        
        return englishNames[languageCode] || 'Unknown';
    }

    // Utility method to check if text contains non-Latin characters
    containsNonLatinCharacters(text) {
        return /[^\u0000-\u007F]/.test(text);
    }

    // Get text direction for RTL languages
    getTextDirection(language) {
        const rtlLanguages = ['ar', 'he', 'fa', 'ur'];
        return rtlLanguages.includes(language) ? 'rtl' : 'ltr';
    }

    // Format currency based on language
    formatCurrency(amount, language) {
        const currencyFormats = {
            'en': '₹',
            'hi': '₹',
            'ta': '₹',
            'te': '₹',
            'kn': '₹',
            'ml': '₹',
            'gu': '₹',
            'mr': '₹',
            'bn': '₹',
            'or': '₹',
            'pa': '₹'
        };
        
        const symbol = currencyFormats[language] || '₹';
        return `${symbol}${amount}`;
    }

    // Get number format based on language
    formatNumber(number, language) {
        // For Indian languages, use Indian number system
        if (language !== 'en') {
            return number.toLocaleString('en-IN');
        }
        return number.toLocaleString('en-US');
    }
}

// Initialize LanguageDetector when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.languageDetector = new LanguageDetector();
}); 