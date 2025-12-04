"""Тесты для модуля validators."""

import pytest
import tempfile
import os
from src.validators import validate_files_exist


def test_validate_files_exist():
    """Тест валидации существующих файлов."""
    with tempfile.NamedTemporaryFile(delete=False) as f:
        temp_file = f.name
    
    try:
        # Должно пройти без исключений
        validate_files_exist([temp_file])
    finally:
        os.unlink(temp_file)


def test_validate_files_exist_nonexistent():
    """Тест валидации несуществующего файла."""
    with pytest.raises(FileNotFoundError, match="не найден"):
        validate_files_exist(["/nonexistent/file.csv"])


def test_validate_files_exist_directory():
    """Тест валидации директории вместо файла."""
    with tempfile.TemporaryDirectory() as temp_dir:
        with pytest.raises(FileNotFoundError, match="Не файл"):
            validate_files_exist([temp_dir])