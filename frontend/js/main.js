// AgriVoice Main JavaScript Utilities
// Additional utility functions and helpers

// API Utilities
class APIUtils {
    static async makeRequest(endpoint, options = {}) {
        const baseURL = 'http://localhost:8000';
        const url = `${baseURL}${endpoint}`;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...options
        };

        try {
            const response = await fetch(url, defaultOptions);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }

    static async uploadAudio(audioBlob, language) {
        const formData = new FormData();
        formData.append('audio', audioBlob);
        formData.append('language', language);

        return this.makeRequest('/api/transcribe', {
            method: 'POST',
            body: formData,
            headers: {} // Let browser set content-type for FormData
        });
    }

    static async saveProduct(productData) {
        return this.makeRequest('/api/store-product', {
            method: 'POST',
            body: JSON.stringify(productData)
        });
    }

    static async getStatus(mobile) {
        return this.makeRequest('/api/check-status', {
            method: 'POST',
            body: JSON.stringify({ mobile })
        });
    }
}

// UI Utilities
class UIUtils {
    static showMessage(message, type = 'info', duration = 3000) {
        const messageEl = document.createElement('div');
        messageEl.className = `message message-${type}`;
        messageEl.textContent = message;
        
        // Add styles
        messageEl.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;

        // Set background color based on type
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        messageEl.style.backgroundColor = colors[type] || colors.info;

        document.body.appendChild(messageEl);

        // Remove after duration
        setTimeout(() => {
            messageEl.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => messageEl.remove(), 300);
        }, duration);
    }

    static showLoading(show = true) {
        let overlay = document.getElementById('loadingOverlay');
        
        if (!overlay) {
            overlay = document.createElement('div');
            overlay.id = 'loadingOverlay';
            overlay.className = 'loading-overlay';
            overlay.innerHTML = `
                <div class="loading-spinner"></div>
                <p>Loading...</p>
            `;
            document.body.appendChild(overlay);
        }

        if (show) {
            overlay.classList.remove('hidden');
        } else {
            overlay.classList.add('hidden');
        }
    }

    static formatCurrency(amount, currency = '₹') {
        return `${currency}${parseFloat(amount).toLocaleString('en-IN')}`;
    }

    static formatDate(date) {
        return new Date(date).toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }

    static animateElement(element, animation) {
        element.style.animation = animation;
        element.addEventListener('animationend', () => {
            element.style.animation = '';
        }, { once: true });
    }
}

// Validation Utilities
class ValidationUtils {
    static validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    static validatePhone(phone) {
        const phoneRegex = /^[6-9]\d{9}$/;
        return phoneRegex.test(phone);
    }

    static validatePassword(password) {
        return password.length >= 6;
    }

    static validateProductData(data) {
        const errors = [];
        
        if (!data.name || data.name.trim().length === 0) {
            errors.push('Product name is required');
        }
        
        if (!data.quantity || parseFloat(data.quantity) <= 0) {
            errors.push('Valid quantity is required');
        }
        
        if (!data.price || parseFloat(data.price) <= 0) {
            errors.push('Valid price is required');
        }

        return {
            isValid: errors.length === 0,
            errors
        };
    }
}

// Storage Utilities
class StorageUtils {
    static setItem(key, value) {
        try {
            localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }

    static getItem(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return defaultValue;
        }
    }

    static removeItem(key) {
        try {
            localStorage.removeItem(key);
        } catch (error) {
            console.error('Error removing from localStorage:', error);
        }
    }

    static clear() {
        try {
            localStorage.clear();
        } catch (error) {
            console.error('Error clearing localStorage:', error);
        }
    }
}

// Audio Utilities
class AudioUtils {
    static async getAudioLevel(stream) {
        const audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const analyser = audioContext.createAnalyser();
        const source = audioContext.createMediaStreamSource(stream);
        
        source.connect(analyser);
        analyser.fftSize = 256;
        
        const dataArray = new Uint8Array(analyser.frequencyBinCount);
        
        return new Promise((resolve) => {
            const getLevel = () => {
                analyser.getByteFrequencyData(dataArray);
                const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
                resolve(average / 255);
            };
            getLevel();
        });
    }

    static formatDuration(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
}

// Export utilities to global scope
window.APIUtils = APIUtils;
window.UIUtils = UIUtils;
window.ValidationUtils = ValidationUtils;
window.StorageUtils = StorageUtils;
window.AudioUtils = AudioUtils;

// Add CSS animations for messages
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style); 