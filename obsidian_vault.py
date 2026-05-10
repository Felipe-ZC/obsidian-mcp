import re
from pathlib import Path
from shutil import copytree

from vault_utils import (
    VaultItem,
    VaultItemType,
    create_vault_item_from_path_item,
    get_sorted_files,
    is_valid_obsidian_folder,
    is_valid_obsidian_note,
)

DEFAULT_BACKUP_PATH = "./vault-backup"


class ObsidianVault:
    def __init__(self, vault_path: str, backup_path: str = DEFAULT_BACKUP_PATH):
        self.vault_path: Path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(
                f"The provided vault path does not exist! Path is {vault_path}"
            )
        self.backup_path: Path = Path(backup_path)
        self._root_vault_item: VaultItem | None = None

    @property
    def root(self) -> VaultItem:
        if self._root_vault_item is None:
            self._root_vault_item = self._build_vault_tree()
        return self._root_vault_item

    def make_backup(self):
        if not self.backup_path.exists():
            self.backup_path.mkdir(parents=True, exist_ok=True)
        elif not self.backup_path.is_dir():
            raise ValueError(
                f"The provided backup path is not a directory! Path is {self.backup_path}"
            )
        copytree(self.vault_path, self.backup_path, dirs_exist_ok=True)

    def search_vault(self, query: str) -> list[VaultItem]:
        return self._search_vault_rec(self.root, query)

    def list_notes(self, folder: str = "") -> VaultItem:
        if folder:
            target_folder = self._find_folder(folder, self.root)
            if not target_folder:
                raise ValueError(
                    f"A folder with name {folder} was not found in this Obsidian vault!"
                )
            return target_folder
        return self.root

    def _search_vault_rec(
        self,
        root: VaultItem,
        query: str,
    ) -> list[VaultItem]:
        matches: list[VaultItem] = []
        for vault_item in root.children:
            if re.search(query, vault_item.name):
                matches.append(vault_item)
            if vault_item.type == VaultItemType.FOLDER:
                matches.extend(self._search_vault_rec(vault_item, query))
        return matches

    def _find_folder(self, folder: str, root: VaultItem) -> VaultItem | None:
        for vault_item in root.children:
            if vault_item.type == VaultItemType.FOLDER:
                if vault_item.name == folder:
                    return vault_item
                result = self._find_folder(folder, vault_item)
                if result:
                    return result
        return None

    def _build_vault_tree(self):
        return VaultItem(
            name=self.vault_path.name,
            path_str=str(self.vault_path),
            type=VaultItemType.FOLDER,
            children=self._get_vault_item_children(self.vault_path),
        )

    def _get_vault_item_children(self, root_path: Path) -> list[VaultItem]:
        children: list[VaultItem] = []
        for item in get_sorted_files(root_path):
            if is_valid_obsidian_folder(item) or is_valid_obsidian_note(item):
                new_vault_item = create_vault_item_from_path_item(item)
                if item.is_dir():
                    new_vault_item.children.extend(self._get_vault_item_children(item))
                children.append(new_vault_item)
        return children
