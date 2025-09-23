#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dynamic Table Creation Script for KPLY Dialysis Project

This script reads SQLAlchemy models and generates SQL CREATE TABLE statements
that match your model definitions exactly, including the kply_ prefix.
"""

import asyncio
import asyncpg
import os
import sys
import re
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql
from sqlalchemy.pool import StaticPool

# Load environment variables
load_dotenv()

# Ensure project 'src' is on sys.path when running from repo root
SRC = Path(__file__).resolve().parents[1]
if str(SRC) not in sys.path:
    sys.path.append(str(SRC))

def get_create_table_sql():
    """
    Generate CREATE TABLE SQL statements from SQLAlchemy models
    """
    try:
        print("📦 Importing models and database configuration...")
        
        # Import your models and database setup
        from core.config import settings
        from database.db import create_database_url
        from common.model import MappedBase
        
        # Import all models to populate metadata
        from app.models import (
            systemuser_model,
            role_model,
            forane_model,
            parish_model,
            community_model,
            family_model,
            individual_model,
            institution_model,
            familycontribution_model,
            individualcontribution_model,
            institutioncontribution_model,
            photo_model,
        )
        
        print("✅ All models imported successfully")
        
        # Use a mock strategy engine that doesn't require real database connection
        # Create a mock engine that can compile SQL without connecting
        mock_engine = create_engine(
            "postgresql://user:pass@localhost/db",  # Dummy URL
            strategy='mock',
            executor=lambda sql, *_: None,
            paramstyle='named',
            module=None
        )
        
        print("🔗 Using mock engine for SQL generation (no database connection required)")
        
        # Generate CREATE TABLE statements using PostgreSQL dialect
        tables_sql = []
        dialect = postgresql.dialect()
        
        # Sort tables by dependencies (your original ordering)
        table_order = [
            'kply_roles',
            'kply_system_users', 
            'kply_foranes',
            'kply_parishes',
            'kply_communities',
            'kply_families',
            'kply_individuals',
            'kply_institutions',
            'kply_family_contributions',
            'kply_individual_contributions',
            'kply_institution_contributions',
            'kply_photos'
        ]
        
        # Get all tables from metadata
        all_tables = {table.name: table for table in MappedBase.metadata.tables.values()}
        
        print(f"📋 Found {len(all_tables)} tables in metadata:")
        for table_name in sorted(all_tables.keys()):
            print(f"   - {table_name}")
        
        if not all_tables:
            print("⚠️  No tables found in metadata. Make sure all models are imported correctly.")
            return []
        
        # Generate SQL in dependency order
        for table_name in table_order:
            if table_name in all_tables:
                table = all_tables[table_name]
                try:
                    create_sql = str(CreateTable(table).compile(dialect=dialect))
                    tables_sql.append({
                        'name': table_name,
                        'sql': create_sql
                    })
                    print(f"✅ Generated SQL for {table_name}")
                except Exception as e:
                    print(f"❌ Error generating SQL for {table_name}: {e}")
            else:
                print(f"⚠️  Table {table_name} not found in metadata")
        
        # Add any remaining tables not in the ordered list
        for table_name, table in all_tables.items():
            if not any(t['name'] == table_name for t in tables_sql):
                try:
                    create_sql = str(CreateTable(table).compile(dialect=dialect))
                    tables_sql.append({
                        'name': table_name,
                        'sql': create_sql
                    })
                    print(f"✅ Generated SQL for {table_name} (additional)")
                except Exception as e:
                    print(f"❌ Error generating SQL for {table_name}: {e}")
        
        return tables_sql
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all your model files exist and are properly structured")
        return []
    except Exception as e:
        print(f"❌ Error generating SQL: {e}")
        import traceback
        traceback.print_exc()
        return []

def add_if_not_exists(sql):
    """
    Safely add IF NOT EXISTS to CREATE TABLE statement
    """
    # More robust pattern matching
    pattern = r'^CREATE TABLE\s+(["`]?)(\w+)\1'
    match = re.match(pattern, sql.strip(), re.IGNORECASE)
    
    if match:
        table_identifier = match.group(0)
        replacement = table_identifier.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS')
        return sql.replace(table_identifier, replacement, 1)
    else:
        # Fallback: simple replacement if pattern doesn't match
        return sql.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS', 1)

def generate_indexes_sql():
    """
    Generate performance indexes for the tables
    """
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_kply_system_users_email ON kply_system_users(usr_email)",
        "CREATE INDEX IF NOT EXISTS idx_kply_system_users_username ON kply_system_users(usr_username)",
        "CREATE INDEX IF NOT EXISTS idx_kply_system_users_role ON kply_system_users(usr_rol_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_parishes_forane ON kply_parishes(par_for_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_communities_parish ON kply_communities(com_par_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_communities_forane ON kply_communities(com_for_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_families_community ON kply_families(fam_com_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_families_unique_no ON kply_families(fam_unique_no)",
        "CREATE INDEX IF NOT EXISTS idx_kply_individuals_unique_no ON kply_individuals(ind_unique_no)",
        "CREATE INDEX IF NOT EXISTS idx_kply_individuals_email ON kply_individuals(ind_email)",
        "CREATE INDEX IF NOT EXISTS idx_kply_institutions_unique_no ON kply_institutions(ins_unique_no)",
        "CREATE INDEX IF NOT EXISTS idx_kply_family_contributions_family ON kply_family_contributions(fcon_fam_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_individual_contributions_individual ON kply_individual_contributions(icon_ind_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_institution_contributions_institution ON kply_institution_contributions(incon_ins_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_photos_forane ON kply_photos(pho_for_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_photos_parish ON kply_photos(pho_par_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_photos_community ON kply_photos(pho_com_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_photos_family ON kply_photos(pho_fam_id)",
        "CREATE INDEX IF NOT EXISTS idx_kply_photos_institution ON kply_photos(pho_ins_id)",
    ]
    return indexes

async def test_connection():
    """
    Test database connection before proceeding
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment variables")
        return False
    
    try:
        conn = await asyncpg.connect(database_url)
        result = await conn.fetchval("SELECT 1")
        await conn.close()
        print("✅ Database connection test successful")
        return True
    except Exception as e:
        print(f"❌ Database connection test failed: {e}")
        return False

