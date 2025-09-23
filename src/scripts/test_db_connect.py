import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    database_url = os.getenv("DATABASE_URL")
    
    if not database_url:
        print("ERROR: DATABASE_URL not found in environment variables")
        return
    
    # Print URL with masked password for debugging
    masked_url = database_url.replace(database_url.split('@')[0].split(':')[-1], '***')
    print(f"Attempting connection to: {masked_url}")
    
    try:
        conn = await asyncpg.connect(database_url)
        print("✅ Connection successful!")
        
        # Test a simple query
        result = await conn.fetchval("SELECT version()")
        print(f"PostgreSQL version: {result}")
        
        await conn.close()
        print("✅ Connection closed successfully")
        
    except asyncpg.exceptions.InvalidPasswordError as e:
        print(f"❌ Password authentication failed: {e}")
        print("Check your password and username in the DATABASE_URL")
        
    except asyncpg.exceptions.ConnectionDoesNotExistError as e:
        print(f"❌ Connection error: {e}")
        print("Check your host, port, and database name")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())