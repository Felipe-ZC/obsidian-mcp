from pathlib import Path
from shutil import copytree

# NOTES_LIST_SEPARATOR_STR = "|-"
LIST_SEPARATOR_STR = "\n\n"
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
        copytree(self.vault_path, self.backup_path)

    def list_notes(self, root: Path | None = None) -> str:
        str_list = self._get_notes_list_str(self.vault_path)
        return LIST_SEPARATOR_STR.join(str_list)

    def _get_notes_list_str(self, root: Path, depth: int = 0) -> list[str]:
        output_str_list: list[str] = []
        spacer: str = EMPTY_SPACE_STR * (depth * 2)
        for item in root.glob("*"):
            if item.is_dir():
                output_str_list.append(f"{spacer}------ {item.name} ------")
                output_str_list.extend(self._get_notes_list_str(Path(item), depth + 1))
            else:
                output_str_list.append(f"{spacer}- {item.name}")
        return output_str_list


vault = ObsidianVault("/home/zubuddy/Documents/obsidian/Felipe")
print(vault.list_notes())
