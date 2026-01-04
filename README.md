# mcp-arxiv

MCP server to give client the ability to search papers through Arxiv

# Usage

For this MCP server to work, add the following configuration to your MCP config file:

```json
{
  "mcpServers": {
    "arxiv": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/mcp-arxiv",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```
