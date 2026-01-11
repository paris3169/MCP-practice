# --- CONFIGURATION (Update these paths) ---
$PYTHON_EXE = "full local path to yiur local python.exe"
$SERVER_PY = "full local path to the mcp server python script test_mcp_cloud.py"

# --- CREDENTIALS ---
$TOKEN = "put your API token here"
$HOSTNAME= "put your databricks host name here"
$PATH = "/sql/1.0/warehouses/your path"
$CATALOG = "catalogue_name"
$SCHEMA = "schema_name"

# --- EXECUTION ---
# Using the -e flag ensures the variables are injected directly into the child process
npx @modelcontextprotocol/inspector `
    -e DATABRICKS_TOKEN=$TOKEN `
    -e DATABRICKS_SERVER_HOSTNAME=$HOSTNAME `
    -e DATABRICKS_HTTP_PATH=$PATH `
    -e DATABRICKS_CATALOG=$CATALOG `
    -e DATABRICKS_SCHEMA=$SCHEMA `
    $PYTHON_EXE $SERVER_PY

    
