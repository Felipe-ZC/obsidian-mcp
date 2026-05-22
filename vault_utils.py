import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import TypedDict


class VaultItemType(Enum):
    NOTE = "note"
    FOLDER = "folder"


class VaultItemDict(TypedDict, total=False):
    name: str
    path_str: str
    type: str
    children: list["VaultItemDict"]


@dataclass
class VaultItem:
    name: str
    path_str: str
    type: VaultItemType
    text_content: str
    children: list["VaultItem"] = field(default_factory=list)

    def to_dict(self) -> VaultItemDict:
        result: VaultItemDict = {
            "name": self.name,
            "path_str": self.path_str,
            "type": self.type.value,
        }
        if self.children:
            result["children"] = [child.to_dict() for child in self.children]
        return result


def create_vault_item_from_path_item(
    item: Path, children: list[VaultItem] | None = None
) -> VaultItem:
    vault_item_type = VaultItemType.FOLDER if item.is_dir() else VaultItemType.NOTE
    return VaultItem(
        name=item.name,
        path_str=str(item),
        type=vault_item_type,
        text_content=item.read_text() if item.is_file() else "",
        children=children or [],
    )


def is_valid_obsidian_folder(item: Path) -> bool:
    return item.is_dir() and not item.name.startswith(".")


def is_valid_obsidian_note(item: Path) -> bool:
    return item.is_file() and item.name.endswith(".md")


def get_sorted_files(root: Path) -> list[Path]:
    return sorted(root.glob("*"), key=lambda p: (p.is_file(), p.name.lower()))


def get_vault_item_children(root_path: Path) -> list[VaultItem]:
    children: list[VaultItem] = []
    for item in get_sorted_files(root_path):
        if is_valid_obsidian_folder(item) or is_valid_obsidian_note(item):
            new_vault_item = create_vault_item_from_path_item(item)
            if item.is_dir():
                new_vault_item.children.extend(get_vault_item_children(item))
            children.append(new_vault_item)
    return children


def search_vault_rec(root: VaultItem, query: str) -> list[VaultItem]:
    matches: list[VaultItem] = []
    for vault_item in root.children:
        if vault_item.type == VaultItemType.NOTE and (
            query in vault_item.name or query in vault_item.text_content
        ):
            matches.append(vault_item)
        if vault_item.type == VaultItemType.FOLDER:
            matches.extend(search_vault_rec(vault_item, query))
    return matches


def find_folder(folder: str, root: VaultItem) -> VaultItem | None:
    for vault_item in root.children:
        if vault_item.type == VaultItemType.FOLDER:
            if vault_item.name == folder:
                return vault_item
            result = find_folder(folder, vault_item)
            if result:
                return result
    return None


def find_note(
    root: VaultItem, note_name: str = "", note_path: str = ""
) -> VaultItem | None:
    for vault_item in root.children:
        if vault_item.type == VaultItemType.NOTE:
            if vault_item.name == note_name or vault_item.path_str == note_path:
                return vault_item
        elif vault_item.type == VaultItemType.FOLDER:
            result = find_note(vault_item, note_name, note_path)
            if result:
                return result
    return None
