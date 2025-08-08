# MCP Converter

A collection of tools and knowledge for converting MCP (Model Context Protocol) server configurations from stdio-based to HTTP transport.

## What is this?

This repository contains documentation and examples for running MCP servers locally as HTTP services instead of stdio-based processes. This is useful for:

- Running MCP servers independently of specific clients
- Debugging MCP servers more easily
- Sharing MCP servers across multiple clients
- Creating persistent MCP services

## Contents

- `mcp-atlassian-local-server.md` - Basic guide for running any MCP server locally
- Examples and patterns for different types of MCP servers

## Quick Start

1. Read the [MCP Local Server Guide](mcp-atlassian-local-server.md)
2. Extract your MCP server configuration from your client
3. Follow the universal pattern to run it locally
4. Update your client configuration to point to the local server

## Universal Pattern

```bash
# 1. Extract command and args from your MCP JSON
# 2. Set required environment variables
# 3. Add transport flags
# 4. Run the command

export JIRA_PERSONAL_TOKEN="Your_TOKEN"
export JIRA_URL="https://your_jira_server.com"
uvx mcp-atlassian --transport streamable-http --port 9000 -vv
```

## Container Deployment

For easy deployment, you can use the provided Docker container:

1. **Create your `.env` file:**
   ```bash
   cp env.example .env
   # Edit .env with your actual credentials
   ```

2. **Run with Docker Compose:**
   ```bash
   ./run-container.sh
   ```

3. **Or manually:**
   ```bash
   docker-compose up --build
   ```

The container will:
- Read configuration from `.env` file
- Execute the command specified in `JIRA_COMMAND`
- Listen on the port specified in `JIRA_PORT`
- Automatically restart on failure

## Contributing

Feel free to add more examples and patterns for different types of MCP servers! 