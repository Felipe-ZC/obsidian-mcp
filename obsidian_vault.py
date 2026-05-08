import json
from dataclasses import dataclass, field
from pathlib import Path
from shutil import copytree

from utils import (
    VaultItemDict,
    VaultItemType,
    get_sorted_files,
    is_valid_obsidian_folder,
    is_valid_obsidian_note,
)

DEFAULT_BACKUP_PATH = "./vault-backup"


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


class ObsidianVault:
    def __init__(self, vault_path: str, backup_path: str = DEFAULT_BACKUP_PATH):
        self.vault_path: Path = Path(vault_path)
        self.backup_path: Path = Path(backup_path)
        if not self.vault_path.exists():
            raise ValueError(
                f"The provided vault path does not exist! Path is {vault_path}"
            )

    def make_backup(self):
        if not self.backup_path.exists():
            self.backup_path.mkdir(parents=True, exist_ok=True)
        elif not self.backup_path.is_dir():
            raise ValueError(
                f"The provided backup path is not a directory! Path is {self.backup_path}"
            )
        copytree(self.vault_path, self.backup_path, dirs_exist_ok=True)

    def list_notes(self) -> VaultItem:
        root_vault_item = VaultItem(
            name=self.vault_path.name,
            path_str=str(self.vault_path),
            type=VaultItemType.FOLDER,
            children=self._gather_vault_item_children(self.vault_path),
        )
        return root_vault_item

    def _gather_vault_item_children(self, root_path: Path) -> list[VaultItem]:
        vault_item_list: list[VaultItem] = []

        for item in get_sorted_files(root_path):
            if is_valid_obsidian_folder(item) or is_valid_obsidian_note(item):
                new_vault_item = create_vault_item_from_path_item(item)
                if item.is_dir():
                    new_vault_item.children.extend(
                        self._gather_vault_item_children(item)
                    )
                vault_item_list.append(new_vault_item)

        return vault_item_list


vault = ObsidianVault("/home/zubuddy/Documents/obsidian/Felipe")
root_vault_item = vault.list_notes()
print(json.dumps(root_vault_item.to_dict(), indent=2))
