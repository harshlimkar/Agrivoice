-- AgriVoice Database Schema
-- Supabase SQL for setting up tables
-- PostgreSQL syntax (not SQL Server compatible)

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create farmers table
CREATE TABLE IF NOT EXISTS farmers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15) UNIQUE NOT NULL CHECK (mobile ~ '^[6-9]\d{9}$'),
    language VARCHAR(5) NOT NULL DEFAULT 'en' CHECK (language IN ('en', 'hi', 'ta', 'te', 'kn', 'ml', 'gu', 'mr', 'bn', 'or', 'pa')),
    village_city VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    language VARCHAR(5) NOT NULL DEFAULT 'en' CHECK (language IN ('en', 'hi', 'ta', 'te', 'kn', 'ml', 'gu', 'mr', 'bn', 'or', 'pa')),
    farmer_mobile VARCHAR(15) NOT NULL REFERENCES farmers(mobile) ON DELETE CASCADE,
    category VARCHAR(50) CHECK (category IN ('vegetables', 'fruits', 'grains', 'dairy', 'meat', 'beverages', 'snacks', 'general')),
    price DECIMAL(10,2) CHECK (price >= 0),
    quantity VARCHAR(50),
    unit VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'sold', 'expired', 'cancelled')),
    suggestions TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create product_suggestions table for AI suggestions
CREATE TABLE IF NOT EXISTS product_suggestions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    suggestions TEXT NOT NULL,
    language VARCHAR(5) NOT NULL DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create voice_transcriptions table for storing transcription history
CREATE TABLE IF NOT EXISTS voice_transcriptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_mobile VARCHAR(15) NOT NULL REFERENCES farmers(mobile) ON DELETE CASCADE,
    original_text TEXT NOT NULL,
    transcribed_text TEXT NOT NULL,
    language VARCHAR(5) NOT NULL DEFAULT 'en',
    confidence DECIMAL(3,2) CHECK (confidence >= 0 AND confidence <= 1),
    audio_duration DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create product_analytics table for storing analytics data
