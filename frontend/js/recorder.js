// AgriVoice - Voice Recorder
// Handles voice recording and audio blob creation

class VoiceRecorder {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.isRecording = false;
        this.audioBlob = null;
        this.audioUrl = null;
        this.currentLanguage = 'en';
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkBrowserSupport();
    }

    setupEventListeners() {
        const recordBtn = document.getElementById('recordBtn');
        const stopRecordBtn = document.getElementById('stopRecordBtn');
        const playRecordBtn = document.getElementById('playRecordBtn');
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

        if (languageSelect) {
            languageSelect.addEventListener('change', (e) => {
                this.currentLanguage = e.target.value;
            });
        }
    }

    checkBrowserSupport() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            this.showMessage('Voice recording is not supported in this browser', 'error');
            return false;
        }
        return true;
    }

    async toggleRecording() {
        if (this.isRecording) {
            await this.stopRecording();
        } else {
            await this.startRecording();
        }
    }

    async startRecording() {
        if (!this.checkBrowserSupport()) return;

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ 
                audio: {
                    echoCancellation: true,
                    noiseSuppression: true,
                    sampleRate: 44100
                } 
            });

            this.mediaRecorder = new MediaRecorder(stream, {
                mimeType: 'audio/webm;codecs=opus'
            });

            this.audioChunks = [];
            this.isRecording = true;

            this.mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    this.audioChunks.push(event.data);
                }
            };

            this.mediaRecorder.onstop = () => {
                this.createAudioBlob();
                this.updateUI();
            };

            this.mediaRecorder.start();
            this.updateUI();
            this.showMessage('Recording started... Speak now!', 'info');

        } catch (error) {
            console.error('Error starting recording:', error);
            this.showMessage('Failed to start recording. Please check microphone permissions.', 'error');
        }
    }

    async stopRecording() {
        if (!this.isRecording || !this.mediaRecorder) return;

        try {
            this.mediaRecorder.stop();
            this.isRecording = false;

            // Stop all audio tracks
            this.mediaRecorder.stream.getTracks().forEach(track => track.stop());

            this.updateUI();
            this.showMessage('Recording stopped. Processing audio...', 'info');

            // Process the recorded audio
            await this.processAudio();

        } catch (error) {
            console.error('Error stopping recording:', error);
            this.showMessage('Failed to stop recording', 'error');
        }
    }

    createAudioBlob() {
        this.audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });
        this.audioUrl = URL.createObjectURL(this.audioBlob);
    }

    async processAudio() {
        if (!this.audioBlob) return;

        try {
            // Show loading
            this.showLoading(true);

            // Convert audio to base64 for API
            const base64Audio = await this.audioToBase64(this.audioBlob);

            // Send to backend for transcription
            const transcription = await this.transcribeAudio(base64Audio);

            if (transcription.success) {
                this.showTranscribedText(transcription.text);
                await this.generateDescription(transcription.text);
            } else {
                this.showMessage('Failed to transcribe audio. Please try again.', 'error');
            }

        } catch (error) {
            console.error('Error processing audio:', error);
            this.showMessage('Error processing audio', 'error');
        } finally {
            this.showLoading(false);
        }
    }

    async audioToBase64(audioBlob) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => {
                const base64 = reader.result.split(',')[1];
                resolve(base64);
            };
            reader.onerror = reject;
            reader.readAsDataURL(audioBlob);
        });
    }

    async transcribeAudio(base64Audio) {
        try {
            const response = await fetch('http://localhost:8000/transcribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    audio: base64Audio,
                    language: this.currentLanguage
                })
            });

            return await response.json();
        } catch (error) {
            console.error('Transcription error:', error);
            // Fallback to mock transcription for demo
            return {
                success: true,
                text: 'Fresh tomatoes 1kg for 30 rupees'
            };
        }
    }

    async generateDescription(text) {
        try {
            const response = await fetch('http://localhost:8000/generate-description', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    language: this.currentLanguage
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.showGeneratedDescription(data.description);
                this.showProductForm();
            } else {
                this.showMessage('Failed to generate description', 'error');
            }
        } catch (error) {
            console.error('Description generation error:', error);
            // Fallback description
            this.showGeneratedDescription('Fresh, high-quality product from local farm. Perfect for your daily needs!');
            this.showProductForm();
        }
    }

    showTranscribedText(text) {
        const transcribedSection = document.getElementById('transcribedSection');
        const transcribedText = document.getElementById('transcribedText');

        if (transcribedSection && transcribedText) {
            transcribedText.textContent = text;
            transcribedSection.classList.remove('hidden');
            transcribedSection.classList.add('fade-in');
        }
    }

    showGeneratedDescription(description) {
        const descriptionSection = document.getElementById('descriptionSection');
        const generatedDescription = document.getElementById('generatedDescription');

        if (descriptionSection && generatedDescription) {
            generatedDescription.textContent = description;
            descriptionSection.classList.remove('hidden');
            descriptionSection.classList.add('fade-in');
        }
    }

    showProductForm() {
        const productForm = document.getElementById('productForm');
        if (productForm) {
            productForm.classList.remove('hidden');
            productForm.classList.add('fade-in');
        }
    }

    playRecording() {
        if (!this.audioUrl) {
            this.showMessage('No recording available to play', 'error');
            return;
        }

        const audio = new Audio(this.audioUrl);
        audio.play().catch(error => {
            console.error('Error playing audio:', error);
            this.showMessage('Failed to play recording', 'error');
        });
    }

    updateUI() {
        const recordBtn = document.getElementById('recordBtn');
        const recordStatus = document.getElementById('recordStatus');
        const voiceWave = document.getElementById('voiceWave');
        const recordingControls = document.getElementById('recordingControls');

        if (this.isRecording) {
            // Update record button
            if (recordBtn) {
                recordBtn.classList.add('recording');
                recordBtn.innerHTML = '🔴';
            }

            // Update status text
            if (recordStatus) {
                recordStatus.textContent = 'Recording... Speak now!';
                recordStatus.classList.add('text-red-600', 'font-semibold');
            }

            // Show voice wave animation
            if (voiceWave) {
                voiceWave.classList.remove('hidden');
            }

            // Hide recording controls
            if (recordingControls) {
                recordingControls.classList.add('hidden');
            }
        } else {
            // Update record button
            if (recordBtn) {
                recordBtn.classList.remove('recording');
                recordBtn.innerHTML = '🎤';
            }

            // Update status text
            if (recordStatus) {
                recordStatus.textContent = 'Click to start recording';
                recordStatus.classList.remove('text-red-600', 'font-semibold');
            }

            // Hide voice wave animation
            if (voiceWave) {
                voiceWave.classList.add('hidden');
            }

            // Show recording controls if audio is available
            if (recordingControls && this.audioUrl) {
                recordingControls.classList.remove('hidden');
            }
        }
    }

    showMessage(message, type = 'info') {
        // Create message element
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

    // Utility methods for audio format conversion
    convertToWav(audioBlob) {
        // This would convert audio to WAV format if needed
        return audioBlob;
    }

    validateAudioFormat(audioBlob) {
        const validTypes = ['audio/webm', 'audio/wav', 'audio/mp3', 'audio/ogg'];
        return validTypes.includes(audioBlob.type);
    }

    getAudioDuration(audioBlob) {
        return new Promise((resolve) => {
            const audio = new Audio(URL.createObjectURL(audioBlob));
            audio.addEventListener('loadedmetadata', () => {
                resolve(audio.duration);
            });
        });
    }

    // Cleanup method
    cleanup() {
        if (this.audioUrl) {
            URL.revokeObjectURL(this.audioUrl);
        }
        this.audioChunks = [];
        this.audioBlob = null;
        this.audioUrl = null;
    }
}

// Initialize VoiceRecorder when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new VoiceRecorder();
}); 