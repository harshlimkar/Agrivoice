# Supabase Setup Documentation

## Overview
This document provides instructions for setting up Supabase for the AgriVoice application.

## Prerequisites
- Supabase account
- PostgreSQL knowledge (basic)
- API keys from Supabase project

## Setup Steps

### 1. Create Supabase Project
1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Create a new project
4. Note down your project URL and API keys

### 2. Database Schema Setup
1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Run the schema.sql file to create all tables and functions

### 3. Environment Variables
Add these to your `.env` file:
```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_anon_key
```

### 4. Table Structure

#### Farmers Table
- `id`: UUID (Primary Key)
- `name`: VARCHAR(100) - Farmer's full name
- `mobile`: VARCHAR(15) - Unique mobile number
- `language`: VARCHAR(5) - Preferred language
- `village_city`: VARCHAR(100) - Village or city name
- `created_at`: TIMESTAMP - Registration time
- `updated_at`: TIMESTAMP - Last update time

#### Products Table
- `id`: UUID (Primary Key)
- `name`: VARCHAR(200) - Product name
- `description`: TEXT - Product description
- `language`: VARCHAR(5) - Language of description
- `farmer_mobile`: VARCHAR(15) - Foreign key to farmers
- `category`: VARCHAR(50) - Product category
- `price`: DECIMAL(10,2) - Product price
- `quantity`: VARCHAR(50) - Product quantity
- `unit`: VARCHAR(20) - Unit of measurement
- `status`: VARCHAR(20) - Product status
- `suggestions`: TEXT - AI-generated suggestions
- `created_at`: TIMESTAMP - Creation time
- `updated_at`: TIMESTAMP - Last update time

### 5. Row Level Security (RLS)
All tables have RLS enabled with appropriate policies:
- Farmers can only access their own data
- Products are filtered by farmer mobile
- Analytics are restricted to farmer's own data

### 6. Indexes
Performance indexes are created for:
- Mobile number lookups
- Status filtering
- Category filtering
- Language filtering
- Date-based queries
- Full-text search

### 7. Functions
Custom functions available:
- `calculate_farmer_stats(mobile)` - Calculate farmer statistics
- `update_daily_analytics()` - Update daily analytics
- `update_updated_at_column()` - Trigger function for timestamps

### 8. Views
Predefined views for easier querying:
- `farmer_products` - Products with farmer information
- `farmer_stats` - Farmer statistics

## API Usage

### Authentication
```python
from supabase import create_client

url = "your_supabase_url"
key = "your_supabase_key"
supabase = create_client(url, key)
```

### Insert Farmer
```python
farmer_data = {
    "name": "Rajesh Kumar",
    "mobile": "9876543210",
    "language": "en",
    "village_city": "Mumbai"
}
result = supabase.table('farmers').insert(farmer_data).execute()
```

### Insert Product
```python
product_data = {
    "name": "Fresh Tomatoes",
    "description": "Fresh, high-quality tomatoes",
    "language": "en",
    "farmer_mobile": "9876543210",
    "category": "vegetables",
    "price": 30.00,
    "quantity": "1",
    "unit": "kg",
    "status": "pending"
}
result = supabase.table('products').insert(product_data).execute()
```

### Get Products by Farmer
```python
products = supabase.table('products')\
    .select('*')\
    .eq('farmer_mobile', '9876543210')\
    .order('created_at', desc=True)\
    .execute()
```

### Update Product Status
```python
result = supabase.table('products')\
    .update({"status": "sold"})\
    .eq('id', 'product_id')\
    .execute()
```

## Security Considerations

### 1. API Key Security
- Never expose your service role key in client-side code
- Use the anon key for client applications
- Store keys securely in environment variables

### 2. Data Validation
- All inputs are validated using Pydantic models
- Mobile numbers must match Indian format
- Language codes are restricted to supported languages

### 3. Rate Limiting
- Implement rate limiting for API calls
- Monitor usage to prevent abuse

### 4. Data Backup
- Enable automatic backups in Supabase
- Test restore procedures regularly

## Monitoring and Analytics

### 1. Database Monitoring
- Monitor query performance
- Check for slow queries
- Review connection usage

### 2. Error Tracking
- Log all database errors
- Set up alerts for critical failures
- Monitor RLS policy violations

### 3. Usage Analytics
- Track API usage patterns
- Monitor farmer engagement
- Analyze product success rates

## Troubleshooting

### Common Issues

1. **RLS Policy Violations**
   - Check if user is authenticated
   - Verify mobile number matches
   - Ensure proper policy setup

2. **Connection Errors**
   - Verify API keys
   - Check network connectivity
   - Validate project URL

3. **Performance Issues**
   - Check query execution plans
   - Verify index usage
   - Monitor connection pool

### Debug Queries
```sql
-- Check farmer data
SELECT * FROM farmers WHERE mobile = '9876543210';

-- Check products for farmer
SELECT * FROM products WHERE farmer_mobile = '9876543210';

-- Check statistics
SELECT * FROM calculate_farmer_stats('9876543210');

-- Check recent activity
SELECT * FROM voice_transcriptions 
WHERE farmer_mobile = '9876543210' 
ORDER BY created_at DESC 
LIMIT 10;
```

## Best Practices

1. **Data Consistency**
   - Use transactions for related operations
   - Validate data before insertion
   - Handle conflicts gracefully

2. **Performance**
   - Use appropriate indexes
   - Limit query results
   - Cache frequently accessed data

3. **Security**
   - Regularly rotate API keys
   - Monitor access patterns
   - Implement proper error handling

4. **Scalability**
   - Plan for data growth
   - Monitor resource usage
   - Optimize queries regularly

## Support

For issues with Supabase setup:
1. Check Supabase documentation
2. Review error logs
3. Contact Supabase support
4. Check community forums

## Migration Notes

When updating the schema:
1. Backup existing data
2. Test migrations on staging
3. Plan downtime if needed
4. Verify data integrity after migration 