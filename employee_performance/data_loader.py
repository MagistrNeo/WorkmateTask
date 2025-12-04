"""Модуль для загрузки данных из CSV файлов."""

import csv
from typing import List
from dataclasses import dataclass


@dataclass
class Employee:
    """Модель данных сотрудника."""
    name: str
    position: str
    completed_tasks: int
    performance: float
    skills: str
    team: str
    experience_years: int


def load_employee_data(file_path: str) -> List[Employee]:
    """
    Загружает данные сотрудников из CSV файла.
    
    Args:
        file_path: Путь к CSV файлу
        
    Returns:
        Список объектов Employee
        
    Raises:
        ValueError: Если файл имеет неверный формат
    """
    employees = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            # Проверяем наличие обязательных колонок
            required_columns = ['name', 'position', 'completed_tasks', 
                              'performance', 'skills', 'team', 'experience_years']
            
            if reader.fieldnames is None:
                raise ValueError(f"Файл {file_path} пустой или имеет неверный формат")
            
            if not all(col in reader.fieldnames for col in required_columns):
                missing = [col for col in required_columns if col not in reader.fieldnames]
                raise ValueError(f"Файл {file_path} отсутствуют колонки: {missing}")
            
            for i, row in enumerate(reader, 1):
                try:
                    employee = Employee(
                        name=row['name'].strip(),
                        position=row['position'].strip(),
                        completed_tasks=int(row['completed_tasks']),
                        performance=float(row['performance']),
                        skills=row['skills'].strip(),
                        team=row['team'].strip(),
                        experience_years=int(row['experience_years'])
                    )
                    employees.append(employee)
                except (ValueError, KeyError) as e:
                    print(f"Предупреждение: Строка {i} пропущена - ошибка: {e}")
                    continue
                    
    except UnicodeDecodeError:
        # Пробуем другую кодировку
        try:
            with open(file_path, 'r', encoding='cp1251') as file:
                reader = csv.DictReader(file)
                for i, row in enumerate(reader, 1):
                    try:
                        employee = Employee(
                            name=row['name'].strip(),
                            position=row['position'].strip(),
                            completed_tasks=int(row['completed_tasks']),
                            performance=float(row['performance']),
                            skills=row['skills'].strip(),
                            team=row['team'].strip(),
                            experience_years=int(row['experience_years'])
                        )
                        employees.append(employee)
                    except (ValueError, KeyError) as e:
                        print(f"Предупреждение: Строка {i} пропущена - ошибка: {e}")
                        continue
        except:
            raise ValueError(f"Не удалось прочитать файл {file_path}. Проверьте кодировку.")
    
    return employees