-- AgriVoice Database Schema
-- Supabase SQL schema for products and farmers tables

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Farmers table
CREATE TABLE IF NOT EXISTS farmers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(15) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    language VARCHAR(5) DEFAULT 'en',
    village_city VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_mobile VARCHAR(15) NOT NULL,
    product_info JSONB NOT NULL,
    ai_suggestions JSONB NOT NULL,
    transcribed_text TEXT NOT NULL,
    language VARCHAR(5) NOT NULL,
    audio_url TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    improvement_suggestions JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Product status enum
CREATE TYPE product_status AS ENUM ('pending', 'sold', 'expired', 'cancelled');

-- Update products table to use enum
ALTER TABLE products 
ALTER COLUMN status TYPE product_status 
USING status::product_status;

-- Indexes for better performance
CREATE INDEX IF NOT EXISTS idx_products_farmer_mobile ON products(farmer_mobile);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);
CREATE INDEX IF NOT EXISTS idx_products_language ON products(language);

CREATE INDEX IF NOT EXISTS idx_farmers_phone ON farmers(phone);
CREATE INDEX IF NOT EXISTS idx_farmers_email ON farmers(email);

-- Row Level Security (RLS) policies
ALTER TABLE farmers ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Farmers policies
CREATE POLICY "Farmers can view their own data" ON farmers
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Farmers can update their own data" ON farmers
    FOR UPDATE USING (auth.uid()::text = id::text);

CREATE POLICY "Farmers can insert their own data" ON farmers
    FOR INSERT WITH CHECK (auth.uid()::text = id::text);

-- Products policies
CREATE POLICY "Farmers can view their own products" ON products
    FOR SELECT USING (farmer_mobile = (
        SELECT phone FROM farmers WHERE id = auth.uid()::uuid
    ));

CREATE POLICY "Farmers can insert their own products" ON products
    FOR INSERT WITH CHECK (farmer_mobile = (
        SELECT phone FROM farmers WHERE id = auth.uid()::uuid
    ));

CREATE POLICY "Farmers can update their own products" ON products
    FOR UPDATE USING (farmer_mobile = (
        SELECT phone FROM farmers WHERE id = auth.uid()::uuid
    ));

-- Functions for automatic timestamp updates
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic timestamp updates
CREATE TRIGGER update_farmers_updated_at 
    BEFORE UPDATE ON farmers 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at 
    BEFORE UPDATE ON products 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to get product statistics
CREATE OR REPLACE FUNCTION get_product_statistics(farmer_phone VARCHAR)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'total_products', COUNT(*),
        'sold_products', COUNT(*) FILTER (WHERE status = 'sold'),
        'pending_products', COUNT(*) FILTER (WHERE status = 'pending'),
        'expired_products', COUNT(*) FILTER (WHERE status = 'expired'),
        'sold_percentage', CASE 
            WHEN COUNT(*) > 0 THEN 
                ROUND((COUNT(*) FILTER (WHERE status = 'sold')::DECIMAL / COUNT(*) * 100), 2)
            ELSE 0 
        END
    ) INTO result
    FROM products 
    WHERE farmer_mobile = farmer_phone;
    
    RETURN result;
END;
$$ LANGUAGE plpgsql;

-- Function to get unsold products older than specified days
CREATE OR REPLACE FUNCTION get_unsold_products_older_than(days INTEGER)
RETURNS TABLE (
    id UUID,
    farmer_mobile VARCHAR,
    product_info JSONB,
    ai_suggestions JSONB,
    language VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE
) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.farmer_mobile, p.product_info, p.ai_suggestions, p.language, p.created_at
    FROM products p
    WHERE p.status = 'pending' 
    AND p.created_at < NOW() - INTERVAL '1 day' * days;
END;
$$ LANGUAGE plpgsql;

-- Views for easier querying
CREATE VIEW product_summary AS
SELECT 
    p.id,
    p.farmer_mobile,
    p.product_info->>'product' as product_name,
    p.product_info->>'quantity' as quantity,
    p.product_info->>'price' as price,
    p.ai_suggestions->>'description' as description,
    p.ai_suggestions->>'price_range' as suggested_price_range,
    p.status,
    p.language,
    p.created_at,
    p.updated_at
FROM products p;

-- Insert sample data for testing
INSERT INTO farmers (name, email, phone, password_hash, language, village_city) VALUES
('Demo Farmer', 'demo@agrivoice.com', '9876543210', 'hashed_password', 'en', 'Demo Village')
ON CONFLICT (phone) DO NOTHING;

INSERT INTO products (farmer_mobile, product_info, ai_suggestions, transcribed_text, language, status) VALUES
('9876543210', 
 '{"product": "tomato", "quantity": "10 kg", "price": "₹40"}',
 '{"description": "Fresh, high-quality tomatoes from local farm", "price_range": "₹35-45", "where_to_sell": "Local market", "selling_tip": "Highlight freshness"}',
 'I have 10 kg of fresh tomatoes',
 'en',
 'pending')
ON CONFLICT DO NOTHING; 