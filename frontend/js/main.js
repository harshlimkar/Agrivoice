// AgriVoice - Main JavaScript
// Handles button logic, form submits, and general interactions

class AgriVoice {
    constructor() {
        this.API_BASE_URL = 'http://localhost:8000';
        this.currentLanguage = 'en';
        this.init();
        this.testAPIConnection();
    }

    init() {
        this.setupEventListeners();
        this.initializeAnimations();
        this.addEmojiWaveAnimation();
    }

    setupEventListeners() {
        // Registration form events
        this.setupRegistrationEvents();
        
        // Voice upload events
        this.setupVoiceUploadEvents();
        
        // Status check events
        this.setupStatusCheckEvents();
        
        // General button events
        this.setupGeneralEvents();
    }

    setupRegistrationEvents() {
        const sendOtpBtn = document.getElementById('sendOtpBtn');
        const verifyOtpBtn = document.getElementById('verifyOtpBtn');
        const resendOtpBtn = document.getElementById('resendOtpBtn');
        const languageSelect = document.getElementById('languageSelect');

        if (sendOtpBtn) {
            sendOtpBtn.addEventListener('click', () => this.sendOTP());
        }

        if (verifyOtpBtn) {
            verifyOtpBtn.addEventListener('click', () => this.verifyOTP());
        }

        if (resendOtpBtn) {
            resendOtpBtn.addEventListener('click', () => this.resendOTP());
        }

        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.currentLanguage = e.target.value;
                this.updateLanguageDisplay();
            });
        }

        // Mobile number validation
        const mobileInput = document.getElementById('mobileNumber');
        if (mobileInput) {
            mobileInput.addEventListener('input', (e) => this.validateMobileNumber(e.target.value));
        }
    }

    setupVoiceUploadEvents() {
        const recordBtn = document.getElementById('recordBtn');
        const stopRecordBtn = document.getElementById('stopRecordBtn');
        const playRecordBtn = document.getElementById('playRecordBtn');
        const regenerateBtn = document.getElementById('regenerateBtn');
        const regenerateDescriptionBtn = document.getElementById('regenerateDescriptionBtn');
        const editDescriptionBtn = document.getElementById('editDescriptionBtn');
        const saveProductBtn = document.getElementById('saveProductBtn');
        const uploadAnotherBtn = document.getElementById('uploadAnotherBtn');
        const languageSelect = document.getElementById('languageSelect');

        if (recordBtn) {
            recordBtn.addEventListener('click', () => this.toggleRecording());
        }

        if (stopRecordBtn) {
            stopRecordBtn.addEventListener('click', () => this.stopRecording());
        }

        if (playRecordBtn) {
            playRecordBtn.addEventListener('click', () => this.playRecording());
        }

        if (regenerateBtn) {
            regenerateBtn.addEventListener('click', () => this.regenerateTranscription());
        }

        if (regenerateDescriptionBtn) {
            regenerateDescriptionBtn.addEventListener('click', () => this.regenerateDescription());
        }

        if (editDescriptionBtn) {
            editDescriptionBtn.addEventListener('click', () => this.editDescription());
        }

        if (saveProductBtn) {
            saveProductBtn.addEventListener('click', () => this.saveProduct());
        }

        if (uploadAnotherBtn) {
            uploadAnotherBtn.addEventListener('click', () => this.uploadAnother());
        }

        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.currentLanguage = e.target.value;
                this.updateLanguageDisplay();
            });
        }
    }

    setupStatusCheckEvents() {
        const checkStatusBtn = document.getElementById('checkStatusBtn');
        const mobileInput = document.getElementById('mobileNumber');

        if (checkStatusBtn) {
            checkStatusBtn.addEventListener('click', () => this.checkProductStatus());
        }

        if (mobileInput) {
            mobileInput.addEventListener('input', (e) => this.validateMobileNumber(e.target.value));
        }
    }

    setupGeneralEvents() {
        // Add ripple effect to all buttons
        document.addEventListener('click', (e) => {
            if (e.target.matches('button')) {
                this.addRippleEffect(e.target, e);
            }
        });

        // Add hover effects to cards
        const cards = document.querySelectorAll('.product-card, .bg-white');
        cards.forEach(card => {
            card.classList.add('hover-lift');
        });
    }

    // Registration Methods
    async sendOTP() {
        const mobile = document.getElementById('mobileNumber')?.value;
        const farmerName = document.getElementById('farmerName')?.value;
        const villageCity = document.getElementById('villageCity')?.value;

        if (!this.validateMobileNumber(mobile)) {
            this.showMessage('Please enter a valid 10-digit mobile number', 'error');
            return;
        }

        if (!farmerName || !villageCity) {
            this.showMessage('Please fill in all required fields', 'error');
            return;
        }

        this.showLoading(true);

        try {
            // Simulate OTP sending
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            this.showMessage('OTP sent to your mobile number! 📱', 'success');
            
            // Show OTP section
            const otpSection = document.getElementById('otpSection');
            if (otpSection) {
                otpSection.classList.remove('hidden');
                otpSection.classList.add('fade-in');
            }

            // Add loading effect to button
            const sendOtpBtn = document.getElementById('sendOtpBtn');
            if (sendOtpBtn) {
                const originalText = sendOtpBtn.textContent;
                sendOtpBtn.textContent = 'Sending...';
                sendOtpBtn.disabled = true;
                
                setTimeout(() => {
                    sendOtpBtn.textContent = originalText;
                    sendOtpBtn.disabled = false;
                }, 2000);
            }
        } catch (error) {
            this.showMessage('Failed to send OTP. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async verifyOTP() {
        const otpInput = document.getElementById('otpInput')?.value;
        
        if (!otpInput || otpInput.length !== 6) {
            this.showMessage('Please enter a valid 6-digit OTP', 'error');
            return;
        }

        this.showLoading(true);

        try {
            // Simulate OTP verification
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            this.showMessage('Registration successful! Welcome to AgriVoice! 🌾', 'success');
            
            // Redirect to upload page after successful registration
            setTimeout(() => {
                window.location.href = 'upload.html';
            }, 2000);
        } catch (error) {
            this.showMessage('Invalid OTP. Please try again.', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async resendOTP() {
        const mobile = document.getElementById('mobileNumber')?.value;
        
        if (!this.validateMobileNumber(mobile)) {
            this.showMessage('Please enter a valid mobile number first', 'error');
            return;
        }

        this.showMessage('OTP resent to your mobile number! 📱', 'success');
        
        // Add loading effect
        const resendOtpBtn = document.getElementById('resendOtpBtn');
        if (resendOtpBtn) {
            resendOtpBtn.textContent = 'Resending...';
            resendOtpBtn.disabled = true;
            
            setTimeout(() => {
                resendOtpBtn.textContent = 'Resend OTP';
                resendOtpBtn.disabled = false;
            }, 2000);
        }
    }

    // Voice Upload Methods
    toggleRecording() {
        // This will be handled by recorder.js
        console.log('Toggle recording called');
    }

    stopRecording() {
        // This will be handled by recorder.js
        console.log('Stop recording called');
    }

    playRecording() {
        // This will be handled by recorder.js
        console.log('Play recording called');
    }

    async regenerateTranscription() {
        this.showLoading(true);
        
        try {
            // Simulate regeneration
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            this.showMessage('Transcription regenerated successfully!', 'success');
        } catch (error) {
            this.showMessage('Failed to regenerate transcription', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async regenerateDescription() {
        this.showLoading(true);
        
        try {
            // Simulate regeneration
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            this.showMessage('Description regenerated successfully!', 'success');
        } catch (error) {
            this.showMessage('Failed to regenerate description', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    editDescription() {
        const descriptionDiv = document.getElementById('generatedDescription');
        if (descriptionDiv) {
            const currentText = descriptionDiv.textContent;
            const textarea = document.createElement('textarea');
            textarea.value = currentText;
            textarea.className = 'w-full px-4 py-3 bg-green-50 border border-green-300 rounded-lg min-h-[60px] mb-4';
            
            descriptionDiv.replaceWith(textarea);
            textarea.focus();
            
            // Add save button
            const saveBtn = document.createElement('button');
            saveBtn.textContent = 'Save Changes';
            saveBtn.className = 'bg-green-500 text-white px-4 py-2 rounded-lg hover:bg-green-600 transition-colors';
            saveBtn.onclick = () => this.saveDescriptionChanges(textarea);
            
            textarea.parentNode.insertBefore(saveBtn, textarea.nextSibling);
        }
    }

    saveDescriptionChanges(textarea) {
        const newText = textarea.value;
        const descriptionDiv = document.createElement('div');
        descriptionDiv.id = 'generatedDescription';
        descriptionDiv.className = 'w-full px-4 py-3 bg-green-50 border border-green-300 rounded-lg min-h-[60px] mb-4';
        descriptionDiv.textContent = newText;
        
        textarea.replaceWith(descriptionDiv);
        this.showMessage('Description updated successfully!', 'success');
    }

    async saveProduct() {
        const productName = document.getElementById('productName')?.value;
        const productCategory = document.getElementById('productCategory')?.value;
        const productPrice = document.getElementById('productPrice')?.value;
        const productQuantity = document.getElementById('productQuantity')?.value;

        if (!productName || !productCategory || !productPrice || !productQuantity) {
            this.showMessage('Please fill in all product details', 'error');
            return;
        }

        this.showLoading(true);

        try {
            // Simulate saving product
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            this.showMessage('Product saved successfully! 🌾', 'success');
            
            // Show action buttons
            const actionButtons = document.getElementById('actionButtons');
            if (actionButtons) {
                actionButtons.classList.remove('hidden');
                actionButtons.classList.add('fade-in');
            }
        } catch (error) {
            this.showMessage('Failed to save product', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    uploadAnother() {
        // Reset form and hide action buttons
        const actionButtons = document.getElementById('actionButtons');
        const transcribedSection = document.getElementById('transcribedSection');
        const descriptionSection = document.getElementById('descriptionSection');
        const productForm = document.getElementById('productForm');

        if (actionButtons) actionButtons.classList.add('hidden');
        if (transcribedSection) transcribedSection.classList.add('hidden');
        if (descriptionSection) descriptionSection.classList.add('hidden');
        if (productForm) productForm.classList.add('hidden');

        // Reset form fields
        const formInputs = document.querySelectorAll('input, select');
        formInputs.forEach(input => {
            if (input.type !== 'button') {
                input.value = '';
            }
        });

        this.showMessage('Ready to upload another product! 🎤', 'info');
    }

    // Status Check Methods
    async checkProductStatus() {
        const mobile = document.getElementById('mobileNumber')?.value;
        
        if (!this.validateMobileNumber(mobile)) {
            this.showMessage('Please enter a valid 10-digit mobile number', 'error');
            return;
        }

        this.showLoading(true);

        try {
            // Simulate API call
            await new Promise(resolve => setTimeout(resolve, 2000));
            
            // Show mock data
            this.showProductStatus(this.getMockProductData());
        } catch (error) {
            this.showMessage('Failed to check product status', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    showProductStatus(data) {
        const statusSummary = document.getElementById('statusSummary');
        const productsList = document.getElementById('productsList');
        const noProducts = document.getElementById('noProducts');
        const aiSuggestions = document.getElementById('aiSuggestions');

        if (data.products && data.products.length > 0) {
            // Show status summary
            if (statusSummary) {
                statusSummary.classList.remove('hidden');
                statusSummary.classList.add('fade-in');
                
                const soldCount = data.products.filter(p => p.status === 'sold').length;
                const pendingCount = data.products.filter(p => p.status === 'pending').length;
                
                document.getElementById('soldCount').textContent = soldCount;
                document.getElementById('pendingCount').textContent = pendingCount;
                document.getElementById('totalCount').textContent = data.products.length;
            }

            // Show products list
            if (productsList) {
                productsList.classList.remove('hidden');
                productsList.innerHTML = this.generateProductsHTML(data.products);
                productsList.classList.add('fade-in');
            }

            // Hide no products message
            if (noProducts) {
                noProducts.classList.add('hidden');
            }

            // Show AI suggestions
            if (aiSuggestions) {
                aiSuggestions.classList.remove('hidden');
                aiSuggestions.classList.add('fade-in');
                this.generateAISuggestions(data.products);
            }
        } else {
            // Show no products message
            if (noProducts) {
                noProducts.classList.remove('hidden');
                noProducts.classList.add('fade-in');
            }

            // Hide other sections
            if (statusSummary) statusSummary.classList.add('hidden');
            if (productsList) productsList.classList.add('hidden');
            if (aiSuggestions) aiSuggestions.classList.add('hidden');
        }
    }

    generateProductsHTML(products) {
        return products.map(product => `
            <div class="product-card stagger-item">
                <div class="flex justify-between items-start mb-4">
                    <h4 class="text-lg font-semibold text-gray-800">${product.name}</h4>
                    <span class="${product.status === 'sold' ? 'status-sold' : 'status-pending'}">
                        ${product.status === 'sold' ? 'Sold ✅' : 'Pending ⏳'}
                    </span>
                </div>
                <p class="text-gray-600 mb-3">${product.description}</p>
                <div class="flex justify-between items-center text-sm text-gray-500">
                    <span>Created: ${new Date(product.created_at).toLocaleDateString()}</span>
                    <span>ID: #${product.id}</span>
                </div>
                ${product.suggestions ? `
                    <div class="mt-3 p-3 bg-blue-50 rounded-lg">
                        <p class="text-sm text-blue-800"><strong>💡 Suggestion:</strong> ${product.suggestions}</p>
                    </div>
                ` : ''}
            </div>
        `).join('');
    }

    generateAISuggestions(products) {
        const pendingProducts = products.filter(p => p.status === 'pending');
        const suggestionsContent = document.getElementById('suggestionsContent');
        
        if (pendingProducts.length > 0) {
            const suggestions = [
                'Try adding better photos to attract more customers',
                'Consider offering competitive pricing for better sales',
                'Highlight the freshness and quality of your products',
                'Respond quickly to customer inquiries',
                'Add detailed product descriptions'
            ];
            
            suggestionsContent.innerHTML = suggestions.map(suggestion => `
                <div class="flex items-start space-x-3 p-3 bg-yellow-50 rounded-lg">
                    <span class="text-xl">💡</span>
                    <p class="text-gray-700">${suggestion}</p>
                </div>
            `).join('');
        } else {
            suggestionsContent.innerHTML = `
                <div class="text-center text-gray-600">
                    <p>🎉 All your products are sold! Great job!</p>
                </div>
            `;
        }
    }

    getMockProductData() {
        return {
            products: [
                {
                    id: 1,
                    name: "Fresh Tomatoes",
                    description: "Fresh, high-quality tomatoes from local farm. Perfect for your daily needs!",
                    status: "pending",
                    created_at: "2024-01-15T10:30:00Z",
                    suggestions: "Try adding better photos and highlighting freshness"
                },
                {
                    id: 2,
                    name: "Organic Rice",
                    description: "Premium quality organic rice, perfect for daily meals",
                    status: "sold",
                    created_at: "2024-01-14T15:45:00Z"
                },
                {
                    id: 3,
                    name: "Sweet Mangoes",
                    description: "Sweet and juicy mangoes from organic farms",
                    status: "pending",
                    created_at: "2024-01-13T09:20:00Z",
                    suggestions: "Consider competitive pricing and quick delivery"
                }
            ]
        };
    }

    // Utility Methods
    validateMobileNumber(mobile) {
        const mobileRegex = /^[6-9]\d{9}$/;
        return mobileRegex.test(mobile);
    }

    updateLanguageDisplay() {
        const welcomeText = document.querySelector('h2');
        if (welcomeText) {
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
            
            welcomeText.innerHTML = `${greetings[this.currentLanguage]} Welcome! स्वागत है!`;
        }
    }

    showMessage(message, type = 'info') {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());

        // Create new message
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type} fade-in`;
        messageDiv.textContent = message;

        // Insert at the top of main content
        const main = document.querySelector('main');
        if (main) {
            main.insertBefore(messageDiv, main.firstChild);
        }

        // Auto remove after 5 seconds
        setTimeout(() => {
            messageDiv.classList.add('fade-out');
            setTimeout(() => messageDiv.remove(), 300);
        }, 5000);
    }

    showLoading(show) {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            if (show) {
                loadingOverlay.classList.remove('hidden');
                loadingOverlay.classList.add('fade-in');
            } else {
                loadingOverlay.classList.add('fade-out');
                setTimeout(() => {
                    loadingOverlay.classList.add('hidden');
                    loadingOverlay.classList.remove('fade-out');
                }, 300);
            }
        }
    }

    addRippleEffect(button, event) {
        const ripple = document.createElement('span');
        ripple.classList.add('ripple');
        ripple.style.left = event.clientX - button.offsetLeft + 'px';
        ripple.style.top = event.clientY - button.offsetTop + 'px';
        
        button.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }

    initializeAnimations() {
        // Add fade-in animation to elements with data-aos
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                }
            });
        }, observerOptions);

        document.querySelectorAll('[data-aos]').forEach(el => {
            observer.observe(el);
        });
    }

    addEmojiWaveAnimation() {
        // Add wave animation to emojis
        const emojis = document.querySelectorAll('span');
        emojis.forEach(emoji => {
            if (emoji.textContent.includes('🌾') || emoji.textContent.includes('🌞')) {
                emoji.classList.add('emoji-wave');
            }
        });
    }

    async testAPIConnection() {
        try {
            const response = await fetch(`${this.API_BASE_URL}/`);
            const data = await response.json();
            console.log('✅ API Connected:', data);
            
            // Show success message
            if (data.status === 'healthy') {
                this.showMessage('🌾 AgriVoice API is connected and running!', 'success');
            }
        } catch (error) {
            console.error('❌ API Connection failed:', error);
            this.showMessage('⚠️ API connection failed. Please check if the server is running.', 'error');
        }
    }
}

// Initialize AgriVoice when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AgriVoice();
}); 