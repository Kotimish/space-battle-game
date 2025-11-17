from pathlib import Path


def load_private_key(primary_path: Path, fallback_path: Path | None = None) -> str:
    """
    Читает приватный ключ из файла.
    :param primary_path: Путь к файлу ключа (PEM).
    :param fallback_path: Путь к файлу резервного ключа (PEM).
    :return: Содержимое файла как строка.
    :raises FileNotFoundError: Если файл не найден.
    :raises ValueError: Если файл пуст.
    """
    def _read_key(path: Path) -> str:
        with open(path, "r") as file:
            return file.read().strip()

    if primary_path.exists():
        key =  _read_key(primary_path)
    elif fallback_path and fallback_path.exists():
        key = _read_key(fallback_path)
    else:
        raise FileNotFoundError(f"Private key file not found at: {primary_path}")
    if not key:
        raise ValueError(f"Private key file is empty: {primary_path}")
    return key
