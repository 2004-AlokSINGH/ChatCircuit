from langchain_mcp_adapters.client import MultiServerMCPClient
import os

def get_mcp_client():
    # Get environment variables to pass to subprocesses
    env = os.environ.copy()
    
    mcp_client = MultiServerMCPClient({
        "calculator": {
            "transport": "stdio",
            "command": "python",
            "args": ["mcpserver/McpCalculatorServer.py"],
            "env": env,
        },
        "jira": {
            "transport": "stdio",
            "command": "python",
            "args": ["mcpserver/McpJiraServer.py"],
            "env": env,
        },
    })
    return mcp_client
