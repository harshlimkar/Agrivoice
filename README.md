# 🌾 AgriVoice - Voice-Based Product Catalog for Indian Farmers

A full-stack voice-based product catalog application designed specifically for Indian farmers. Farmers can record their product descriptions in their native language, and the system will transcribe, generate AI descriptions, and store their products with intelligent suggestions.

## 🚀 Features

- **Voice Recording**: Record product descriptions in multiple Indian languages
- **Speech Recognition**: Automatic transcription of voice to text
- **AI-Powered Descriptions**: Generate enhanced product descriptions using Google Gemini AI
- **Multi-language Support**: English, Hindi, Tamil, Telugu, Kannada, Malayalam, Gujarati, Marathi, Bengali, Odia, Punjabi
- **Product Management**: Store and manage products with categories and pricing
- **Status Tracking**: Track product status (pending, sold, expired, cancelled)
- **Analytics**: View sales statistics and performance metrics
- **Responsive UI**: Modern, mobile-friendly interface

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Database (via Supabase)
- **Google Gemini AI**: AI-powered description generation
- **Speech Recognition**: Voice-to-text conversion
- **Pydantic**: Data validation and serialization

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Interactive voice recording and UI
- **Web Audio API**: Voice recording functionality
- **Fetch API**: Backend communication

### Database
- **Supabase**: PostgreSQL database with real-time features
- **Row Level Security**: Secure data access
- **Full-text Search**: Advanced product search capabilities

## 📁 Project Structure

```
TECHY-CRACKS-main/
├── backend/                 # FastAPI backend
│   ├── main.py             # Main application entry point
│   ├── routes/             # API route handlers
│   ├── utils/              # Utility functions
│   ├── models/             # Pydantic models
│   └── requirements.txt    # Python dependencies
├── frontend/               # Frontend files
│   ├── index.html          # Main application page
│   ├── register.html       # Farmer registration
│   ├── upload.html         # Product upload
│   ├── status.html         # Product status
│   ├── assets/             # Images and fonts
│   └── test.html           # API testing page
├── supabase/               # Database schema
│   └── schema.sql          # PostgreSQL schema
├── .env                    # Environment variables
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, for development)
- Supabase account
- Google Gemini AI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/agrivoice.git
   cd agrivoice
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Set up database**
   - Create a Supabase project
   - Run the schema.sql file in your Supabase SQL editor
   - Update your .env file with Supabase credentials

5. **Start the backend server**
   ```bash
   python main.py
   # or
   python -m uvicorn main:app --reload
   ```

6. **Open the frontend**
   - Open `frontend/index.html` in your browser
   - Or serve it using a local server

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# Server Configuration
HOST=127.0.0.1
PORT=8000
```

### API Endpoints

- `GET /` - Health check
- `POST /transcribe` - Transcribe voice to text
- `POST /generate-description` - Generate AI description
- `POST /store` - Store product in database
- `POST /check-status` - Check product status
- `GET /categories` - Get product categories
- `GET /test` - Test endpoint

## 🎯 Usage

1. **Register**: Farmers register with their mobile number and preferred language
2. **Record**: Record product description in their native language
3. **Review**: Review transcribed text and AI-generated description
4. **Store**: Save product with pricing and category information
5. **Track**: Monitor product status and sales analytics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for intelligent text generation
- Supabase for database infrastructure
- FastAPI for the robust backend framework
- Indian farmers for inspiration and feedback

## 📞 Support

For support, email support@agrivoice.com or create an issue in this repository.

---

**Made with ❤️ for Indian Farmers** 