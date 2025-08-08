# Running Any MCP Server Locally: From JSON Config to HTTP Transport

## Understanding MCP Server Configurations

Most MCP (Model Context Protocol) servers are designed to run inside MCP clients like Cursor, Claude Desktop, or VS Code. These clients use JSON configuration files that tell them how to start and connect to MCP servers.

Here's a typical MCP configuration:

```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    },
    "jira-mcp": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_PERSONAL_TOKEN": "your_token_here",
        "JIRA_URL": "https://your-jira-instance.com"
      }
    }
  }
}
```

## Reading the Configuration

When you see an MCP configuration, look for these key elements:

1. **`command`**: The executable to run (e.g., `uvx`, `python`, `node`)
2. **`args`**: Command-line arguments (e.g., `["mcp-atlassian"]`)
3. **`env`**: Environment variables the server needs
4. **`url`**: For remote servers (skip this for local execution)

## What is `uvx`?

`uvx` is a tool from the `uv` Python package manager that downloads and runs Python packages without installing them globally. It's like `npx` for Python. When you see:

```json
"command": "uvx",
"args": ["mcp-atlassian"]
```

This means: "Download and run the `mcp-atlassian` package using `uvx`"

## Converting to Local HTTP Server

Most MCP servers support multiple transport methods. The default is usually stdio (for client integration), but many also support HTTP/SSE for standalone operation.

### Step 1: Extract the Command

From your JSON config, extract:
- **Command**: `uvx`
- **Package**: `mcp-atlassian`
- **Environment**: `JIRA_PERSONAL_TOKEN`, `JIRA_URL`

### Step 2: Check for HTTP Transport Support

Most MCP servers support HTTP transport. Common flags include:
- `--transport http` or `--transport streamable-http`
- `--transport sse` (Server-Sent Events)
- `--port <port_number>`
- `--host <host>`

### Step 3: Run Locally

Using our `mcp-atlassian` example:

```bash
# Set environment variables
export JIRA_PERSONAL_TOKEN="your_token"
export JIRA_URL="https://your-jira-instance.com"

# Run with HTTP transport
uvx mcp-atlassian --transport streamable-http --port 9000 -vv
```

Or create a `.env` file:
```bash
# .env
JIRA_PERSONAL_TOKEN=your_actual_token_here
JIRA_URL=https://your-jira-instance.com
```

Then run:
```bash
uvx mcp-atlassian --transport streamable-http --port 9000 -vv
```

## Universal Pattern

This approach works with almost any MCP server:

1. **Extract the command and args** from your MCP JSON
2. **Set the required environment variables**
3. **Add transport flags** (`--transport`, `--port`, etc.)
4. **Run the command**

### Examples for Other Servers

**For a Python-based MCP server:**
```json
{
  "command": "python",
  "args": ["path/to/server.py"],
  "env": {"API_KEY": "secret"}
}
```

Becomes:
```bash
API_KEY="secret" python path/to/server.py --transport http --port 9000
```

**For a Node.js MCP server:**
```json
{
  "command": "npx",
  "args": ["@modelcontextprotocol/server-filesystem", "/path/to/files"],
  "env": {"DEBUG": "true"}
}
```

Becomes:
```bash
DEBUG=true npx @modelcontextprotocol/server-filesystem /path/to/files --transport http --port 9000
```

## Client Configuration

Once running, update your MCP client configuration:

```json
{
  "mcpServers": {
    "my-server": {
      "url": "http://localhost:9000/mcp"
    }
  }
}
```

## Key Insights

- **Most MCP servers support HTTP transport** - look for `--transport` flags
- **Environment variables are crucial** - extract them from the JSON config
- **`uvx` is Python's `npx`** - it downloads and runs packages on-demand
- **Port 9000 is common** - but check the server's documentation
- **Verbose logging helps** - use `-v` or `-vv` flags for debugging

## Result

You can now run any MCP server as a standalone HTTP service, making it accessible to multiple clients and easier to debug. This approach works with the vast majority of MCP servers available today.

---

*This pattern transforms any stdio-based MCP server into a persistent HTTP service, giving you the flexibility to run MCP servers independently of specific clients.* 