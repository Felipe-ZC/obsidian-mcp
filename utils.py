from enum import Enum
from pathlib import Path
from typing import TypedDict


def is_valid_obsidian_folder(item: Path) -> bool:
    return item.is_dir() and not item.name.startswith(".")


def is_valid_obsidian_note(item: Path) -> bool:
    return item.is_file() and item.name.endswith(".md")


def get_sorted_files(root: Path) -> list[Path]:
    return sorted(root.glob("*"), key=lambda p: (p.is_file(), p.name.lower()))


class VaultItemType(Enum):
    NOTE = "note"
    FOLDER = "folder"


class VaultItemDict(TypedDict, total=False):
    name: str
    path_str: str
    type: str
    children: list["VaultItemDict"]
