"""Модуль для генерации отчетов."""

from typing import List, Dict, Any
from dataclasses import dataclass
from collections import defaultdict
from tabulate import tabulate


@dataclass
class Report:
    """Базовый класс для отчетов."""
    data: List[Dict[str, Any]]
    columns: List[str]


class ReportGenerator:
    """Генератор отчетов."""
    
    def __init__(self):
        """Инициализация генератора отчетов."""
        self.report_handlers = {
            "performance": self._generate_performance_report
        }
    
    def generate_report(self, report_type: str, employees: List[Any]) -> Report:
        """
        Генерирует отчет указанного типа.
        
        Args:
            report_type: Тип отчета
            employees: Список сотрудников
            
        Returns:
            Объект Report
            
        Raises:
            ValueError: Если тип отчета не поддерживается
        """
        if report_type not in self.report_handlers:
            raise ValueError(f"Неизвестный тип отчета: {report_type}")
        
        handler = self.report_handlers[report_type]
        return handler(employees)
    
    def _generate_performance_report(self, employees: List[Any]) -> Report:
        """
        Генерирует отчет по эффективности.
        
        Args:
            employees: Список сотрудников
            
        Returns:
            Отчет по эффективности
        """
        # Группируем по должности
        position_data = defaultdict(list)
        for employee in employees:
            position_data[employee.position].append(employee.performance)
        
        # Рассчитываем среднюю эффективность
        report_data = []
        for position, performances in position_data.items():
            avg_performance = sum(performances) / len(performances)
            report_data.append({
                "position": position,
                "performance": round(avg_performance, 2)
            })
        
        # Сортируем по убыванию эффективности
        report_data.sort(key=lambda x: x["performance"], reverse=True)
        
        return Report(
            data=report_data,
            columns=["position", "performance"]
        )
    
    def print_report(self, report: Report, report_type: str):
        """
        Выводит отчет в консоль в виде таблицы.
        
        Args:
            report: Объект отчета
            report_type: Тип отчета (для заголовка)
        """
        if not report.data:
            print("Нет данных для отображения")
            return
        
        # Добавляем нумерацию строк
        table_data = []
        for i, row in enumerate(report.data, 1):
            table_row = [i]
            for column in report.columns:
                table_row.append(row[column])
            table_data.append(table_row)
        
        headers = ["#"] + report.columns
        
        print(f"Отчет: {report_type}")
        print(tabulate(table_data, headers=headers, tablefmt="simple"))
        print()
    
    def register_report_handler(self, report_type: str, handler):
        """
        Регистрирует новый обработчик отчета.
        
        Args:
            report_type: Тип отчета
            handler: Функция-обработчик
        """
        self.report_handlers[report_type] = handler