# AgriVoice 🌾

**Multilingual AI-powered voice product catalog for Indian farmers**

AgriVoice is a comprehensive platform that enables Indian farmers to create product listings using voice input in their native language. The system uses AI to transcribe speech, extract product information, and generate intelligent suggestions for better sales.

## 🌟 Features

- **Multilingual Voice Input**: Support for 11 Indian languages
- **AI-Powered Processing**: Gemini AI for intelligent product analysis
- **Smart Suggestions**: Price ranges, market recommendations, selling tips
- **Real-time Database**: Supabase for reliable data storage
- **Responsive UI**: Modern, mobile-friendly interface
- **Voice Recording**: Browser-based audio capture and processing

## 🗂️ Project Structure

```
agri-voice-product-app/
├── frontend/                    # Frontend application
│   ├── index.html              # Main UI with voice input
│   ├── login.html              # Farmer login/register page
│   ├── dashboard.html          # Shows product listings and tips
│   ├── app.js                  # Handles UI logic, API calls, language handling
│   ├── voiceHandler.js         # Manages speech recognition & mic access
│   ├── langSupport.js          # Handles multilingual text rendering
│   ├── styles/
│   │   ├── main.css           # Animations, alignment, colors, responsiveness
│   │   └── theme.css          # Theme settings per language/region
│   └── assets/
│       ├── logo.svg
│       ├── icons/
│       └── illustrations/
│
├── backend/                    # Python FastAPI backend
│   ├── main.py                # FastAPI app for routing and integration
│   ├── whisper_transcribe.py  # Converts voice to text (multilingual)
│   ├── parse_product.py       # Extracts product, quantity, price
│   ├── gemini_ai.py          # Gemini API call for suggestions & description
│   ├── translate_module.py    # Optional: Translate output for language consistency
│   ├── supabase_connector.py  # Handles storing/fetching data to/from Supabase
│   └── utils/
│       └── helpers.py         # Common helper functions
│
├── supabase_config/           # Supabase setup
│   ├── schema.sql             # Supabase table schema
│   └── setup_supabase.sh      # Script to initialize project
│
├── .env                       # Gemini + Supabase keys
├── requirements.txt           # Python dependencies
├── README.md                 # Project overview
└── LICENSE
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 14+ (for Supabase CLI)
- Supabase account
- Gemini AI API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd agri-voice-product-app
```

2. **Set up Supabase**
```bash
cd supabase_config
chmod +x setup_supabase.sh
./setup_supabase.sh
```

3. **Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp env.example .env
# Edit .env with your API keys
```

5. **Start the backend server**
```bash
cd backend
python start_server.py
```

6. **Start the frontend**
```bash
cd frontend
python -m http.server 3000
```

7. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Gemini AI API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Supabase Configuration
SUPABASE_URL=your_supabase_project_url_here
SUPABASE_ANON_KEY=your_supabase_anon_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Supported Languages

| Code | Language | Example |
|------|----------|---------|
| `en` | English | "I have 10 kg of tomatoes" |
| `hi` | Hindi | "मेरे पास 10 किलो टमाटर हैं" |
| `ta` | Tamil | "என்னிடம் 10 கிலோ தக்காளிகள் உள்ளன" |
| `te` | Telugu | "నా వద్ద 10 కిలోల టమాటాలు ఉన్నాయి" |
| `kn` | Kannada | "ನನ್ನ ಬಳಿ 10 ಕಿಲೋ ಟೊಮೇಟೊಗಳಿವೆ" |
| `ml` | Malayalam | "എന്റെ കൈയിൽ 10 കിലോ തക്കാളികൾ ഉണ്ട്" |
| `gu` | Gujarati | "મારી પાસે 10 કિલો ટામેટા છે" |
| `mr` | Marathi | "माझ्याकडे 10 किलो टोमॅटो आहेत" |
| `bn` | Bengali | "আমার কাছে 10 কিলো টমেটো আছে" |
| `or` | Odia | "ମୋ ପାଖରେ 10 କିଲୋ ଟମାଟୋ ଅଛି" |
| `pa` | Punjabi | "ਮੇਰੇ ਕੋਲ 10 ਕਿਲੋ ਟਮਾਟਰ ਹਨ" |

## 🔄 Workflow

```
┌─────────────────────────────┐
│     Farmer Voice Input      │
│ (e.g., "I have 10kg tomato")│
└────────────┬────────────────┘
             │
             ▼
