import asyncio
import asyncpg
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure project 'src' is on sys.path when running from repo root
SRC = Path(__file__).resolve().parents[1]
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))

async def create_tables_direct():
    """Create tables directly using asyncpg instead of SQLAlchemy"""
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("ERROR: DATABASE_URL not found in environment variables")
        return False
    
    print("🔗 Connecting to Supabase...")
    
    try:
        conn = await asyncpg.connect(database_url)
        print("✅ Connected to Supabase successfully!")
        
        # Enable UUID extension (commonly needed)
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        print("✅ UUID extension enabled")
        
        # Create schema if needed (adjust as per your settings)
        schema = os.getenv("DATABASE_SCHEMA")
        if schema and schema.lower() != 'public':
            await conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
            print(f"✅ Schema '{schema}' created/verified")
        
        # Example table creation - replace with your actual table definitions
        tables = {
            "roles": """
                CREATE TABLE IF NOT EXISTS roles (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(100) NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "system_users": """
                CREATE TABLE IF NOT EXISTS system_users (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    username VARCHAR(100) NOT NULL UNIQUE,
                    email VARCHAR(255) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    role_id UUID REFERENCES roles(id),
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "foranes": """
                CREATE TABLE IF NOT EXISTS foranes (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "parishes": """
                CREATE TABLE IF NOT EXISTS parishes (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(200) NOT NULL,
                    forane_id UUID REFERENCES foranes(id),
                    address TEXT,
                    phone VARCHAR(20),
                    email VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "communities": """
                CREATE TABLE IF NOT EXISTS communities (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(200) NOT NULL,
                    parish_id UUID REFERENCES parishes(id),
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "families": """
                CREATE TABLE IF NOT EXISTS families (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    family_code VARCHAR(50) UNIQUE,
                    head_of_family VARCHAR(200),
                    community_id UUID REFERENCES communities(id),
                    address TEXT,
                    phone VARCHAR(20),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "individuals": """
                CREATE TABLE IF NOT EXISTS individuals (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    date_of_birth DATE,
                    gender VARCHAR(10),
                    family_id UUID REFERENCES families(id),
                    phone VARCHAR(20),
                    email VARCHAR(255),
                    occupation VARCHAR(200),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "institutions": """
                CREATE TABLE IF NOT EXISTS institutions (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    name VARCHAR(200) NOT NULL,
                    type VARCHAR(100),
                    parish_id UUID REFERENCES parishes(id),
                    address TEXT,
                    phone VARCHAR(20),
                    email VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "photos": """
                CREATE TABLE IF NOT EXISTS photos (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    filename VARCHAR(255) NOT NULL,
                    original_filename VARCHAR(255),
                    file_path TEXT,
                    file_size INTEGER,
                    mime_type VARCHAR(100),
                    individual_id UUID REFERENCES individuals(id),
                    family_id UUID REFERENCES families(id),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "family_contributions": """
                CREATE TABLE IF NOT EXISTS family_contributions (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    family_id UUID REFERENCES families(id),
                    amount DECIMAL(10, 2) NOT NULL,
                    contribution_date DATE NOT NULL,
                    purpose VARCHAR(500),
                    payment_method VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "individual_contributions": """
                CREATE TABLE IF NOT EXISTS individual_contributions (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    individual_id UUID REFERENCES individuals(id),
                    amount DECIMAL(10, 2) NOT NULL,
                    contribution_date DATE NOT NULL,
                    purpose VARCHAR(500),
                    payment_method VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """,
            
            "institution_contributions": """
                CREATE TABLE IF NOT EXISTS institution_contributions (
                    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                    institution_id UUID REFERENCES institutions(id),
                    amount DECIMAL(10, 2) NOT NULL,
                    contribution_date DATE NOT NULL,
                    purpose VARCHAR(500),
                    payment_method VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
        }
        
        # Create tables in order (respecting foreign key dependencies)
        for table_name, sql in tables.items():
            try:
                await conn.execute(sql)
                print(f"✅ Table '{table_name}' created/verified")
            except Exception as e:
                print(f"❌ Error creating table '{table_name}': {e}")
                return False
        
        # Create indexes for better performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_system_users_email ON system_users(email)",
            "CREATE INDEX IF NOT EXISTS idx_system_users_username ON system_users(username)",
            "CREATE INDEX IF NOT EXISTS idx_parishes_forane_id ON parishes(forane_id)",
            "CREATE INDEX IF NOT EXISTS idx_communities_parish_id ON communities(parish_id)",
            "CREATE INDEX IF NOT EXISTS idx_families_community_id ON families(community_id)",
            "CREATE INDEX IF NOT EXISTS idx_individuals_family_id ON individuals(family_id)",
            "CREATE INDEX IF NOT EXISTS idx_photos_individual_id ON photos(individual_id)",
            "CREATE INDEX IF NOT EXISTS idx_photos_family_id ON photos(family_id)",
            "CREATE INDEX IF NOT EXISTS idx_family_contributions_family_id ON family_contributions(family_id)",
            "CREATE INDEX IF NOT EXISTS idx_individual_contributions_individual_id ON individual_contributions(individual_id)",
            "CREATE INDEX IF NOT EXISTS idx_institution_contributions_institution_id ON institution_contributions(institution_id)",
        ]
        
        for index_sql in indexes:
            try:
                await conn.execute(index_sql)
            except Exception as e:
                print(f"⚠️  Warning: Could not create index: {e}")
        
        print("✅ All indexes created/verified")
        
        await conn.close()
        print("🎉 All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def create_tables_with_sqlalchemy():
    """Alternative method using SQLAlchemy (your original approach)"""
    try:
        # Import your models and database setup
        from core.config import settings
        from database.db import create_database_url, create_table, async_engine
        from sqlalchemy.engine.url import make_url
        from sqlalchemy import text
        
        # Import all models so metadata is populated
        from app.models import (
            community_model,
            familycontribution_model,
            family_model,
            forane_model,
            individualcontribution_model,
            individual_model,
            institutioncontribution_model,
            institution_model,
            parish_model,
            photo_model,
            role_model,
            systemuser_model,
        )
        
        url = create_database_url()
        sanitized = make_url(str(url)).set(password="***")
        print(f"🔗 Connecting to {sanitized.username}@{sanitized.host}:{sanitized.port}/{sanitized.database}")
        
        # Ensure schema exists if configured
        schema = getattr(settings, 'DATABASE_SCHEMA', None)
        if schema and schema.lower() != 'public':
            print(f"📁 Creating schema: {schema}")
            async with async_engine.begin() as conn:
                await conn.run_sync(
                    lambda c: c.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
                )
        
        print("🔨 Creating tables via SQLAlchemy...")
        await create_table()
        print("🎉 SQLAlchemy table creation completed!")
        return True
        
    except Exception as e:
        print(f"❌ SQLAlchemy method failed: {e}")
        return False

async def main():
    print("🚀 Starting table creation process for Supabase...")
    print("=" * 60)
    
    # Method 1: Try direct asyncpg approach first
    print("🔧 Method 1: Direct asyncpg table creation")
    success = await create_tables_direct()
    
    if success:
        print("\n✅ Tables created successfully using direct method!")
        return
    
    print("\n🔧 Method 2: Trying SQLAlchemy approach...")
    success = await create_tables_with_sqlalchemy()
    
    if success:
        print("\n✅ Tables created successfully using SQLAlchemy!")
    else:
        print("\n❌ Both methods failed. Please check your configuration.")

if __name__ == "__main__":
    asyncio.run(main())