# Azure Deployment Guide for FAQ Backend with PostgreSQL

This guide will help you deploy your FAQ backend application to Azure with PostgreSQL database support.

## Prerequisites

1. **Azure Account**: Active Azure subscription
2. **Azure CLI**: Installed and configured
3. **Python 3.8+**: For local testing
4. **Git**: For version control

## Step 1: Azure PostgreSQL Database Setup

### 1.1 Create PostgreSQL Flexible Server

```bash
# Login to Azure
az login

# Create resource group (if not exists)
az group create --name your-resource-group --location eastus

# Create PostgreSQL Flexible Server
az postgres flexible-server create \
  --resource-group your-resource-group \
  --name your-postgresql-server \
  --admin-user your-admin-username \
  --admin-password "YourSecurePassword123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 14
```

### 1.2 Configure Database Access

```bash
# Allow Azure services to access the database
az postgres flexible-server firewall-rule create \
  --resource-group your-resource-group \
  --name your-postgresql-server \
  --rule-name allow-azure-services \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255

# Create database
az postgres flexible-server db create \
  --resource-group your-resource-group \
  --server-name your-postgresql-server \
  --database-name your-database-name
```

### 1.3 Get Connection Information

```bash
# Get connection string
az postgres flexible-server show \
  --resource-group your-resource-group \
  --name your-postgresql-server \
  --query "connectionString"
```

## Step 2: Environment Configuration

### 2.1 Create Environment File

Copy `env.example` to `.env` and update with your Azure PostgreSQL details:

```bash
cp env.example .env
```

Edit `.env` with your actual values:

```env
# Azure PostgreSQL Database Configuration
DATABASE_URL=postgresql://your-admin-username:YourSecurePassword123!@your-postgresql-server.postgres.database.azure.com:5432/your-database-name?sslmode=require

# Azure-specific settings
AZURE_DEPLOYMENT=true
AZURE_APP_SERVICE=true

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secure-secret-key-here

# OpenAI Configuration
OPENAI_API_KEY=sk-4TMyDTGXFc6xoMQiWhkkAUgoPLJqWoAZUSpNGhdPdUftcFiF
```

### 2.2 Test Local Connection

```bash
# Test PostgreSQL connection
python azure-deployment.py
```

## Step 3: Deploy to Azure App Service

### 3.1 Create App Service Plan

```bash
# Create App Service Plan
az appservice plan create \
  --resource-group your-resource-group \
  --name your-app-service-plan \
  --sku B1 \
  --is-linux
```

### 3.2 Create Web App

```bash
# Create Web App
az webapp create \
  --resource-group your-resource-group \
  --plan your-app-service-plan \
  --name your-faq-backend \
  --runtime "PYTHON:3.11"
```

### 3.3 Configure Environment Variables

```bash
# Set environment variables
az webapp config appsettings set \
  --resource-group your-resource-group \
  --name your-faq-backend \
  --settings \
    DATABASE_URL="postgresql://your-admin-username:YourSecurePassword123!@your-postgresql-server.postgres.database.azure.com:5432/your-database-name?sslmode=require" \
    AZURE_DEPLOYMENT="true" \
    AZURE_APP_SERVICE="true" \
    FLASK_ENV="production" \
    FLASK_DEBUG="False" \
    SECRET_KEY="your-secure-secret-key-here" \
    OPENAI_API_KEY="sk-4TMyDTGXFc6xoMQiWhkkAUgoPLJqWoAZUSpNGhdPdUftcFiF"
```

### 3.4 Deploy Application

```