┌──────────────────────────────────────┐
│  Speech-to-Text Conversion Module     │
│ (Google STT / Whisper)                │
└────────────┬──────────────────────────┘
             │
             ▼
┌────────────────────────────────────────────┐
│     Text Parsing & Entity Extraction       │
│  → Product: Tomato                         │
│  → Quantity: 10kg                          │
│  → Price: ₹20/kg                           │
│  → Language: Tamil                         │
└────────────┬───────────────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Store Parsed Data in Supabase │
└────────────┬────────────────────┘
             │
             ▼
┌────────────────────────────────────────────────────┐
│      Send Prompt to Gemini AI Module               │
│  → Generate description, min/max price, tips       │
│  → Translate response to original input language   │
└────────────┬───────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│   Store Gemini Output in Supabase DB         │
└────────────┬────────────────────────────────┘
             │
             ▼
┌───────────────────────────────────────────────┐
│   Return Response to Frontend (Web App)       │
│ → Translated Product Description              │
│ → Min/Max Price Suggestions                   │
│ → Selling Tips (e.g., market, time, etc.)     │
└────────────┬──────────────────────────────────┘
             │
             ▼
┌───────────────────────────────────────────────────────┐
│     Optional Check: Product Not Sold After X Time     │
│  → Re-engage Gemini for improvement suggestions       │
└───────────────────────────────────────────────────────┘
```

## 🛠️ API Endpoints

### Core Endpoints

- `POST /api/complete-voice-process` - Complete voice processing workflow
- `POST /api/store-product` - Store product information
- `POST /api/check-status` - Check product status by mobile number
- `POST /api/register` - Register new farmer
- `POST /api/login` - Farmer login
- `GET /api/health` - Health check

### Demo Endpoints

- `GET /` - Serve frontend
- `GET /api/health` - System status
- `GET /docs` - API documentation

## 🎨 UI Features

- **Responsive Design**: Works on mobile and desktop
- **Language Themes**: Different color schemes per language
- **Voice Recording**: Real-time audio capture
- **Product Preview**: Live preview of extracted information
- **Status Tracking**: Monitor product sales status
- **AI Suggestions**: Intelligent recommendations

## 🔒 Security

- **Row Level Security**: Supabase RLS policies
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Graceful error management
- **CORS Configuration**: Proper cross-origin settings

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

### API Testing
```bash
# Health check
curl http://localhost:8000/api/health

# Voice processing (demo)
curl -X POST http://localhost:8000/api/complete-voice-process \
  -H "Content-Type: application/json" \
  -d '{"language": "en", "transcribed_text": "I have 10 kg of tomatoes"}'
```

## 📊 Database Schema

### Farmers Table
```sql
CREATE TABLE farmers (
    id UUID PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    language VARCHAR(5) DEFAULT 'en',
    village_city VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Products Table
```sql
CREATE TABLE products (
    id UUID PRIMARY KEY,
    farmer_mobile VARCHAR(15) NOT NULL,
    product_info JSONB NOT NULL,
    ai_suggestions JSONB NOT NULL,
    transcribed_text TEXT NOT NULL,
    language VARCHAR(5) NOT NULL,
    audio_url TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    improvement_suggestions JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 🚀 Deployment

### Backend Deployment (Railway/Heroku)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy to Railway
railway login
railway init
railway up
```

### Frontend Deployment (Vercel/Netlify)
```bash
# Build and deploy
npm run build
# Upload dist/ folder to your hosting provider
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent text generation
- **Supabase** for database and authentication
- **FastAPI** for the robust backend framework
- **Indian Farmers** for inspiration and feedback

## 📞 Support

For support, email support@agrivoice.com or create an issue in this repository.

---

**Made with ❤️ for Indian Farmers** 
