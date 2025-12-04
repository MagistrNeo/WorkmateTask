"""Тесты для модуля data_loader."""

import pytest
import tempfile
import csv
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_loader import load_employee_data, Employee


def test_load_employee_data_valid_file():
    """Тест загрузки данных из валидного файла."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'position', 'completed_tasks', 
                        'performance', 'skills', 'team', 'experience_years'])
        writer.writerow(['Alex', 'Backend Developer', '45', '4.8', 
                        'Python', 'API Team', '5'])
        writer.writerow(['Maria', 'Frontend Developer', '38', '4.7',
                        'React', 'Web Team', '4'])
        temp_file = f.name
    
    try:
        employees = load_employee_data(temp_file)
        
        assert len(employees) == 2
        assert isinstance(employees[0], Employee)
        assert employees[0].name == "Alex"
        assert employees[0].position == "Backend Developer"
        assert employees[0].performance == 4.8
        assert employees[1].name == "Maria"
    finally:
        import os
        os.unlink(temp_file)


def test_load_employee_data_invalid_format():
    """Тест загрузки данных из файла с неверным форматом."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['wrong', 'headers'])
        writer.writerow(['data1', 'data2'])
        temp_file = f.name
    
    try:
        # Ожидаем любое сообщение об ошибке ValueError
        with pytest.raises(ValueError):
            load_employee_data(temp_file)
    finally:
        import os
        os.unlink(temp_file)


def test_load_employee_data_empty_file():
    """Тест загрузки данных из пустого файла."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        writer = csv.writer(f)
        writer.writerow(['name', 'position', 'completed_tasks', 
                        'performance', 'skills', 'team', 'experience_years'])
        temp_file = f.name
    
    try:
        employees = load_employee_data(temp_file)
        assert len(employees) == 0
    finally:
        import os
        os.unlink(temp_file)
