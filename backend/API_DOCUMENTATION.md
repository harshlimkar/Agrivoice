# AgriVoice API Documentation

## Overview

AgriVoice is a multilingual AI-powered voice product catalog for Indian farmers. This API provides endpoints for voice processing, product management, and AI-powered suggestions.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API uses demo mode. In production, implement proper authentication.

## Endpoints

### Health Check

#### GET `/api/health`

Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "AgriVoice API is running",
  "version": "1.0.0"
}
```

### Voice Processing

#### POST `/api/complete-voice-process`

Complete voice processing workflow including transcription, product extraction, and AI suggestions.

**Request Body:**
```json
{
  "audio_data": "base64_encoded_audio_string",
  "transcribed_text": "optional_pre_transcribed_text",
  "language": "en",
  "farmer_mobile": "9876543210"
}
```

**Response:**
```json
{
  "success": true,
  "transcribed_text": "I have 10 kg of fresh tomatoes",
  "product": "tomato",
  "quantity": "10 kg",
  "price": "₹40",
  "description": "Fresh, high-quality tomatoes from local farm",
  "suggested_price_range": "₹35 - ₹45 per kg",
  "market_suggestion": "Local market, nearby towns",
  "selling_tip": "Highlight freshness and organic quality",
  "product_id": "demo_product_123",
  "language": "en"
}
```

### Product Management

#### POST `/api/store-product`

Store product information in the database.

**Request Body:**
```json
{
  "product_info": {
    "product": "tomato",
    "quantity": "10 kg",
    "price": "₹40"
  },
  "ai_response": {
    "description": "Fresh tomatoes",
    "price_range": "₹35-45"
  },
  "transcribed_text": "I have 10 kg of tomatoes",
  "language": "en",
  "farmer_mobile": "9876543210"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Product stored successfully",
  "product_id": "demo_product_123"
}
```

#### POST `/api/check-status`

Check product status by mobile number.

**Request Body:**
```json
{
  "mobile": "9876543210"
}
```

**Response:**
```json
{
  "success": true,
  "products": [
    {
      "id": "demo_product_123",
      "farmer_mobile": "9876543210",
      "product_info": "{\"product\": \"tomato\", \"quantity\": \"10 kg\"}",
      "status": "pending",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

#### POST `/api/update-product-status`

Update product status.

**Request Body:**
```json
{
  "product_id": "demo_product_123",
  "status": "sold"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Status updated successfully"
}
```

### Farmer Management

#### POST `/api/register`

Register a new farmer.

**Request Body:**
```json
{
  "name": "Rajesh Kumar",
  "email": "rajesh@example.com",
  "phone": "9876543210",
  "password": "password123",
  "language": "en",
  "village_city": "Mumbai"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Farmer registered successfully",
  "user": {
    "id": "demo_farmer_123",
    "name": "Rajesh Kumar",
    "email": "rajesh@example.com",
    "phone": "9876543210"
  }
}
```

#### POST `/api/login`

Login farmer.

**Request Body:**
```json
{
  "email": "rajesh@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": "demo_farmer_123",
    "name": "Rajesh Kumar",
    "email": "rajesh@example.com"
  }
}
```

### AI Suggestions

#### POST `/api/check-unsold-products`

Check for unsold products and generate improvement suggestions.

**Response:**
```json
{
  "success": true,
  "message": "Processing 2 unsold products"
}
```

## Error Responses

All endpoints return error responses in the following format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

Common HTTP status codes:
- `400` - Bad Request (invalid input)
- `401` - Unauthorized (authentication required)
- `404` - Not Found (resource not found)
- `500` - Internal Server Error (server error)

## Language Support

The API supports the following Indian languages:

| Code | Language |
|------|----------|
| `en` | English |
| `hi` | Hindi |
| `ta` | Tamil |
| `te` | Telugu |
| `kn` | Kannada |
| `ml` | Malayalam |
| `gu` | Gujarati |
| `mr` | Marathi |
| `bn` | Bengali |
| `or` | Odia |
| `pa` | Punjabi |

## Audio Format Support

Supported audio formats:
- WAV
- MP3
- OGG
- WebM

Maximum file size: 10MB
Maximum duration: 60 seconds

## Rate Limiting

Currently, no rate limiting is implemented. In production, implement appropriate rate limiting.

## CORS

CORS is enabled for development. Configure appropriately for production.

## Demo Mode

The API runs in demo mode when environment variables are not configured. In demo mode:
- Mock responses are returned
- No actual AI processing occurs
- No database operations are performed

## Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp env.example .env
# Edit .env with your API keys
```

3. Start the server:
```bash
python start_server.py
```

4. Access the API:
- API: http://localhost:8000
- Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health

## Testing

Test the API using curl or any HTTP client:

```bash
# Health check
curl http://localhost:8000/api/health

# Voice processing (demo)
curl -X POST http://localhost:8000/api/complete-voice-process \
  -H "Content-Type: application/json" \
  -d '{"language": "en", "transcribed_text": "I have 10 kg of tomatoes"}'
``` 