// AgriVoice Main Application JavaScript

class AgriVoiceApp {
    constructor() {
        this.currentLanguage = 'en';
        this.isRecording = false;
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.apiBaseUrl = 'http://127.0.0.1:8000/api';
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadUserPreferences();
        this.updateUI();
    }

    setupEventListeners() {
        // Language selector
        const languageSelect = document.getElementById('languageSelect');
        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.currentLanguage = e.target.value;
                this.updateLanguage();
            });
        }

        // Voice button
        const voiceButton = document.getElementById('voiceButton');
        if (voiceButton) {
            voiceButton.addEventListener('click', () => {
                this.toggleRecording();
            });
        }

        // Save product button
        const saveProductBtn = document.getElementById('saveProduct');
        if (saveProductBtn) {
            saveProductBtn.addEventListener('click', () => {
                this.saveProduct();
            });
        }

        // Record again button
        const recordAgainBtn = document.getElementById('recordAgain');
        if (recordAgainBtn) {
            recordAgainBtn.addEventListener('click', () => {
                this.resetRecording();
            });
        }

        // Manual form inputs
        this.setupFormListeners();
    }

    setupFormListeners() {
        const formInputs = [
            'productName',
            'productQuantity', 
            'productPrice',
            'productDescription',
            'productCategory'
        ];

        formInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.addEventListener('input', () => {
                    this.updatePreview();
                });
            }
        });
    }

    async toggleRecording() {
        if (this.isRecording) {
            this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            this.mediaRecorder = new MediaRecorder(stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                this.processAudio();
            };

            this.mediaRecorder.start();
            this.isRecording = true;
            this.updateRecordingUI(true);
            this.showStatus('Recording...', 'recording');

        } catch (error) {
            console.error('Error accessing microphone:', error);
            this.showStatus('Microphone access denied', 'error');
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            this.isRecording = false;
            this.updateRecordingUI(false);
            this.showStatus('Processing audio...', 'processing');
        }
    }

    async processAudio() {
        try {
            this.showLoading(true);
            
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/wav' });
            const base64Audio = await this.blobToBase64(audioBlob);

            // Call the actual backend API
            const response = await fetch(`${this.apiBaseUrl}/complete-voice-process`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    audio_data: base64Audio,
                    language: this.currentLanguage,
                    farmer_mobile: 'demo_user'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.success) {
                this.displayProductPreview({
                    product_name: result.product,
                    quantity: result.quantity,
                    price: result.price,
                    description: result.description,
                    category: 'vegetables'
                });
                this.showStatus('Audio processed successfully', 'success');
            } else {
                throw new Error('Processing failed');
            }

        } catch (error) {
            console.error('Error processing audio:', error);
            this.showStatus('Error processing audio', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async blobToBase64(blob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(blob);
        });
    }

    displayProductPreview(data) {
        const preview = document.getElementById('productPreview');
        if (preview) {
            document.getElementById('previewProduct').textContent = data.product_name;
            document.getElementById('previewQuantity').textContent = data.quantity;
            document.getElementById('previewPrice').textContent = data.price;
            document.getElementById('previewDescription').textContent = data.description;
            document.getElementById('previewCategory').textContent = data.category;
            
            preview.classList.remove('hidden');
        }
    }

    updatePreview() {
        const name = document.getElementById('productName')?.value || '';
        const quantity = document.getElementById('productQuantity')?.value || '';
        const price = document.getElementById('productPrice')?.value || '';
        const description = document.getElementById('productDescription')?.value || '';
        const category = document.getElementById('productCategory')?.value || '';

        if (name || quantity || price || description || category) {
            const preview = document.getElementById('productPreview');
            if (preview) {
                document.getElementById('previewProduct').textContent = name || '-';
                document.getElementById('previewQuantity').textContent = quantity ? `${quantity} kg` : '-';
                document.getElementById('previewPrice').textContent = price ? `₹${price}/kg` : '-';
                document.getElementById('previewDescription').textContent = description || '-';
                document.getElementById('previewCategory').textContent = category || '-';
                
                preview.classList.remove('hidden');
            }
        }
    }

    async saveProduct() {
        try {
            this.showStatus('Saving product...', 'processing');
            
            // Collect form data
            const productData = {
                name: document.getElementById('productName')?.value || document.getElementById('previewProduct')?.textContent,
                quantity: document.getElementById('productQuantity')?.value || document.getElementById('previewQuantity')?.textContent,
                price: document.getElementById('productPrice')?.value || document.getElementById('previewPrice')?.textContent,
                description: document.getElementById('productDescription')?.value || document.getElementById('previewDescription')?.textContent,
                category: document.getElementById('productCategory')?.value || document.getElementById('previewCategory')?.textContent,
                language: this.currentLanguage
            };

            // Call the actual backend API to save product
            const response = await fetch(`${this.apiBaseUrl}/store-product`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    product_info: {
                        product: productData.name,
                        quantity: productData.quantity,
                        price: productData.price
                    },
                    ai_response: {
                        description: productData.description,
                        price_range: "Market price",
                        where_to_sell: "Local market",
                        selling_tip: "Highlight freshness"
                    },
                    transcribed_text: `${productData.name} ${productData.quantity} ${productData.price}`,
                    language: this.currentLanguage,
                    farmer_mobile: 'demo_user'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.success) {
                this.showStatus('Product saved successfully!', 'success');
                this.resetForm();
                
                // Redirect to dashboard after a delay
                setTimeout(() => {
                    window.location.href = 'dashboard.html';
                }, 2000);
            } else {
                throw new Error('Failed to save product');
            }

        } catch (error) {
            console.error('Error saving product:', error);
            this.showStatus('Error saving product', 'error');
        }
    }

    resetRecording() {
        this.audioChunks = [];
        this.isRecording = false;
        this.updateRecordingUI(false);
        this.showStatus('Ready to record', 'ready');
        
        const preview = document.getElementById('productPreview');
        if (preview) {
            preview.classList.add('hidden');
        }
    }

    resetForm() {
        const formInputs = [
            'productName',
            'productQuantity',
            'productPrice', 
            'productDescription',
            'productCategory'
        ];

        formInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.value = '';
            }
        });

        const preview = document.getElementById('productPreview');
        if (preview) {
            preview.classList.add('hidden');
        }
    }

    updateRecordingUI(isRecording) {
        const voiceButton = document.getElementById('voiceButton');
        const recordingIndicator = document.getElementById('recordingIndicator');
        const buttonText = document.getElementById('buttonText');

        if (voiceButton) {
            if (isRecording) {
                voiceButton.classList.add('recording');
                if (buttonText) buttonText.textContent = 'Click to Stop Recording';
            } else {
                voiceButton.classList.remove('recording');
                if (buttonText) buttonText.textContent = 'Click to Start Recording';
            }
        }

        if (recordingIndicator) {
            if (isRecording) {
                recordingIndicator.classList.remove('hidden');
            } else {
                recordingIndicator.classList.add('hidden');
            }
        }
    }

    showStatus(message, type = 'info') {
        const statusElement = document.getElementById('voiceStatus');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `status-text ${type}`;
        }
    }

    showLoading(show) {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            if (show) {
                loadingOverlay.classList.remove('hidden');
            } else {
                loadingOverlay.classList.add('hidden');
            }
        }
    }

    updateLanguage() {
        // Update UI based on selected language
        console.log('Language changed to:', this.currentLanguage);
        
        // Save preference
        localStorage.setItem('agrivoice_language', this.currentLanguage);
    }

    loadUserPreferences() {
        const savedLanguage = localStorage.getItem('agrivoice_language');
        if (savedLanguage) {
            this.currentLanguage = savedLanguage;
            const languageSelect = document.getElementById('languageSelect');
            if (languageSelect) {
                languageSelect.value = savedLanguage;
            }
        }
    }

    updateUI() {
        // Update any UI elements that need initialization
        this.showStatus('Ready to record', 'ready');
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AgriVoiceApp();
});

// Export for use in other modules
window.AgriVoiceApp = AgriVoiceApp; 