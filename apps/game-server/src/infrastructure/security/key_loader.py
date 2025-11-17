from pathlib import Path


def load_public_key(primary_path: Path, fallback_path: Path | None = None) -> str:
    """
    Читает публичный ключ из файла.
    :param primary_path: Путь к файлу ключа (PEM).
    :param fallback_path: Резервный путь (например, для тестов).
    :return: Содержимое файла как строка.
    :raises FileNotFoundError: Если ни основной, ни fallback-файл не найдены.
    :raises ValueError: Если файл пуст.
    """
    def _read_key(path: Path) -> str:
        with open(path, "r") as file:
            return file.read().strip()

    if primary_path.exists():
        key = _read_key(primary_path)
    elif fallback_path and fallback_path.exists():
        key = _read_key(fallback_path)
    else:
        raise FileNotFoundError(f"Public key not found at: {primary_path} or fallback {fallback_path}")

    if not key:
        raise ValueError(f"Public key file is empty: {primary_path}")

    return key