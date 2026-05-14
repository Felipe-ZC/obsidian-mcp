import json
import os

from mcp.server.fastmcp import FastMCP

from obsidian_vault import ObsidianVault
from vault_utils import VaultItem

USER_AGENT = "obsidian-mcp/0.1 (contact@example.com)"
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
    Finds and returns the metadata of a notes or folders in the Obsidian vault.
    Use this tool when you have a note or folder name and need the full VaultItem
    metadata (including the absolute path_str).

    Args:
        query: The name of the note or folder in the vault.
    """
    results = [result.to_dict() for result in vault.search_vault(query)]
    return json.dumps(results, indent=2)


@mcp.tool()
async def find_note(note_name: str = "", note_path: str = "") -> str:
    """
    Finds and returns the metadata of a specific note in the Obsidian vault.
    Use this tool when you have a note name or path and need the full VaultItem
    metadata (including the absolute path_str) before reading or writing to it.

    Args:
        note_name: The filename of the note (e.g. "Daily Log.md").
        note_path: The absolute path of the note. Provide either note_name
        or note_path, at least one is required.
    """
    try:
        result: VaultItem | None = vault.find_note(note_name, note_path)
    except ValueError as e:
        return str(e)
    if not result:
        return "No Obsidian note found with that name or path in the vault."
    return json.dumps(result.to_dict(), indent=2)


@mcp.tool()
async def read_note(note_path: str) -> str:
    """
    Returns the full text content of an Obsidian note.
    Use this when the user asks to read, summarize, or analyze a note's contents.
    The note_path argument must be the absolute path of the note — use the path_str
    field from a VaultItem returned by find_note or search_vault.

    Args:
        note_path: The absolute path of the note to read.
    """
    result: VaultItem | None = vault.find_note(note_path=note_path)
    if not result:
        return "No Obsidian note found with that path in the vault."
    return vault.read_note(result)


@mcp.tool()
async def append_to_note(note_path: str, append_markdown_text: str):
    """
    Appends markdown text to the end of an Obsidian note.
    Use this when the user asks to add content to an existing note.

    Before calling this tool:
    1. Use find_note or search_vault to confirm the exact note and get its path_str.
    2. ALWAYS confirm with the user which note will be modified before appending.

    Args:
        note_path: The absolute path of the note to append to (from path_str of a VaultItem).
        append_markdown_text: The markdown text to append.
    """
    result: VaultItem | None = vault.find_note(note_path=note_path)
    if not result:
        return "No Obsidian note found with that path in the vault."
    vault.append_to_note(result, append_markdown_text)


if __name__ == "__main__":
    mcp.run(transport="stdio")
