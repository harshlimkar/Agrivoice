// AgriVoice Language Support
// Handles multilingual support and localization

class LanguageSupport {
    constructor() {
        this.currentLanguage = 'en';
        this.translations = this.loadTranslations();
        this.init();
    }

    init() {
        this.loadUserLanguage();
        this.setupLanguageSelector();
        this.updatePageLanguage();
    }

    loadTranslations() {
        return {
            'en': {
                // Navigation
                'nav_home': 'Home',
                'nav_dashboard': 'Dashboard',
                'nav_upload': 'Upload',
                'nav_status': 'Status',
                'nav_logout': 'Logout',
                'nav_login': 'Login',

                // Voice Interface
                'voice_start': 'Click to Start Recording',
                'voice_stop': 'Click to Stop Recording',
                'voice_ready': 'Ready to record',
                'voice_recording': 'Recording...',
                'voice_processing': 'Processing audio...',
                'voice_success': 'Audio processed successfully',
                'voice_error': 'Error processing audio',
                'voice_mic_denied': 'Microphone access denied',

                // Product Form
                'product_name': 'Product Name',
                'product_quantity': 'Quantity',
                'product_price': 'Price per Unit',
                'product_description': 'Description',
                'product_category': 'Category',
                'product_image': 'Product Image',

                // Categories
                'category_vegetables': 'Vegetables',
                'category_fruits': 'Fruits',
                'category_grains': 'Grains',
                'category_dairy': 'Dairy',
                'category_poultry': 'Poultry',
                'category_other': 'Other',

                // Actions
                'action_save': 'Save Product',
                'action_record_again': 'Record Again',
                'action_refresh': 'Refresh Status',
                'action_view': 'View Product',
                'action_add_more': 'Add More Products',

                // Status Messages
                'status_processing': 'Processing...',
                'status_complete': 'Complete',
                'status_pending': 'Pending',
                'status_error': 'Error',
                'status_success': 'Success',

                // Dashboard
                'dashboard_welcome': 'Welcome, Farmer!',
                'dashboard_subtitle': 'Manage your products and track your sales',
                'stats_total_products': 'Total Products',
                'stats_total_sales': 'Total Sales',
                'stats_this_month': 'This Month',
                'stats_rating': 'Rating',

                // Quick Actions
                'quick_add_product': 'Add Product',
                'quick_add_desc': 'Record your product details',
                'quick_view_status': 'View Status',
                'quick_status_desc': 'Check processing status',
                'quick_share': 'Share',
                'quick_share_desc': 'Share your catalog',
                'quick_settings': 'Settings',
                'quick_settings_desc': 'Manage your account',

                // AI Suggestions
                'ai_price_opt': 'Price Optimization',
                'ai_stock_mgmt': 'Stock Management',
                'ai_new_product': 'New Product',

                // Auth
                'login_title': 'Login',
                'register_title': 'Register as Farmer',
                'username': 'Username',
                'password': 'Password',
                'confirm_password': 'Confirm Password',
                'full_name': 'Full Name',
                'mobile_number': 'Mobile Number',
                'village_city': 'Village/City',
                'preferred_language': 'Preferred Language',
                'remember_me': 'Remember me',
                'forgot_password': 'Forgot password?',
                'already_registered': 'Already registered?',
                'not_registered': "Don't have an account?",
                'login_here': 'Login here',
                'register_here': 'Register here',

                // Benefits
                'benefits_voice': 'Voice commands in your native language',
                'benefits_ai': 'AI-generated product descriptions',
                'benefits_tracking': 'Track product sales and get suggestions',
                'benefits_mobile': 'Mobile-friendly interface',

                // Footer
                'footer_made_for_farmers': 'Made for Farmers ❤️ by AgriVoice',
                'footer_empowering': 'Empowering Indian agriculture through voice technology'
            },

            'hi': {
                // Navigation
                'nav_home': 'होम',
                'nav_dashboard': 'डैशबोर्ड',
                'nav_upload': 'अपलोड',
                'nav_status': 'स्थिति',
                'nav_logout': 'लॉगआउट',
                'nav_login': 'लॉगिन',

                // Voice Interface
                'voice_start': 'रिकॉर्डिंग शुरू करने के लिए क्लिक करें',
                'voice_stop': 'रिकॉर्डिंग रोकने के लिए क्लिक करें',
                'voice_ready': 'रिकॉर्ड करने के लिए तैयार',
                'voice_recording': 'रिकॉर्डिंग...',
                'voice_processing': 'ऑडियो प्रोसेसिंग...',
                'voice_success': 'ऑडियो सफलतापूर्वक प्रोसेस किया गया',
                'voice_error': 'ऑडियो प्रोसेसिंग में त्रुटि',
                'voice_mic_denied': 'माइक्रोफोन एक्सेस अस्वीकृत',

                // Product Form
                'product_name': 'उत्पाद का नाम',
                'product_quantity': 'मात्रा',
                'product_price': 'इकाई मूल्य',
                'product_description': 'विवरण',
                'product_category': 'श्रेणी',
                'product_image': 'उत्पाद छवि',

                // Categories
                'category_vegetables': 'सब्जियां',
                'category_fruits': 'फल',
                'category_grains': 'अनाज',
                'category_dairy': 'दूध',
                'category_poultry': 'मुर्गीपालन',
                'category_other': 'अन्य',

                // Actions
                'action_save': 'उत्पाद सहेजें',
                'action_record_again': 'फिर से रिकॉर्ड करें',
                'action_refresh': 'स्थिति रिफ्रेश करें',
                'action_view': 'उत्पाद देखें',
                'action_add_more': 'और उत्पाद जोड़ें',

                // Status Messages
                'status_processing': 'प्रोसेसिंग...',
                'status_complete': 'पूर्ण',
                'status_pending': 'लंबित',
                'status_error': 'त्रुटि',
                'status_success': 'सफलता',

                // Dashboard
                'dashboard_welcome': 'स्वागत है, किसान!',
                'dashboard_subtitle': 'अपने उत्पादों का प्रबंधन करें और बिक्री ट्रैक करें',
                'stats_total_products': 'कुल उत्पाद',
                'stats_total_sales': 'कुल बिक्री',
                'stats_this_month': 'इस महीने',
                'stats_rating': 'रेटिंग',

                // Quick Actions
                'quick_add_product': 'उत्पाद जोड़ें',
                'quick_add_desc': 'अपने उत्पाद का विवरण रिकॉर्ड करें',
                'quick_view_status': 'स्थिति देखें',
                'quick_status_desc': 'प्रोसेसिंग स्थिति जांचें',
                'quick_share': 'शेयर करें',
                'quick_share_desc': 'अपना कैटलॉग शेयर करें',
                'quick_settings': 'सेटिंग्स',
                'quick_settings_desc': 'अपना खाता प्रबंधित करें',

                // AI Suggestions
                'ai_price_opt': 'मूल्य अनुकूलन',
                'ai_stock_mgmt': 'स्टॉक प्रबंधन',
                'ai_new_product': 'नया उत्पाद',

                // Auth
                'login_title': 'लॉगिन',
                'register_title': 'किसान के रूप में पंजीकरण करें',
                'username': 'उपयोगकर्ता नाम',
                'password': 'पासवर्ड',
                'confirm_password': 'पासवर्ड की पुष्टि करें',
                'full_name': 'पूरा नाम',
                'mobile_number': 'मोबाइल नंबर',
                'village_city': 'गांव/शहर',
                'preferred_language': 'पसंदीदा भाषा',
                'remember_me': 'मुझे याद रखें',
                'forgot_password': 'पासवर्ड भूल गए?',
                'already_registered': 'पहले से पंजीकृत हैं?',
                'not_registered': 'खाता नहीं है?',
                'login_here': 'यहां लॉगिन करें',
                'register_here': 'यहां पंजीकरण करें',

                // Benefits
                'benefits_voice': 'अपनी मातृभाषा में आवाज आदेश',
                'benefits_ai': 'एआई-जनित उत्पाद विवरण',
                'benefits_tracking': 'उत्पाद बिक्री ट्रैक करें और सुझाव प्राप्त करें',
                'benefits_mobile': 'मोबाइल-अनुकूल इंटरफेस',

                // Footer
                'footer_made_for_farmers': 'किसानों के लिए बनाया गया ❤️ AgriVoice द्वारा',
                'footer_empowering': 'आवाज तकनीक के माध्यम से भारतीय कृषि को सशक्त बनाना'
            },

            'ta': {
                // Navigation
                'nav_home': 'முகப்பு',
                'nav_dashboard': 'டாஷ்போர்டு',
                'nav_upload': 'பதிவேற்று',
                'nav_status': 'நிலை',
                'nav_logout': 'வெளியேறு',
                'nav_login': 'உள்நுழைவு',

                // Voice Interface
                'voice_start': 'பதிவு தொடங்க கிளிக் செய்யவும்',
                'voice_stop': 'பதிவு நிறுத்த கிளிக் செய்யவும்',
                'voice_ready': 'பதிவு செய்ய தயாராக உள்ளது',
                'voice_recording': 'பதிவு செய்யப்படுகிறது...',
                'voice_processing': 'ஒலி செயலாக்கப்படுகிறது...',
                'voice_success': 'ஒலி வெற்றிகரமாக செயலாக்கப்பட்டது',
                'voice_error': 'ஒலி செயலாக்கத்தில் பிழை',
                'voice_mic_denied': 'மைக்ரோஃபோன் அணுகல் மறுக்கப்பட்டது',

                // Product Form
                'product_name': 'தயாரிப்பு பெயர்',
                'product_quantity': 'அளவு',
                'product_price': 'அலகு விலை',
                'product_description': 'விளக்கம்',
                'product_category': 'வகை',
                'product_image': 'தயாரிப்பு படம்',

                // Categories
                'category_vegetables': 'காய்கறிகள்',
                'category_fruits': 'பழங்கள்',
                'category_grains': 'தானியங்கள்',
                'category_dairy': 'பால்',
                'category_poultry': 'கோழி வளர்ப்பு',
                'category_other': 'மற்றவை',

                // Actions
                'action_save': 'தயாரிப்பு சேமிக்கவும்',
                'action_record_again': 'மீண்டும் பதிவு செய்யவும்',
                'action_refresh': 'நிலை புதுப்பிக்கவும்',
                'action_view': 'தயாரிப்பு காண்க',
                'action_add_more': 'மேலும் தயாரிப்புகள் சேர்க்கவும்',

                // Status Messages
                'status_processing': 'செயலாக்கப்படுகிறது...',
                'status_complete': 'முடிந்தது',
                'status_pending': 'நிலுவையில்',
                'status_error': 'பிழை',
                'status_success': 'வெற்றி',

                // Dashboard
                'dashboard_welcome': 'வரவேற்கிறோம், விவசாயி!',
                'dashboard_subtitle': 'உங்கள் தயாரிப்புகளை நிர்வகித்து விற்பனையை கண்காணிக்கவும்',
                'stats_total_products': 'மொத்த தயாரிப்புகள்',
                'stats_total_sales': 'மொத்த விற்பனை',
                'stats_this_month': 'இந்த மாதம்',
                'stats_rating': 'மதிப்பீடு',

                // Quick Actions
                'quick_add_product': 'தயாரிப்பு சேர்க்கவும்',
                'quick_add_desc': 'உங்கள் தயாரிப்பு விவரங்களை பதிவு செய்யவும்',
                'quick_view_status': 'நிலை காண்க',
                'quick_status_desc': 'செயலாக்க நிலையை சரிபார்க்கவும்',
                'quick_share': 'பகிரவும்',
                'quick_share_desc': 'உங்கள் பட்டியலை பகிரவும்',
                'quick_settings': 'அமைப்புகள்',
                'quick_settings_desc': 'உங்கள் கணக்கை நிர்வகிக்கவும்',

                // AI Suggestions
                'ai_price_opt': 'விலை உகந்தமயமாக்கல்',
                'ai_stock_mgmt': 'சரக்கு மேலாண்மை',
                'ai_new_product': 'புதிய தயாரிப்பு',

                // Auth
                'login_title': 'உள்நுழைவு',
                'register_title': 'விவசாயியாக பதிவு செய்யவும்',
                'username': 'பயனர்பெயர்',
                'password': 'கடவுச்சொல்',
                'confirm_password': 'கடவுச்சொலை உறுதிப்படுத்தவும்',
                'full_name': 'முழு பெயர்',
                'mobile_number': 'மொபைல் எண்',
                'village_city': 'கிராமம்/நகரம்',
                'preferred_language': 'விருப்பமான மொழி',
                'remember_me': 'என்னை நினைவில் வைக்கவும்',
                'forgot_password': 'கடவுச்சொல் மறந்துவிட்டதா?',
                'already_registered': 'ஏற்கனவே பதிவு செய்யப்பட்டுள்ளதா?',
                'not_registered': 'கணக்கு இல்லையா?',
                'login_here': 'இங்கே உள்நுழையவும்',
                'register_here': 'இங்கே பதிவு செய்யவும்',

                // Benefits
                'benefits_voice': 'உங்கள் தாய்மொழியில் குரல் கட்டளைகள்',
                'benefits_ai': 'AI-உருவாக்கப்பட்ட தயாரிப்பு விளக்கங்கள்',
                'benefits_tracking': 'தயாரிப்பு விற்பனையை கண்காணித்து பரிந்துரைகளைப் பெறவும்',
                'benefits_mobile': 'மொபைல்-நட்பு இடைமுகம்',

                // Footer
                'footer_made_for_farmers': 'விவசாயிகளுக்காக உருவாக்கப்பட்டது ❤️ AgriVoice மூலம்',
                'footer_empowering': 'குரல் தொழில்நுட்பம் மூலம் இந்திய விவசாயத்தை சக்தியளித்தல்'
            }
        };
    }

