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
        "C:/Users/Braincore/Documents/GitHub/mcp-arxiv",
        "run",
        "python",
        "main.py"
      ],
      "env": {
        "ARXIV_PAPER_STORAGE_PATH": "C:/Users/Braincore/Downloads/ArxivPapers"
      }
    }
  }
}
```
