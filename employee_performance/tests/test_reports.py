"""Тесты для модуля reports."""

"""Тесты для модуля reports."""

import pytest
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
    
    # Проверяем сортировку по убыванию эффективности
    assert report.data[0]["position"] == "Backend Developer"
    assert report.data[0]["performance"] == 4.85  # (4.8 + 4.9) / 2
    
    assert report.data[1]["position"] == "Frontend Developer"
    assert report.data[1]["performance"] == 4.6  # (4.7 + 4.5) / 2


def test_generate_report_unknown_type(report_generator, sample_employees):
    """Тест генерации отчета с неизвестным типом."""
    with pytest.raises(ValueError, match="Неизвестный тип отчета"):
        report_generator.generate_report("unknown", sample_employees)


def test_register_report_handler(report_generator):
    """Тест регистрации нового обработчика отчета."""
    
    def custom_report_handler(employees):
        return Report(data=[{"test": "data"}], columns=["test"])
    
    report_generator.register_report_handler("custom", custom_report_handler)
    
    # Проверяем, что новый обработчик работает
    report = report_generator.generate_report("custom", [])
    assert report.data[0]["test"] == "data"


def test_print_report_empty(capsys, report_generator):
    """Тест вывода пустого отчета."""
    empty_report = Report(data=[], columns=[])
    report_generator.print_report(empty_report, "test")
    
    captured = capsys.readouterr()
    assert "Нет данных для отображения" in captured.out


def test_print_report_with_data(capsys, report_generator):
    """Тест вывода отчета с данными."""
    report = Report(
        data=[
            {"position": "Backend", "performance": 4.8},
            {"position": "Frontend", "performance": 4.5}
        ],
        columns=["position", "performance"]
    )
    
    report_generator.print_report(report, "performance")
    captured = capsys.readouterr()
    
    assert "Отчет: performance" in captured.out
    assert "Backend" in captured.out
    assert "Frontend" in captured.out
    assert "4.8" in captured.out
    assert "4.5" in captured.out