async def create_tables_from_models():
    """
    Create tables using SQL generated from SQLAlchemy models
    """
    # Test connection first
    if not await test_connection():
        return False
    
    database_url = os.getenv("DATABASE_URL")
    
    print("🔗 Connecting to Supabase...")
    
    try:
        conn = await asyncpg.connect(database_url)
        print("✅ Connected to Supabase successfully!")
        
        # Enable UUID extension
        await conn.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
        print("✅ UUID extension enabled")
        
        # Create schema if needed
        schema = os.getenv("DATABASE_SCHEMA", "public")
        if schema and schema.lower() != 'public':
            await conn.execute(f'CREATE SCHEMA IF NOT EXISTS "{schema}"')
            print(f"✅ Schema '{schema}' created/verified")
        
        # Generate SQL from models
        print("🔨 Generating SQL from SQLAlchemy models...")
        tables_sql = get_create_table_sql()
        
        if not tables_sql:
            print("❌ No tables SQL generated")
            await conn.close()
            return False
        
        # Create tables
        print(f"📋 Creating {len(tables_sql)} tables...")
        successful_tables = 0
        failed_tables = 0
        
        for table_info in tables_sql:
            table_name = table_info['name']
            sql = table_info['sql']
            
            try:
                # Add IF NOT EXISTS to the SQL
                sql_with_if_not_exists = add_if_not_exists(sql)
                await conn.execute(sql_with_if_not_exists)
                print(f"✅ Table '{table_name}' created/verified")
                successful_tables += 1
            except Exception as e:
                print(f"❌ Error creating table '{table_name}': {e}")
                print(f"   SQL: {sql[:200]}...")
                failed_tables += 1
                # Continue with other tables
        
        print(f"📊 Table creation summary: {successful_tables} successful, {failed_tables} failed")
        
        if successful_tables > 0:
            # Create indexes only if some tables were created
            print("🔍 Creating performance indexes...")
            indexes = generate_indexes_sql()
            successful_indexes = 0
            
            for index_sql in indexes:
                try:
                    await conn.execute(index_sql)
                    successful_indexes += 1
                except Exception as e:
                    print(f"⚠️  Warning: Could not create index: {e}")
            
            print(f"✅ Created {successful_indexes}/{len(indexes)} indexes")
        
        await conn.close()
        
        if successful_tables > 0:
            print("🎉 Tables created successfully from SQLAlchemy models!")
            return True
        else:
            print("❌ No tables were created successfully")
            return False
        
    except Exception as e:
        print(f"❌ Connection error: {e}")
        import traceback
        traceback.print_exc()
        return False

