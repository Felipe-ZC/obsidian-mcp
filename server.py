import json
import os

# import httpx
from mcp.server.fastmcp import FastMCP

from obsidian_vault import ObsidianVault

USER_AGENT = "weather-mcp/0.1 (contact@example.com)"
VAULT_PATH = os.getenv("VAULT_PATH", "")

mcp = FastMCP("obsidian-mcp")
vault = ObsidianVault(VAULT_PATH)


@mcp.tool()
async def list_notes(folder: str = "") -> str:
    """
    Returns the metadata of an Obsidian vault, this being a JSON
    document that represents an Obsidian vault as a tree structure.
    Each entry in the JSON doc has a name, a path string, a type
    (folder or note) and the children under this folder (more folders or notes).

    Only folders can have children, notes are the leaves of the tree.
    Use this tool when a user asks for all the notes in the vault or
    just the ones in a specific folder.

    Args:
        folder: A string containing the name of the folder whose notes should be listed.

    """
    return json.dumps(vault.list_notes(folder).to_dict(), indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
