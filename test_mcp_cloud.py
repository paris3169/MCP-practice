import os
import pandas as pd
from sqlalchemy import create_engine, text
from fastmcp import FastMCP
import dotenv

dotenv.load_dotenv()#dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
print(os.getenv("DATABRICKS_HTTP_PATH"))

# Initialize FastMCP
mcp = FastMCP("Databricks Cloud Manager")

def get_db_engine():
    host = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    print(f"Host: {host}")
    http_path = os.getenv("DATABRICKS_HTTP_PATH")
    token = os.getenv("DATABRICKS_TOKEN")
    catalog = os.getenv("DATABRICKS_CATALOG")
    schema = os.getenv("DATABRICKS_SCHEMA")
    
    # Connection string for databricks-sqlalchemy
    url = f"databricks://token:{token}@{host}?http_path={http_path}&catalog={catalog}&schema={schema}"
    try:
        engine = create_engine(url)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Databricks connection successful")  # Debug print
        return engine
    except Exception as e:
        print(f"Databricks connection failed: {e}")  # Debug print
        raise
    return engine

@mcp.tool()
def query_databricks(sql_query: str) -> str:
    """Runs a SELECT query on Databricks and returns results as a string."""
    try:
        sql_upper = sql_query.upper().strip()
        if not sql_upper.startswith("SELECT"):
            return "Error: Only SELECT queries are allowed."
        
        # Add LIMIT if not present
        if "LIMIT" not in sql_upper:
            sql_query += " LIMIT 100"
        
        engine = get_db_engine()
        with engine.connect() as conn:
            df = pd.read_sql(text(sql_query), conn)
            if df.empty:
                return "Query executed successfully: No data returned."
            
            result = df.fillna("NULL").to_string(index=False)
            
            # Truncate if too long
            if len(result) > 1000:
                result = result[:1000] + "... (truncated)"
            
            return result
    except Exception as e:
        return f"Query Error: {str(e)}"

@mcp.tool()
def update_databricks(sql_command: str) -> str:
    """Executes UPDATE, INSERT, or DELETE commands on cloud tables."""
    try:
        sql_upper = sql_command.upper().strip()
        # Allow only safe DML operations
        if not any(sql_upper.startswith(cmd) for cmd in ["UPDATE", "INSERT", "DELETE"]):
            return "Error: Only UPDATE, INSERT, and DELETE commands are allowed."
        
        engine = get_db_engine()
        with engine.begin() as conn:
            result = conn.execute(text(sql_command))
            return f"Success: {result.rowcount} rows affected."
    except Exception as e:
        return f"Update Error: {str(e)}"

@mcp.tool()
def list_cloud_tables(limit: int = 10) -> str:
    """Lists available tables in the silver schema."""
    if limit > 50:  # Prevent excessive listing
        limit = 50
    query = f"""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = current_schema() 
        LIMIT {limit}
    """
    return query_databricks(query)

@mcp.tool()
def inspect_cloud_schema(table_name: str) -> str:
    """Retrieves columns and types for a specific cloud table."""
    # Validate table name to prevent SQL injection
    if not table_name.replace("_", "").replace(".", "").isalnum():
        return "Error: Invalid table name."
    
    result = query_databricks(f"DESCRIBE TABLE {table_name}")
    
    # Truncate if too long (though DESCRIBE is usually short)
    if len(result) > 1000:
        result = result[:1000] + "... (truncated)"
    
    return result


if __name__ == "__main__":
    mcp.run()
