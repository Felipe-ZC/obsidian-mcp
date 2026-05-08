from dataclasses import dataclass, field
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


@dataclass
class VaultItem:
    name: str
    path_str: str
    type: VaultItemType
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
        children=children or [],
    )