    setupLanguageSelector() {
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.currentLanguage = e.target.value;
                this.updatePageLanguage();
                this.saveUserLanguage();
            });
        }
    }

    loadUserLanguage() {
        const savedLanguage = localStorage.getItem('agrivoice_language');
        if (savedLanguage && this.translations[savedLanguage]) {
            this.currentLanguage = savedLanguage;
            const languageSelect = document.getElementById('languageSelect');
            if (languageSelect) {
                languageSelect.value = savedLanguage;
            }
        }
    }

    saveUserLanguage() {
        localStorage.setItem('agrivoice_language', this.currentLanguage);
    }

    updatePageLanguage() {
        const elements = document.querySelectorAll('[data-translate]');
        elements.forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getTranslation(key);
            if (translation) {
                element.textContent = translation;
            }
        });

        // Update placeholders
        const inputs = document.querySelectorAll('input[data-translate-placeholder]');
        inputs.forEach(input => {
            const key = input.getAttribute('data-translate-placeholder');
            const translation = this.getTranslation(key);
            if (translation) {
                input.placeholder = translation;
            }
        });

        // Update button text
        const buttons = document.querySelectorAll('button[data-translate]');
        buttons.forEach(button => {
            const key = button.getAttribute('data-translate');
            const translation = this.getTranslation(key);
            if (translation) {
                button.textContent = translation;
            }
        });
    }

    getTranslation(key) {
        const translations = this.translations[this.currentLanguage];
        return translations ? translations[key] : this.translations['en'][key] || key;
    }

    translate(key) {
        return this.getTranslation(key);
    }

    // Utility method to translate dynamic content
    translateElement(element, key) {
        const translation = this.getTranslation(key);
        if (translation && element) {
            element.textContent = translation;
        }
    }

    // Method to update specific elements
    updateElement(elementId, key) {
        const element = document.getElementById(elementId);
        if (element) {
            this.translateElement(element, key);
        }
    }

    // Get current language
    getCurrentLanguage() {
        return this.currentLanguage;
    }

    // Check if language is RTL
    isRTLLanguage(language) {
        const rtlLanguages = ['ar', 'he', 'fa', 'ur'];
        return rtlLanguages.includes(language);
    }

    // Update document direction
    updateDocumentDirection() {
        const isRTL = this.isRTLLanguage(this.currentLanguage);
        document.documentElement.dir = isRTL ? 'rtl' : 'ltr';
        document.documentElement.lang = this.currentLanguage;
    }
}

// Initialize language support when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.langSupport = new LanguageSupport();
});

// Export for use in other modules
window.LanguageSupport = LanguageSupport; 