CREATE TABLE IF NOT EXISTS product_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_mobile VARCHAR(15) NOT NULL REFERENCES farmers(mobile) ON DELETE CASCADE,
    date DATE NOT NULL,
    total_products INTEGER DEFAULT 0,
    sold_products INTEGER DEFAULT 0,
    pending_products INTEGER DEFAULT 0,
    expired_products INTEGER DEFAULT 0,
    cancelled_products INTEGER DEFAULT 0,
    sold_percentage DECIMAL(5,2) DEFAULT 0,
    average_price DECIMAL(10,2),
    total_value DECIMAL(12,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(farmer_mobile, date)
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_farmers_mobile ON farmers(mobile);
CREATE INDEX IF NOT EXISTS idx_farmers_language ON farmers(language);
CREATE INDEX IF NOT EXISTS idx_products_farmer_mobile ON products(farmer_mobile);
CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
CREATE INDEX IF NOT EXISTS idx_products_language ON products(language);
CREATE INDEX IF NOT EXISTS idx_products_created_at ON products(created_at);
CREATE INDEX IF NOT EXISTS idx_product_suggestions_product_id ON product_suggestions(product_id);
CREATE INDEX IF NOT EXISTS idx_voice_transcriptions_farmer_mobile ON voice_transcriptions(farmer_mobile);
CREATE INDEX IF NOT EXISTS idx_voice_transcriptions_created_at ON voice_transcriptions(created_at);
CREATE INDEX IF NOT EXISTS idx_product_analytics_farmer_mobile ON product_analytics(farmer_mobile);
CREATE INDEX IF NOT EXISTS idx_product_analytics_date ON product_analytics(date);

-- Create full-text search indexes
CREATE INDEX IF NOT EXISTS idx_products_search ON products USING gin(to_tsvector('english', name || ' ' || description));
CREATE INDEX IF NOT EXISTS idx_products_search_hindi ON products USING gin(to_tsvector('hindi', name || ' ' || description));

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_farmers_updated_at BEFORE UPDATE ON farmers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_product_analytics_updated_at BEFORE UPDATE ON product_analytics
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Create function to calculate product statistics
CREATE OR REPLACE FUNCTION calculate_farmer_stats(farmer_mobile_param VARCHAR(15))
RETURNS TABLE(
    total_products BIGINT,
    sold_products BIGINT,
    pending_products BIGINT,
    expired_products BIGINT,
    cancelled_products BIGINT,
    sold_percentage DECIMAL(5,2),
    average_price DECIMAL(10,2),
    total_value DECIMAL(12,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::BIGINT as total_products,
        COUNT(CASE WHEN status = 'sold' THEN 1 END)::BIGINT as sold_products,
        COUNT(CASE WHEN status = 'pending' THEN 1 END)::BIGINT as pending_products,
        COUNT(CASE WHEN status = 'expired' THEN 1 END)::BIGINT as expired_products,
        COUNT(CASE WHEN status = 'cancelled' THEN 1 END)::BIGINT as cancelled_products,
        CASE 
            WHEN COUNT(*) > 0 THEN 
                (COUNT(CASE WHEN status = 'sold' THEN 1 END)::DECIMAL / COUNT(*)::DECIMAL * 100)
            ELSE 0 
        END as sold_percentage,
        AVG(price) as average_price,
        SUM(price) as total_value
    FROM products 
    WHERE farmer_mobile = farmer_mobile_param;
END;
$$ LANGUAGE plpgsql;

-- Create function to update analytics
CREATE OR REPLACE FUNCTION update_daily_analytics()
RETURNS VOID AS $$
BEGIN
    INSERT INTO product_analytics (
        farmer_mobile,
        date,
        total_products,
        sold_products,
        pending_products,
        expired_products,
        cancelled_products,
        sold_percentage,
        average_price,
        total_value
    )
    SELECT 
        f.mobile,
        CURRENT_DATE,
        COALESCE(p_stats.total_products, 0),
        COALESCE(p_stats.sold_products, 0),
        COALESCE(p_stats.pending_products, 0),
        COALESCE(p_stats.expired_products, 0),
        COALESCE(p_stats.cancelled_products, 0),
        COALESCE(p_stats.sold_percentage, 0),
        COALESCE(p_stats.average_price, 0),
        COALESCE(p_stats.total_value, 0)
    FROM farmers f
    LEFT JOIN LATERAL calculate_farmer_stats(f.mobile) p_stats ON true
    ON CONFLICT (farmer_mobile, date) 
    DO UPDATE SET
        total_products = EXCLUDED.total_products,
        sold_products = EXCLUDED.sold_products,
        pending_products = EXCLUDED.pending_products,
        expired_products = EXCLUDED.expired_products,
        cancelled_products = EXCLUDED.cancelled_products,
        sold_percentage = EXCLUDED.sold_percentage,
        average_price = EXCLUDED.average_price,
        total_value = EXCLUDED.total_value,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- Create RLS (Row Level Security) policies
ALTER TABLE farmers ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_suggestions ENABLE ROW LEVEL SECURITY;
ALTER TABLE voice_transcriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE product_analytics ENABLE ROW LEVEL SECURITY;

-- Farmers policies
CREATE POLICY "Farmers can view their own data" ON farmers
    FOR SELECT USING (mobile = current_setting('app.farmer_mobile', true));

CREATE POLICY "Farmers can insert their own data" ON farmers
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Farmers can update their own data" ON farmers
    FOR UPDATE USING (mobile = current_setting('app.farmer_mobile', true));

-- Products policies
CREATE POLICY "Farmers can view their own products" ON products
    FOR SELECT USING (farmer_mobile = current_setting('app.farmer_mobile', true));

CREATE POLICY "Farmers can insert their own products" ON products
    FOR INSERT WITH CHECK (farmer_mobile = current_setting('app.farmer_mobile', true));

CREATE POLICY "Farmers can update their own products" ON products
    FOR UPDATE USING (farmer_mobile = current_setting('app.farmer_mobile', true));

-- Product suggestions policies
CREATE POLICY "Farmers can view suggestions for their products" ON product_suggestions
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM products p 
            WHERE p.id = product_suggestions.product_id 
            AND p.farmer_mobile = current_setting('app.farmer_mobile', true)
        )
    );

CREATE POLICY "System can insert suggestions" ON product_suggestions
    FOR INSERT WITH CHECK (true);

-- Voice transcriptions policies
CREATE POLICY "Farmers can view their own transcriptions" ON voice_transcriptions
    FOR SELECT USING (farmer_mobile = current_setting('app.farmer_mobile', true));

CREATE POLICY "Farmers can insert their own transcriptions" ON voice_transcriptions
    FOR INSERT WITH CHECK (farmer_mobile = current_setting('app.farmer_mobile', true));

-- Product analytics policies
CREATE POLICY "Farmers can view their own analytics" ON product_analytics
    FOR SELECT USING (farmer_mobile = current_setting('app.farmer_mobile', true));

-- Create views for easier querying
CREATE OR REPLACE VIEW farmer_products AS
SELECT 
    p.*,
    f.name as farmer_name,
    f.language as farmer_language
FROM products p
JOIN farmers f ON p.farmer_mobile = f.mobile;

CREATE OR REPLACE VIEW farmer_stats AS
SELECT 
    f.mobile,
    f.name,
    f.language,
    f.village_city,
    COALESCE(p_stats.total_products, 0) as total_products,
    COALESCE(p_stats.sold_products, 0) as sold_products,
    COALESCE(p_stats.pending_products, 0) as pending_products,
    COALESCE(p_stats.sold_percentage, 0) as sold_percentage,
    f.created_at as registration_date,
    f.updated_at as last_activity
FROM farmers f
LEFT JOIN LATERAL calculate_farmer_stats(f.mobile) p_stats ON true;

-- Insert sample data for testing
INSERT INTO farmers (name, mobile, language, village_city) VALUES
('Rajesh Kumar', '9876543210', 'en', 'Mumbai'),
('Priya Singh', '8765432109', 'hi', 'Delhi'),
('Mohan Reddy', '7654321098', 'te', 'Hyderabad'),
('Lakshmi Devi', '6543210987', 'ta', 'Chennai')
ON CONFLICT (mobile) DO NOTHING;

INSERT INTO products (name, description, language, farmer_mobile, category, price, quantity, unit, status) VALUES
('Fresh Tomatoes', 'Fresh, high-quality tomatoes from local farm. Perfect for your daily needs!', 'en', '9876543210', 'vegetables', 30.00, '1', 'kg', 'pending'),
('Organic Rice', 'Premium quality organic rice, perfect for daily meals', 'en', '9876543210', 'grains', 250.00, '5', 'kg', 'sold'),
('Sweet Mangoes', 'Sweet and juicy mangoes from organic farms', 'en', '9876543210', 'fruits', 120.00, '2', 'kg', 'pending'),
('Fresh Vegetables', 'Fresh vegetables from my farm', 'hi', '8765432109', 'vegetables', 50.00, '1', 'kg', 'pending')
ON CONFLICT DO NOTHING;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated; 