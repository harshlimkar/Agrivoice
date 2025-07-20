-- AgriVoice Supabase Access Control Rules
-- Row Level Security (RLS) policies for data protection

-- Enable RLS on all tables
ALTER TABLE farmers ENABLE ROW LEVEL SECURITY;
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if they exist
DROP POLICY IF EXISTS "Farmers can view their own data" ON farmers;
DROP POLICY IF EXISTS "Farmers can update their own data" ON farmers;
DROP POLICY IF EXISTS "Farmers can insert their own data" ON farmers;

DROP POLICY IF EXISTS "Farmers can view their own products" ON products;
DROP POLICY IF EXISTS "Farmers can insert their own products" ON products;
DROP POLICY IF EXISTS "Farmers can update their own products" ON products;

-- Farmers table policies
CREATE POLICY "Farmers can view their own data" ON farmers
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Farmers can update their own data" ON farmers
    FOR UPDATE USING (auth.uid()::text = id::text);

CREATE POLICY "Farmers can insert their own data" ON farmers
    FOR INSERT WITH CHECK (auth.uid()::text = id::text);

-- Products table policies
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

-- Allow public read access for demo purposes (remove in production)
CREATE POLICY "Public read access for demo" ON products
    FOR SELECT USING (true);

-- Function to check if user is authenticated
CREATE OR REPLACE FUNCTION is_authenticated()
RETURNS BOOLEAN AS $$
BEGIN
    RETURN auth.uid() IS NOT NULL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function to get current user's phone
CREATE OR REPLACE FUNCTION get_current_user_phone()
RETURNS VARCHAR AS $$
BEGIN
    RETURN (SELECT phone FROM farmers WHERE id = auth.uid()::uuid);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO anon, authenticated; 