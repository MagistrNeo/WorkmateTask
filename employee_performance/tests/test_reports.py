"""Тесты для модуля reports."""

import pytest
import sys
import os

# Добавьте родительскую директорию в путь поиска модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from reports import ReportGenerator, Report
from data_loader import Employee


@pytest.fixture
def sample_employees():
    """Фикстура с тестовыми данными сотрудников."""
    return [
        Employee("Alex", "Backend Developer", 45, 4.8, "Python", "Team A", 5),
        Employee("Maria", "Frontend Developer", 38, 4.7, "React", "Team B", 4),
        Employee("John", "Backend Developer", 40, 4.9, "Java", "Team A", 3),
        Employee("Anna", "Frontend Developer", 35, 4.5, "Vue", "Team B", 2),
    ]


@pytest.fixture
def report_generator():
    """Фикстура генератора отчетов."""
    return ReportGenerator()


def test_generate_performance_report(report_generator, sample_employees):
    """Тест генерации отчета по эффективности."""
    report = report_generator.generate_report("performance", sample_employees)
    
    assert isinstance(report, Report)
    assert len(report.data) == 2  # 2 уникальные должности
    
    assert report.data[0]["position"] == "Backend Developer"
    assert report.data[0]["performance"] == 4.85
    
    assert report.data[1]["position"] == "Frontend Developer"
    assert report.data[1]["performance"] == 4.6


def test_generate_report_unknown_type(report_generator, sample_employees):
    """Тест генерации отчета с неизвестным типом."""
    with pytest.raises(ValueError, match="Неизвестный тип отчета"):
        report_generator.generate_report("unknown", sample_employees)


def test_register_report_handler(report_generator):
    """Тест регистрации нового обработчика отчета."""
    
    def custom_report_handler(employees):
        return Report(data=[{"test": "data"}], columns=["test"])
    
    report_generator.register_report_handler("custom", custom_report_handler)
    
    report = report_generator.generate_report("custom", [])
    assert report.data[0]["test"] == "data"
