"""Модуль для валидации."""

import os
from typing import List


def validate_files_exist(file_paths: List[str]):
    """
    Проверяет существование файлов.
    
    Args:
        file_paths: Список путей к файлам
        
    Raises:
        FileNotFoundError: Если файл не существует
    """
    for file_path in file_paths:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Не файл: {file_path}")