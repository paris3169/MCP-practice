# MCP-practice
this is repository for all my MCP code practices

# Databricks MCP Server

A Model Context Protocol (MCP) server that provides tools for interacting with Databricks SQL Analytics.

## Files Overview

- **`venv/test_mcp_cloud.py`**: Main MCP server script providing Databricks SQL tools
- **`venv/databricks_connection.py`**: Connection test script to verify Databricks credentials
- **`venv/run_inspector.ps1`**: PowerShell script to launch MCP inspector with environment variables
- **`venv/.env`**: Environment variables file (create this with your credentials)
- **`README.md`**: This documentation file

## Features

- **Query Databricks**: Execute SELECT queries on Databricks tables
- **Update Databricks**: Perform INSERT, UPDATE, DELETE operations
- **List Tables**: Browse available tables in your schema
- **Inspect Schema**: Get column information for specific tables

## Prerequisites

- Python 3.8+
- Databricks workspace with SQL Analytics enabled
- Personal Access Token with appropriate permissions

## Installation

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install fastmcp databricks-sql-connector sqlalchemy python-dotenv
   ```

## Configuration

1. Create a `.env` file in the `venv/` directory:
   ```
   DATABRICKS_SERVER_HOSTNAME=your-workspace.databricks.com
   DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
   DATABRICKS_TOKEN=your-personal-access-token
   DATABRICKS_CATALOG=your-catalog-name
   DATABRICKS_SCHEMA=your-schema-name
   ```

2. Test your connection:
   ```bash
   python venv/databricks_connection.py
   ```

## Usage

### Testing the MCP Server

**Using the PowerShell script** (recommended):
1. Edit `venv/run_inspector.ps1` and update the paths and your Databricks credentials
2. Run: `./venv/run_inspector.ps1`

**Manual command**:
```bash
npx @modelcontextprotocol/inspector venv/Scripts/python.exe venv/test_mcp_cloud.py
```

**Important**: Before running `run_inspector.ps1`, you must edit the file and update:
- The `$PYTHON_EXE` and `$SERVER_PY` paths to match your system
- All the credential variables (`$TOKEN`, `$HOSTNAME`, `$PATH`, `$CATALOG`, `$SCHEMA`) with your actual Databricks information

### Claude Desktop Integration

To use this MCP server with Claude Desktop:

1. **Locate the config file**:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the server configuration**:
   ```json
   {
     "mcpServers": {
       "databricks": {
         "command": "python",
         "args": ["path/to/your/weather-mcp-server/venv/test_mcp_cloud.py"],
         "env": {
           "DATABRICKS_SERVER_HOSTNAME": "your-workspace.databricks.com",
           "DATABRICKS_HTTP_PATH": "/sql/1.0/warehouses/your-warehouse-id",
           "DATABRICKS_TOKEN": "your-personal-access-token",
           "DATABRICKS_CATALOG": "your-catalog-name",
           "DATABRICKS_SCHEMA": "your-schema-name"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop** to load the new MCP server

4. **Test in Claude**: Ask Claude to "list my Databricks tables" or "query my data"

### Using with MCP Clients

The server provides these tools:

- `query_databricks(sql_query)`: Execute SELECT queries (auto-limits to 100 rows)
- `update_databricks(sql_command)`: Execute DML operations
- `list_cloud_tables(limit)`: List available tables
- `inspect_cloud_schema(table_name)`: Get table schema information

### Example Usage

```python
# Query data
result = query_databricks("SELECT * FROM customers WHERE region = 'US'")

# Update data
result = update_databricks("UPDATE customers SET status = 'active' WHERE id = 123")

# List tables
tables = list_cloud_tables(10)

# Get schema
schema = inspect_cloud_schema("customers")
```

## Security Notes

- Only SELECT queries are allowed in `query_databricks`
- Only INSERT, UPDATE, DELETE are allowed in `update_databricks`
- Table names are validated to prevent SQL injection
- Results are truncated to prevent large payloads
- Queries are automatically limited to 100 rows unless specified

## Troubleshooting

1. **Connection fails**: Check your `.env` file and token permissions
2. **No tables found**: Verify catalog and schema names
3. **Inspector doesn't connect**: Ensure correct file paths in commands
4. **Large result errors**: The server automatically limits/truncates results

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with the inspector
5. Submit a pull request

