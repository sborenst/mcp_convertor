# MCP Server Container Example

This repository demonstrates how to convert an MCP (Model Context Protocol) JSON configuration into a containerized server that runs locally. Using the Jira MCP server as an example, you'll learn how to:

1. **Extract** the command and environment from MCP JSON
2. **Run** the MCP server locally with HTTP transport
3. **Containerize** it for easy deployment

Most MCP Servers are published to run locally, within a client (like claud desktop, cursor and so on), they often provide a json structure like this: 

```json
{
  "mcpServers": {
    "jira-mcp": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_PERSONAL_TOKEN": "your_token",
        "JIRA_URL": "https://your.jira.server"
      }
    }
  }
}
```

It's often easy to exctract what is needed from this structure to quickly run or wrap these mcp servers outside of a specific tool. This helps when you want to build code or agents that use these tools. 

Let's get right to the point, and you can read a bit more of the process after the Quick Start section.

## Quick Start

### Option 1: Command Line (Fastest)
```bash
# Set environment variables
export JIRA_PERSONAL_TOKEN="your_token_here"
export JIRA_URL="https://your.jira.server"

# Run the MCP server locally
uvx mcp-atlassian --transport streamable-http --port 9000 -vv
```

### Option 2: Container (Recommended)
```bash
# Create .env file
cp env.example .env
# Edit .env with your credentials

# Run with Podman Compose
podman-compose up --build

# Or with legacy Docker Compose
docker-compose up --build
```

The server will be available at `http://localhost:9000`

If you are using cursor, your json file will now look like this:
```json
{
  "mcpServers": {
    "context7": {
      "url": "https://mcp.context7.com/mcp"
    },
    "jira-mcp": {
      "url": "http://localhost:9000/mcp"
    }
  }
}
```

Side note, if you aren't using context7 MCP server in your code assistant, what are you even doin' Mate?

## What This Solves

Most MCP servers are designed to run inside MCP clients (like Cursor, Claude Desktop) using stdio transport. This approach shows you how to:

- **Run MCP servers independently** of specific clients
- **Use HTTP transport** instead of stdio for better debugging
- **Containerize** for consistent deployment across environments
- **Scale** to multiple MCP servers easily

## The Approach

### 1. Extract from MCP JSON
Your MCP configuration looks like this:
```json
{
  "mcpServers": {
    "jira-mcp": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "JIRA_PERSONAL_TOKEN": "your_token",
        "JIRA_URL": "https://your.jira.server"
      }
    }
  }
}
```

### 2. Convert to HTTP Transport
Most MCP servers support HTTP transport with flags:
```bash
# Instead of stdio transport
uvx mcp-atlassian

# Use HTTP transport
uvx mcp-atlassian --transport streamable-http --port 9000 -vv
```

### 3. Containerize
Create a simple container that:
- Reads environment from `.env` file
- Executes the command dynamically
- Exposes the port for external access

## Project Structure

```
├── Dockerfile              # Fedora-based container
├── entrypoint.sh          # Dynamic command execution
├── docker-compose.yml     # Legacy Docker Compose
├── env.example           # Environment template
└── README.md            # This file
```

## Customization

To adapt this for other MCP servers:

1. **Update `env.example`** with your server's environment variables
2. **Modify the command** in `entrypoint.sh` or set via `JIRA_COMMAND` env var
3. **Adjust the port** via `JIRA_PORT` environment variable

## Why This Works

- **`uvx`** is Python's equivalent to `npx` - it runs packages without installation
- **HTTP transport** allows external connections and better debugging
- **Environment variables** make configuration flexible and secure
- **Containerization** ensures consistent runtime across environments

## Testing

Once running, you can test the MCP server by connecting to it from any MCP client or making direct HTTP requests to `http://localhost:9000/mcp/`.

## Contributing

This is an example repository. Feel free to adapt it for your own MCP servers or improve the patterns shown here. 