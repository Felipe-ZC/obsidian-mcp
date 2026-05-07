from pathlib import Path


class ObsidianVault:
    def __init__(self, vault_path: str):
        self.vault_path: Path = Path(vault_path)
        if not self.vault_path.exists():
            raise ValueError(
                f"The provided vault path does not exist! Path is {vault_path}"
            )


def main():
    print("Hello from obsidian-mcp!")


if __name__ == "__main__":
    main()
