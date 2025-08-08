#!/bin/bash

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Set default values if not provided
JIRA_PORT=${JIRA_PORT:-9000}

# Build the command with expanded variables
if [ -z "$JIRA_COMMAND" ]; then
    JIRA_COMMAND="uvx mcp-atlassian --transport streamable-http --port $JIRA_PORT -vv"
else
    # Expand any variables in the custom command
    JIRA_COMMAND=$(eval echo "$JIRA_COMMAND")
fi

# Validate required environment variables
if [ -z "$JIRA_PERSONAL_TOKEN" ]; then
    echo "Error: JIRA_PERSONAL_TOKEN is required"
    exit 1
fi

if [ -z "$JIRA_URL" ]; then
    echo "Error: JIRA_URL is required"
    exit 1
fi

# Print configuration
echo "Starting MCP server with configuration:"
echo "  JIRA_URL: $JIRA_URL"
echo "  JIRA_PORT: $JIRA_PORT"
echo "  JIRA_COMMAND: $JIRA_COMMAND"
echo "  Token configured: ${JIRA_PERSONAL_TOKEN:0:10}..."

# Execute the command
echo "Executing: $JIRA_COMMAND"
exec $JIRA_COMMAND 