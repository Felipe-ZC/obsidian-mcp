import os

import httpx
from mcp.server.fastmcp import FastMCP

from obsidian_vault import ObsidianVault

USER_AGENT = "weather-mcp/0.1 (contact@example.com)"
VAULT_PATH = os.getenv("VAULT_PATH", "")

mcp = FastMCP("obsidian-mcp")
vault = ObsidianVault(VAULT_PATH)


@mcp.tool()
async def list_notes() -> str:
    """Get all notes in a vault.

    Args:
        vault_path: The path to an Obsidian vault.
    """
    return vault.list_notes()
