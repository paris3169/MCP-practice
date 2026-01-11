import os
from databricks import sql
import dotenv

dotenv.load_dotenv()

def test_connection():
    # 1. Load your credentials from environment variables
    server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    access_token = os.getenv("DATABRICKS_TOKEN")
    catalog = os.getenv("DATABRICKS_CATALOG")
    schema = os.getenv("DATABRICKS_SCHEMA")

    print(f"--- Attempting to connect to {server_hostname} ---")

    try:
        # 2. Establish the connection
        with sql.connect(
            server_hostname=server_hostname,
            http_path=http_path,
            access_token=access_token,
            catalog=catalog,
            schema=schema
        ) as connection:
            
            # 3. Create a cursor and execute a simple "Sanity Check" query
            with connection.cursor() as cursor:
                print("✅ Connection Established!")
                
                # Verify Catalog and Schema
                cursor.execute("SELECT current_catalog(), current_schema()")
                result = cursor.fetchone()
                print(f"📍 Current Context: Catalog='{result[0]}', Schema='{result[1]}'")
                
                # List first 3 tables to confirm read permissions
                # Use this for Unity Catalog compatibility:
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = current_schema() 
                    LIMIT 3
                """)
                tables = cursor.fetchall()
                print(f"📋 Sample Tables found: {[t[0] for t in tables]}")
                
        print("\n✨ Test Passed: Your credentials are correct and ready for MCP.")

    except Exception as e:
        print(f"\n❌ Connection Failed!")
        print(f"Error Details: {str(e)}")

if __name__ == "__main__":
    test_connection()