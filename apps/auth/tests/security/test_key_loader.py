from pathlib import Path

import pytest

from src.infrastructure.security.key_loader import load_private_key


def test_load_private_key(tmp_path: Path):
    """Тест чтения файла с ключем"""
    # Создаём временный PEM-файл
    key_path = tmp_path / "test_key.pem"
    dummy_key = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----"
    key_path.write_text(dummy_key)

    # Загружаем
    key = load_private_key(key_path)
    assert key == dummy_key.strip()


def test_load_private_key_file_not_found():
    """Тест отсутствия файла с ключем"""
    with pytest.raises(FileNotFoundError):
        load_private_key(Path("/non/existent/key.pem"))


def test_load_private_key_empty_file(tmp_path: Path):
    """Тест пустого файла с ключем"""
    empty = tmp_path / "empty.pem"
    empty.write_text("")
    with pytest.raises(ValueError, match="empty"):
        load_private_key(empty)
