# --- CONFIGURATION (Update these paths) ---
$PYTHON_EXE = "C:/Users/EPARDET/weather-mcp-server/venv/Scripts/python.exe"
$SERVER_PY = "C:/Users/EPARDET/weather-mcp-server/venv/test_mcp_cloud.py"

# --- CREDENTIALS ---
$TOKEN = "dapi38407e8c74a1cda6151e1decdb035d5d"
$HOSTNAME= "dbc-94075d17-c048.cloud.databricks.com"
$PATH = "/sql/1.0/warehouses/1519f7c7bfd6bf44"
$CATALOG = "ecommerce_course"
$SCHEMA = "silver"

# --- EXECUTION ---
# Using the -e flag ensures the variables are injected directly into the child process
npx @modelcontextprotocol/inspector `
    -e DATABRICKS_TOKEN=$TOKEN `
    -e DATABRICKS_SERVER_HOSTNAME=$HOSTNAME `
    -e DATABRICKS_HTTP_PATH=$PATH `
    -e DATABRICKS_CATALOG=$CATALOG `
    -e DATABRICKS_SCHEMA=$SCHEMA `
    $PYTHON_EXE $SERVER_PY
    