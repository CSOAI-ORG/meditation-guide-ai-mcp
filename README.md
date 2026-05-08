<div align="center">

# Meditation Guide Ai MCP

**MCP server for meditation guide ai mcp operations**

[![PyPI](https://img.shields.io/pypi/v/meok-meditation-guide-ai-mcp)](https://pypi.org/project/meok-meditation-guide-ai-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![MEOK AI Labs](https://img.shields.io/badge/MEOK_AI_Labs-MCP_Server-purple)](https://meok.ai)

</div>

## Overview

Meditation Guide Ai MCP provides AI-powered tools via the Model Context Protocol (MCP).

## Tools

| Tool | Description |
|------|-------------|
| `get_meditation` | Get a guided meditation script. Styles: calm, focus, sleep, stress. Duration adj |
| `track_session` | Log a completed meditation session. Mood scores 1-10 (1=worst, 10=best). |
| `get_breathing_exercise` | Get a structured breathing exercise. Techniques: box, 478, energize, calm. |
| `suggest_practice` | Suggest a meditation or breathing practice based on your goal and available time |

## Installation

```bash
pip install meok-meditation-guide-ai-mcp
```

## Usage with Claude Desktop

Add to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "meditation-guide-ai": {
      "command": "python",
      "args": ["-m", "meok_meditation_guide_ai_mcp.server"]
    }
  }
}
```

## Usage with FastMCP

```python
from mcp.server.fastmcp import FastMCP

# This server exposes 4 tool(s) via MCP
# See server.py for full implementation
```

## License

MIT © [MEOK AI Labs](https://meok.ai)