def save_sql_to_file():
    """
    Generate and save SQL to a file for manual execution
    """
    print("💾 Generating SQL file...")
    
    tables_sql = get_create_table_sql()
    indexes_sql = generate_indexes_sql()
    
    if not tables_sql:
        print("❌ No SQL generated")
        return
    
    # Create SQL file
    sql_file_path = Path(__file__).parent.parent / "generated_tables.sql"
    
    try:
        with open(sql_file_path, 'w', encoding='utf-8') as f:
            f.write("-- ============================================================================\n")
            f.write("-- KPLY DIALYSIS PROJECT - AUTO-GENERATED TABLE CREATION SCRIPT\n")
            f.write(f"-- Generated from SQLAlchemy models on {asyncio.get_event_loop().time()}\n")
            f.write("-- ============================================================================\n\n")
            f.write("-- Enable UUID extension\n")
            f.write('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";\n\n')
            f.write("-- Create tables\n")
            f.write("-- ============================================================================\n\n")
            
            for table_info in tables_sql:
                table_name = table_info['name']
                sql = table_info['sql']
                sql_with_if_not_exists = add_if_not_exists(sql)
                
                f.write(f"-- Table: {table_name}\n")
                f.write(f"{sql_with_if_not_exists};\n\n")
            
            f.write("-- Performance Indexes\n")
            f.write("-- ============================================================================\n\n")
            
            for index_sql in indexes_sql:
                f.write(f"{index_sql};\n")
            
            f.write("\n-- ============================================================================\n")
            f.write("-- END OF AUTO-GENERATED SCRIPT\n")
            f.write("-- ============================================================================\n")
        
        print(f"✅ SQL file saved to: {sql_file_path}")
        print("   You can now execute this SQL in your Supabase SQL Editor")
        return True
        
    except Exception as e:
        print(f"❌ Error saving SQL file: {e}")
        return False

async def main():
    print("🚀 KPLY Dialysis - Dynamic Table Creation")
    print("=" * 60)
    print("This script generates tables from your SQLAlchemy models")
    print("=" * 60)
    
    # Option 1: Save SQL to file
    print("\n📁 Option 1: Generate SQL file for manual execution")
    file_saved = save_sql_to_file()
    
    if not file_saved:
        print("❌ Could not generate SQL file. Please check your model imports.")
        return
    
    # Option 2: Direct execution
    print(f"\n🔧 Option 2: Execute directly on Supabase")
    user_input = input("Do you want to execute the SQL directly on Supabase? (y/N): ")
    
    if user_input.lower() in ['y', 'yes']:
        success = await create_tables_from_models()
        if success:
            print("\n✅ Tables created successfully!")
        else:
            print("\n❌ Table creation failed. Check the generated SQL file for manual execution.")
    else:
        print("\n💡 Use the generated SQL file in your Supabase SQL Editor")

if __name__ == "__main__":
    asyncio.run(main())