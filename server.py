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


@mcp.tool()
async def search_vault(query: str = "") -> str:
    """
    Returns a JSON list of notes or folders in the Obsidian vault that match
    the query argument. Use this tool when the user asks to search for a specific
    note or folder, if the user asks to search the vault but does not provide a
    query, this function will return the result of list_notes (all the notes in the vault).

    Args:
        query: The search query to use to filter out notes and folders in the vault.

    """
    if not query:
        return await list_notes()
    results = [result.to_dict() for result in vault.search_vault(query)]
    return json.dumps(results, indent=2)


if __name__ == "__main__":
    mcp.run(transport="stdio")
