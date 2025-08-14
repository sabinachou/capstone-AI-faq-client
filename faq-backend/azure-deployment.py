#!/usr/bin/env python3
"""
Azure PostgreSQL Deployment Configuration Script
This script helps verify and configure the PostgreSQL connection for Azure deployment.
"""

import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import time

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment variables"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        # Build from individual components
        postgres_host = os.environ.get('POSTGRES_HOST')
        postgres_port = os.environ.get('POSTGRES_PORT', '5432')
        postgres_db = os.environ.get('POSTGRES_DB')
        postgres_user = os.environ.get('POSTGRES_USER')
        postgres_password = os.environ.get('POSTGRES_PASSWORD')
        postgres_sslmode = os.environ.get('POSTGRES_SSLMODE', 'require')
        
        if all([postgres_host, postgres_db, postgres_user, postgres_password]):
            database_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}?sslmode={postgres_sslmode}"
        else:
            raise ValueError("PostgreSQL database configuration is incomplete")
    
    return database_url

def test_connection(database_url, max_retries=5):
    """Test database connection with retry logic"""
    print(f"Testing connection to PostgreSQL database...")
    print(f"Host: {database_url.split('@')[1].split(':')[0] if '@' in database_url else 'Unknown'}")
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(
                database_url,
                pool_pre_ping=True,
                pool_recycle=300,
                pool_size=5,
                max_overflow=10,
                echo=False
            )
            
            with engine.connect() as connection:
                # Test basic connection
                result = connection.execute(text('SELECT 1'))
                print(f"✓ Connection test successful (attempt {attempt + 1})")
                
                # Get database version
                version_result = connection.execute(text('SELECT version()'))
                version = version_result.scalar()
                print(f"✓ Database version: {version.split()[1] if version else 'Unknown'}")
                
                # Test SSL connection
                ssl_result = connection.execute(text("SHOW ssl"))
                ssl_status = ssl_result.scalar()
                print(f"✓ SSL status: {ssl_status}")
                
                return True
                
        except OperationalError as e:
            print(f"✗ Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"  Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
            else:
                print("✗ All connection attempts failed")
                return False
                
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
    
    return False

def verify_environment():
    """Verify that all required environment variables are set"""
    print("Verifying environment configuration...")
    
    required_vars = ['DATABASE_URL'] if os.environ.get('DATABASE_URL') else ['POSTGRES_HOST', 'POSTGRES_DB', 'POSTGRES_USER', 'POSTGRES_PASSWORD']
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"✗ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✓ All required environment variables are set")
    return True

def main():
    """Main function to test Azure PostgreSQL deployment"""
    print("=" * 60)
    print("Azure PostgreSQL Deployment Configuration Test")
    print("=" * 60)
    
    try:
        # Verify environment
        if not verify_environment():
            sys.exit(1)
        
        # Get database URL
        database_url = get_database_url()
        print(f"✓ Database URL configured successfully")
        
        # Test connection
        if test_connection(database_url):
            print("\n" + "=" * 60)
            print("✓ Azure PostgreSQL deployment configuration is ready!")
            print("=" * 60)
            print("\nNext steps:")
            print("1. Deploy your application to Azure")
            print("2. Set the environment variables in your Azure App Service")
            print("3. Your Flask app will automatically connect to PostgreSQL")
            print("4. Monitor the /api/health endpoint for deployment status")
        else:
            print("\n" + "=" * 60)
            print("✗ Connection test failed")
            print("=" * 60)
            print("\nTroubleshooting:")
            print("1. Verify your Azure PostgreSQL server is running")
            print("2. Check firewall rules and network access")
            print("3. Verify SSL configuration")
            print("4. Check username/password and database name")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n✗ Configuration error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
