# Azure PostgreSQL Deployment Guide

This guide will help you deploy your FAQ application with Azure PostgreSQL. The application now requires PostgreSQL and no longer supports SQLite.

## Prerequisites

1. Azure account with an active subscription
2. Azure PostgreSQL Flexible Server instance created
3. Database created on your PostgreSQL server
4. Firewall rules configured to allow your application access

## Step 1: Install Dependencies

Install the updated requirements:

```bash
cd faq-backend
pip install -r requirements.txt
```

## Step 2: Configure Environment Variables

### Option A: Using DATABASE_URL (Recommended)

Create a `.env` file in the `faq-backend` directory with your Azure PostgreSQL connection string:

```env
# Azure PostgreSQL Configuration
DATABASE_URL=postgresql://username:password@servername.postgres.database.azure.com:5432/databasename?sslmode=require

# Replace with your actual values:
# username: Your PostgreSQL admin username
# password: Your PostgreSQL admin password
# servername: Your Azure PostgreSQL server name
# databasename: Your database name
```

### Option B: Using Individual Variables

Alternatively, you can use separate environment variables:

```env
POSTGRES_HOST=your-server-name.postgres.database.azure.com
POSTGRES_PORT=5432
POSTGRES_DB=your-database-name
POSTGRES_USER=your-username
POSTGRES_PASSWORD=your-password
POSTGRES_SSLMODE=require
```

### Other Required Environment Variables

```env
# OpenAI Configuration
OPENAI_API_KEY="sk-4TMyDTGXFc6xoMQiWhkkAUgoPLJqWoAZUSpNGhdPdUftcFiF" \

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secure-secret-key-here

# AI Service Configuration
AI_SIMILARITY_THRESHOLD=0.3
AI_MAX_TOKENS=500
AI_TEMPERATURE=0.7
```

## Step 3: Database Migration

### Initialize the Database

Run the application once to create all tables:

```bash
python app.py
```

The application will automatically create all necessary tables in your PostgreSQL database.

### Populate Initial Data (Optional)

If you need to add initial FAQ data to your PostgreSQL database:

```python
# Create a data population script
from app import app, db, FAQ

with app.app_context():
    # Add sample FAQs
    sample_faqs = [
        {"question": "What is this application?", "answer": "This is an AI-powered FAQ system."},
        {"question": "How do I get support?", "answer": "Please contact our support team."}
    ]
    
    for faq_data in sample_faqs:
        faq = FAQ(question=faq_data['question'], answer=faq_data['answer'])
        db.session.add(faq)
    
    db.session.commit()
    print("Sample data added successfully!")
```

## Step 4: Azure App Service Deployment (Optional)

If deploying to Azure App Service:

### 1. Create App Service

```bash
# Create resource group
az group create --name myResourceGroup --location "East US"

# Create App Service plan
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux

# Create web app
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myFAQApp --runtime "PYTHON|3.9" --deployment-local-git
```

### 2. Configure App Settings

```bash
# Set environment variables
az webapp config appsettings set --resource-group myResourceGroup --name myFAQApp --settings \
    DATABASE_URL="postgresql://username:password@servername.postgres.database.azure.com:5432/databasename?sslmode=require" \
    OPENAI_API_KEY="sk-abcd1234efgh5678abcd1234efgh5678abcd1234" \
    FLASK_ENV="production" \
    SECRET_KEY="your-secure-secret-key"
```

### 3. Deploy Application

```bash
# Add Azure remote
git remote add azure <deploymentLocalGitUrl>

# Deploy
git push azure main
```

## Step 5: Testing the Migration

1. **Test database connection:**
   ```bash
   python -c "from app import app, db; app.app_context().push(); print('Database connection successful!' if db.engine.execute('SELECT 1').scalar() == 1 else 'Connection failed')"
   ```

2. **Test API endpoints:**
   ```bash
   # Test FAQ endpoint
   curl http://localhost:5000/api/faqs
   
   # Test chat endpoint
   curl -X POST http://localhost:5000/api/chat -H "Content-Type: application/json" -d '{"question": "test", "session_id": "test123"}'
   ```

## Troubleshooting

### Common Issues

1. **Connection timeout:**
   - Ensure firewall rules allow your IP address
   - Check if SSL is required (use `sslmode=require`)

2. **Authentication failed:**
   - Verify username and password
   - Check if the user has proper permissions

3. **Database not found:**
   - Ensure the database exists on your PostgreSQL server
   - Check the database name in your connection string

### Performance Optimization

1. **Connection pooling** is already configured in `config.py`
2. **Consider using Azure Database for PostgreSQL connection pooling**
3. **Monitor query performance** using Azure PostgreSQL insights

## Security Best Practices

1. **Use Azure Key Vault** for storing sensitive configuration
2. **Enable SSL/TLS** for all database connections
3. **Restrict database access** using firewall rules
4. **Use managed identity** when possible for Azure services
5. **Regularly update dependencies** and security patches

## Monitoring and Logging

1. **Enable Azure PostgreSQL logs**
2. **Use Application Insights** for application monitoring
3. **Set up alerts** for database performance and errors
4. **Monitor connection pool usage**

## Backup and Recovery

1. **Configure automated backups** in Azure PostgreSQL
2. **Test restore procedures** regularly
3. **Consider point-in-time recovery** options
4. **Document recovery procedures**

Your application is now ready for Azure PostgreSQL deployment!