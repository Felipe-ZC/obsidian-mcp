from pathlib import Path
from shutil import copytree

from vault_utils import (
    VaultItem,
    VaultItemType,
    find_folder,
    find_note,
    get_vault_item_children,
    search_vault_rec,
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

    # def make_backup(self):
    #     if not self.backup_path.exists():
    #         self.backup_path.mkdir(parents=True, exist_ok=True)
    #     elif not self.backup_path.is_dir():
    #         raise ValueError(
    #             f"The provided backup path is not a directory! Path is {self.backup_path}"
    #         )
    #     copytree(self.vault_path, self.backup_path, dirs_exist_ok=True)

    def search_vault(self, query: str) -> list[VaultItem]:
        return search_vault_rec(self.root, query)

    def list_notes(self, folder: str = "") -> VaultItem:
        if folder:
            target_folder = find_folder(folder, self.root)
            if not target_folder:
                raise ValueError(
                    f"A folder with name {folder} was not found in this Obsidian vault!"
                )
            return target_folder
        return self.root

    def find_note(self, note_name: str = "", note_path: str = "") -> VaultItem | None:
        if not note_name and not note_path:
            raise ValueError("Must provide a the name or path of the note!")
        return find_note(self.root, note_name, note_path)

    def read_note(self, vault_item: VaultItem) -> str:
        with open(vault_item.path_str, "r") as file:
            text_data = file.read()
            return text_data

    def append_to_note(self, vault_item: VaultItem, append_markdown_text: str):
        with open(vault_item.path_str, "a") as file:
            file.write("\n" + append_markdown_text + "\n")

    def _build_vault_tree(self):
        return VaultItem(
            name=self.vault_path.name,
            path_str=str(self.vault_path),
            type=VaultItemType.FOLDER,
            text_content="",
            children=get_vault_item_children(self.vault_path),
        )
