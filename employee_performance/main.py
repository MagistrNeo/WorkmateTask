"""Основной скрипт для анализа эффективности разработчиков."""

import argparse
from typing import List, Dict, Any
import sys

from data_loader import load_employee_data
from reports import ReportGenerator
from validators import validate_files_exist


def parse_args() -> argparse.Namespace:
    """Парсинг аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Анализ эффективности работы разработчиков"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV файлам с данными сотрудников"
    )
    parser.add_argument(
        "--report",
        choices=["performance"],
        required=True,
        help="Тип отчета для генерации"
    )
    return parser.parse_args()


def main():
    """Основная функция скрипта."""
    args = parse_args()
    
    try:
        # Валидация файлов
        validate_files_exist(args.files)
        
        # Загрузка данных из всех файлов
        employees = []
        for file_path in args.files:
            employees.extend(load_employee_data(file_path))
        
        if not employees:
            print("Ошибка: Нет данных для анализа")
            sys.exit(1)
        
        # Генерация отчета
        generator = ReportGenerator()
        report = generator.generate_report(args.report, employees)
        
        # Вывод отчета
        generator.print_report(report, args.report)
        
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Ошибка данных: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":

    main()
