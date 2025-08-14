#!/usr/bin/env python3
"""
Simple PostgreSQL Connection Test Script
This script helps test your PostgreSQL connection step by step.
"""

import os
from dotenv import load_dotenv

def test_env_variables():
    """Test if environment variables are loaded correctly"""
    print("🔍 Testing Environment Variables...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if we have the basic PostgreSQL variables
    database_url = os.environ.get('DATABASE_URL')
    postgres_host = os.environ.get('POSTGRES_HOST')
    postgres_db = os.environ.get('POSTGRES_DB')
    postgres_user = os.environ.get('POSTGRES_USER')
    postgres_password = os.environ.get('POSTGRES_PASSWORD')
    
    print(f"  DATABASE_URL: {'✓ Set' if database_url else '✗ Not set'}")
    print(f"  POSTGRES_HOST: {'✓ Set' if postgres_host else '✗ Not set'}")
    print(f"  POSTGRES_DB: {'✓ Set' if postgres_db else '✗ Not set'}")
    print(f"  POSTGRES_USER: {'✓ Set' if postgres_user else '✗ Not set'}")
    print(f"  POSTGRES_PASSWORD: {'✓ Set' if postgres_password else '✗ Not set'}")
    
    # Check if we have placeholder values
    if postgres_host and 'your-azure-postgresql-server' in postgres_host:
        print("\n⚠️  WARNING: You still have placeholder values in your .env file!")
        print("   Please update with your actual Azure PostgreSQL server details.")
        return False
    
    if database_url and 'your-azure-postgresql-server' in database_url:
        print("\n⚠️  WARNING: You still have placeholder values in your .env file!")
        print("   Please update with your actual Azure PostgreSQL server details.")
        return False
    
    return True

def test_psycopg2_installation():
    """Test if psycopg2 is properly installed"""
    print("\n🔍 Testing psycopg2 Installation...")
    
    try:
        import psycopg2
        print("  ✓ psycopg2 is installed")
        print(f"  Version: {psycopg2.__version__}")
        return True
    except ImportError as e:
        print(f"  ✗ psycopg2 not installed: {e}")
        print("  Install with: pip install psycopg2-binary")
        return False

def test_sqlalchemy_installation():
    """Test if SQLAlchemy is properly installed"""
    print("\n🔍 Testing SQLAlchemy Installation...")
    
    try:
        import sqlalchemy
        print("  ✓ SQLAlchemy is installed")
        print(f"  Version: {sqlalchemy.__version__}")
        return True
    except ImportError as e:
        print(f"  ✗ SQLAlchemy not installed: {e}")
        return False

def test_database_connection():
    """Test actual database connection"""
    print("\n🔍 Testing Database Connection...")
    
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.exc import OperationalError
        
        # Load environment variables
        load_dotenv()
        
        database_url = os.environ.get('DATABASE_URL')
        if not database_url:
            print("  ✗ DATABASE_URL not set")
            return False
        
        print(f"  Attempting to connect to: {database_url.split('@')[1] if '@' in database_url else 'Unknown'}")
        
        # Create engine
        engine = create_engine(database_url, echo=False)
        
        # Test connection
        with engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print("  ✓ Database connection successful!")
            
            # Get database version
            version_result = connection.execute(text('SELECT version()'))
            version = version_result.scalar()
            print(f"  Database version: {version.split()[1] if version else 'Unknown'}")
            
            return True
            
    except OperationalError as e:
        print(f"  ✗ Database connection failed: {e}")
        return False
    except Exception as e:
        print(f"  ✗ Unexpected error: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("PostgreSQL Connection Test Suite")
    print("=" * 60)
    
    # Test environment variables
    env_ok = test_env_variables()
    
    # Test installations
    psycopg2_ok = test_psycopg2_installation()
    sqlalchemy_ok = test_sqlalchemy_installation()
    
    # Only test database connection if everything else is OK
    if env_ok and psycopg2_ok and sqlalchemy_ok:
        db_ok = test_database_connection()
    else:
        db_ok = False
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    if env_ok and psycopg2_ok and sqlalchemy_ok and db_ok:
        print("🎉 All tests passed! Your PostgreSQL connection is working.")
        print("\nNext steps:")
        print("1. Test your Flask app: python app.py")
        print("2. Test the health endpoint: curl http://localhost:5000/api/health")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
        if not env_ok:
            print("\n🔧 To fix environment variables:")
            print("1. Update your .env file with real Azure PostgreSQL credentials")
            print("2. Make sure to replace placeholder values like 'your-azure-postgresql-server'")
            print("3. Use the format: postgresql://username:password@server.postgres.database.azure.com:5432/database?sslmode=require")
        
        if not psycopg2_ok:
            print("\n🔧 To fix psycopg2:")
            print("1. Run: pip install psycopg2-binary")
        
        if not sqlalchemy_ok:
            print("\n🔧 To fix SQLAlchemy:")
            print("1. Run: pip install SQLAlchemy")

if __name__ == '__main__':
    main()

