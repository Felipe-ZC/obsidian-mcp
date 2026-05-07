from pathlib import Path
from shutil import copytree

from utils import get_sorted_files, is_valid_obsidian_folder, is_valid_obsidian_note

LIST_SEPARATOR_STR = "\n"
DEFAULT_BACKUP_PATH = "./vault-backup"
EMPTY_SPACE_STR = " "


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

    def list_notes(self) -> str:
        str_list = self._get_notes_list_str(self.vault_path)
        return LIST_SEPARATOR_STR.join(str_list)

    def _get_notes_list_str(self, root: Path, depth: int = 0) -> list[str]:
        output_str_list: list[str] = []
        spacer: str = EMPTY_SPACE_STR * (depth * 2)
        for item in get_sorted_files(root):
            if is_valid_obsidian_folder(item):
                output_str_list.append(f"{spacer}- {item.name}")
                output_str_list.extend(self._get_notes_list_str(item, depth + 1))
            elif is_valid_obsidian_note(item):
                output_str_list.append(f"{spacer}|- {item.name}")
        return output_str_list
