#!/bin/bash

# AgriVoice Supabase Setup Script
# This script helps set up the Supabase project for AgriVoice

echo "🌾 AgriVoice Supabase Setup"
echo "=========================="

# Check if Supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI is not installed."
    echo "📦 Please install it first:"
    echo "   npm install -g supabase"
    echo "   or"
    echo "   brew install supabase/tap/supabase"
    exit 1
fi

echo "✅ Supabase CLI found"

# Check if user is logged in
if ! supabase auth list &> /dev/null; then
    echo "🔐 Please log in to Supabase:"
    supabase login
fi

echo "✅ Logged in to Supabase"

# Create new project or link existing
echo "📋 Do you want to:"
echo "1. Create a new Supabase project"
echo "2. Link to existing project"
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo "🚀 Creating new Supabase project..."
    supabase projects create agrivoice --org-id $(supabase orgs list --output json | jq -r '.[0].id')
    echo "✅ Project created successfully"
elif [ "$choice" = "2" ]; then
    echo "🔗 Linking to existing project..."
    read -p "Enter your Supabase project reference ID: " project_ref
    supabase link --project-ref $project_ref
    echo "✅ Project linked successfully"
else
    echo "❌ Invalid choice"
    exit 1
fi

# Initialize Supabase in current directory
echo "📁 Initializing Supabase..."
supabase init

# Apply the schema
echo "🗄️ Applying database schema..."
supabase db push

echo "✅ Schema applied successfully"

# Get project URL and keys
echo "🔑 Getting project credentials..."
PROJECT_REF=$(supabase projects list --output json | jq -r '.[0].id')
PROJECT_URL=$(supabase projects list --output json | jq -r '.[0].api_url')
ANON_KEY=$(supabase projects api-keys list --project-ref $PROJECT_REF --output json | jq -r '.[0].anon')

echo "📋 Project Information:"
echo "Project Reference: $PROJECT_REF"
echo "Project URL: $PROJECT_URL"
echo "Anon Key: $ANON_KEY"

# Create .env file
echo "📝 Creating .env file..."
cat > ../backend/.env << EOF
# AgriVoice Environment Variables
GEMINI_API_KEY=your_gemini_api_key_here
SUPABASE_URL=$PROJECT_URL
SUPABASE_ANON_KEY=$ANON_KEY
HOST=0.0.0.0
PORT=8000
DEBUG=True
EOF

echo "✅ .env file created with Supabase credentials"
echo ""
echo "🎉 Supabase setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Add your Gemini API key to backend/.env"
echo "2. Start the backend server: cd backend && python start_server.py"
echo "3. Start the frontend: cd frontend && python -m http.server 3000"
echo ""
echo "🌐 Access your app at: http://localhost:3000" 