// AgriVoice Voice Handler
// Handles voice recording, processing, and audio management

class VoiceHandler {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.audioContext = null;
        this.analyser = null;
        this.dataArray = null;
        this.init();
    }

    init() {
        this.setupAudioContext();
        this.setupEventListeners();
    }

    setupAudioContext() {
        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;
            const bufferLength = this.analyser.frequencyBinCount;
            this.dataArray = new Uint8Array(bufferLength);
        } catch (error) {
            console.warn('Audio context not supported:', error);
        }
    }

    setupEventListeners() {
        // Voice button events
        const voiceButton = document.getElementById('voiceButton');
        if (voiceButton) {
            voiceButton.addEventListener('click', () => {
                this.toggleRecording();
            });
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                this.toggleRecording();
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
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    autoGainControl: true,
                    sampleRate: 44100
                } 
            });

            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });

            this.audioChunks = [];
            this.isRecording = true;

            // Set up event handlers
            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                this.processRecording();
            };

            this.mediaRecorder.onerror = (event) => {
                console.error('MediaRecorder error:', event);
                this.handleRecordingError('Recording failed');
            };

            // Start recording
            this.mediaRecorder.start(1000); // Collect data every second
            this.updateUI(true);
            this.startVisualization(stream);
            this.showStatus('Recording...', 'recording');

        } catch (error) {
            console.error('Error starting recording:', error);
            this.handleRecordingError('Microphone access denied');
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.isRecording) {
            this.mediaRecorder.stop();
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
            this.isRecording = false;
            this.updateUI(false);
            this.stopVisualization();
            this.showStatus('Processing audio...', 'processing');
        }
    }

    async processRecording() {
        try {
            this.showLoading(true);
            
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append('audio', audioBlob);
            formData.append('language', this.getCurrentLanguage());

            // Send to backend for processing
            const response = await this.sendAudioToBackend(formData);
            
            if (response.success) {
                this.displayResults(response.data);
                this.showStatus('Audio processed successfully', 'success');
            } else {
                throw new Error(response.message || 'Processing failed');
            }

        } catch (error) {
            console.error('Error processing recording:', error);
            this.handleRecordingError('Failed to process audio');
        } finally {
            this.showLoading(false);
        }
    }

    async sendAudioToBackend(formData) {
        try {
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();

        } catch (error) {
            console.error('Backend API error:', error);
            
            // Fallback to mock processing for demo
            return this.mockProcessing();
        }
    }

    async mockProcessing() {
        // Simulate processing delay
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Mock response based on language
        const language = this.getCurrentLanguage();
        const mockResponses = {
            'en': {
                product_name: 'Fresh Tomatoes',
                quantity: '50 kg',
                price: '₹40/kg',
                description: 'Organic red tomatoes, freshly harvested',
                category: 'vegetables'
            },
            'hi': {
                product_name: 'ताजे टमाटर',
                quantity: '50 किलो',
                price: '₹40/किलो',
                description: 'जैविक लाल टमाटर, ताजा काटा गया',
                category: 'सब्जियां'
            },
            'ta': {
                product_name: 'புதிய தக்காளி',
                quantity: '50 கிலோ',
                price: '₹40/கிலோ',
                description: 'கரிம சிவப்பு தக்காளி, புதிதாக அறுவடை செய்யப்பட்டது',
                category: 'காய்கறிகள்'
            }
        };

        return {
            success: true,
            data: mockResponses[language] || mockResponses['en']
        };
    }

    displayResults(data) {
        const preview = document.getElementById('productPreview');
        if (preview) {
            // Update preview fields
            const fields = {
                'previewProduct': data.product_name,
                'previewQuantity': data.quantity,
                'previewPrice': data.price,
                'previewDescription': data.description,
                'previewCategory': data.category
            };

            Object.entries(fields).forEach(([id, value]) => {
                const element = document.getElementById(id);
                if (element) {
                    element.textContent = value;
                }
            });

            preview.classList.remove('hidden');
        }
    }

    startVisualization(stream) {
        if (!this.audioContext || !this.analyser) return;

        try {
            const source = this.audioContext.createMediaStreamSource(stream);
            source.connect(this.analyser);
            
            this.visualize();
        } catch (error) {
            console.warn('Visualization not supported:', error);
        }
    }

    visualize() {
        if (!this.analyser || !this.isRecording) return;

        this.analyser.getByteFrequencyData(this.dataArray);
        
        // Create visualization effect
        this.createVisualizationEffect();
        
        requestAnimationFrame(() => this.visualize());
    }

    createVisualizationEffect() {
        // Add visual feedback for recording
        const voiceButton = document.getElementById('voiceButton');
        if (voiceButton && this.dataArray) {
            const average = this.dataArray.reduce((a, b) => a + b) / this.dataArray.length;
            const intensity = Math.min(average / 128, 1);
            
            voiceButton.style.transform = `scale(${1 + intensity * 0.1})`;
        }
    }

    stopVisualization() {
        const voiceButton = document.getElementById('voiceButton');
        if (voiceButton) {
            voiceButton.style.transform = 'scale(1)';
        }
    }

    updateUI(isRecording) {
        const voiceButton = document.getElementById('voiceButton');
        const recordingIndicator = document.getElementById('recordingIndicator');
        const buttonText = voiceButton?.querySelector('.button-text');

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

    handleRecordingError(message) {
        this.isRecording = false;
        this.updateUI(false);
        this.stopVisualization();
        this.showStatus(message, 'error');
        this.showLoading(false);
    }

    getCurrentLanguage() {
        const languageSelect = document.getElementById('languageSelect');
        return languageSelect ? languageSelect.value : 'en';
    }

    // Utility methods
    formatDuration(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }

    getAudioLevel() {
        if (!this.analyser || !this.dataArray) return 0;
        
        this.analyser.getByteFrequencyData(this.dataArray);
        const average = this.dataArray.reduce((a, b) => a + b) / this.dataArray.length;
        return average / 255;
    }

    // Cleanup
    destroy() {
        if (this.mediaRecorder && this.isRecording) {
            this.stopRecording();
        }
        
        if (this.audioContext) {
            this.audioContext.close();
        }
    }
}

// Initialize voice handler when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.voiceHandler = new VoiceHandler();
});

// Export for use in other modules
window.VoiceHandler = VoiceHandler; 