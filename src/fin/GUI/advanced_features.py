"""
Дополнительные функции для приложения управления финансами
"""

import sys
import os
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QDateEdit, QComboBox, QFormLayout, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox, QTabWidget,
    QWidget, QProgressBar, QFrame, QGridLayout
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QPainter, QPen, QColor
import sqlite3
from datetime import datetime, timedelta

# Добавляем путь к модулям БД
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
from database import get_all_category
from DB_payment import get_total_statistics, get_statistics_by_date_range


class ChartWidget(QWidget):
    """Виджет для отображения графика"""
    
    def __init__(self, chart_data=None, parent=None):
        super().__init__(parent)
        self.chart_data = chart_data or []
        self.setMinimumSize(600, 300)
        self.setStyleSheet("background: white; border: 1px solid #ddd; border-radius: 8px;")
    
    def set_data(self, chart_data):
        self.chart_data = chart_data
        self.update()
    
    def paintEvent(self, event):
        if not self.chart_data:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Размеры виджета
        width = self.width()
        height = self.height()
        margin = 60
        
        # Область для графика
        chart_width = width - 2 * margin
        chart_height = height - 2 * margin
        
        # Находим максимальные значения
        max_income = max([row[1] for row in self.chart_data]) if self.chart_data else 1
        max_expense = max([row[2] for row in self.chart_data]) if self.chart_data else 1
        max_value = max(max_income, max_expense, 1)
        
        # Рисуем оси
        painter.setPen(QPen(QColor("#333"), 2))
        painter.drawLine(margin, height - margin, width - margin, height - margin)  # X ось
        painter.drawLine(margin, margin, margin, height - margin)  # Y ось
        
        # Рисуем сетку
        painter.setPen(QPen(QColor("#e9ecef"), 1))
        for i in range(1, 10):
            y = margin + (chart_height * i) // 10
            painter.drawLine(margin, y, width - margin, y)
        
        # Подписи осей Y (суммы) - делаем более видимыми
        painter.setPen(QColor("#495057"))
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        for i in range(0, 11, 2):
            y = margin + (chart_height * i) // 10
            value = max_value * (10 - i) // 10
            painter.drawText(5, y + 3, f"{value:.0f}")
        
        # Рисуем данные
        if len(self.chart_data) > 1:
            # Линия доходов
            painter.setPen(QPen(QColor("#28a745"), 3))
            for i in range(len(self.chart_data) - 1):
                x1 = margin + (chart_width * i) // (len(self.chart_data) - 1)
                y1 = height - margin - (chart_height * self.chart_data[i][1]) // max_value
                x2 = margin + (chart_width * (i + 1)) // (len(self.chart_data) - 1)
                y2 = height - margin - (chart_height * self.chart_data[i + 1][1]) // max_value
                painter.drawLine(x1, y1, x2, y2)
            
            # Линия расходов
            painter.setPen(QPen(QColor("#dc3545"), 3))
            for i in range(len(self.chart_data) - 1):
                x1 = margin + (chart_width * i) // (len(self.chart_data) - 1)
                y1 = height - margin - (chart_height * self.chart_data[i][2]) // max_value
                x2 = margin + (chart_width * (i + 1)) // (len(self.chart_data) - 1)
                y2 = height - margin - (chart_height * self.chart_data[i + 1][2]) // max_value
                painter.drawLine(x1, y1, x2, y2)
            
            # Точки на графике
            painter.setPen(QPen(QColor("#28a745"), 6))
            for i, (date, income, expense) in enumerate(self.chart_data):
                x = margin + (chart_width * i) // (len(self.chart_data) - 1)
                if income > 0:
                    y = height - margin - (chart_height * income) // max_value
                    painter.drawEllipse(x - 3, y - 3, 6, 6)
            
            painter.setPen(QPen(QColor("#dc3545"), 6))
            for i, (date, income, expense) in enumerate(self.chart_data):
                x = margin + (chart_width * i) // (len(self.chart_data) - 1)
                if expense > 0:
                    y = height - margin - (chart_height * expense) // max_value
                    painter.drawEllipse(x - 3, y - 3, 6, 6)
        
        # Подписи осей
        painter.setPen(QColor("#495057"))
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        painter.drawText(10, height // 2, "Сумма (₽)")
        painter.drawText(width // 2, height - 10, "Дата")
        
        # Подписи дат на оси X - делаем более видимыми
        if self.chart_data:
            painter.setPen(QColor("#495057"))
            painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            for i, (date, income, expense) in enumerate(self.chart_data):
                if i % max(1, len(self.chart_data) // 6) == 0:  # Показываем каждую 6-ю дату
                    x = margin + (chart_width * i) // (len(self.chart_data) - 1)
                    # Форматируем дату
                    try:
                        date_obj = datetime.strptime(date, "%Y-%m-%d")
                        date_str = date_obj.strftime("%d.%m")
                    except:
                        date_str = date
                    painter.drawText(x - 15, height - margin + 20, date_str)
        
        # Легенда
        legend_y = 20
        painter.setPen(QPen(QColor("#28a745"), 3))
        painter.drawLine(10, legend_y, 30, legend_y)
        painter.drawText(35, legend_y + 5, "Доходы")
        
        painter.setPen(QPen(QColor("#dc3545"), 3))
        painter.drawLine(100, legend_y, 120, legend_y)
        painter.drawText(125, legend_y + 5, "Расходы")


class SearchDialog(QDialog):
    """Диалог для поиска платежей"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Поиск платежей")
        self.setModal(True)
        self.setFixedSize(500, 400)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Форма поиска
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введите название платежа")
        form_layout.addRow("Название:", self.name_edit)
        
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        form_layout.addRow("Дата от:", self.date_from)
        
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        form_layout.addRow("Дата до:", self.date_to)
        
        self.amount_from = QLineEdit()
        self.amount_from.setPlaceholderText("0")
        form_layout.addRow("Сумма от:", self.amount_from)
        
        self.amount_to = QLineEdit()
        self.amount_to.setPlaceholderText("999999")
        form_layout.addRow("Сумма до:", self.amount_to)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Все", "income", "expense"])
        form_layout.addRow("Тип:", self.type_combo)
        
        self.category_combo = QComboBox()
        self.category_combo.addItem("Все категории")
        categories = get_all_category()
        for _, category_name in categories:
            self.category_combo.addItem(category_name)
        form_layout.addRow("Категория:", self.category_combo)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.search_button = QPushButton("Поиск")
        self.search_button.clicked.connect(self.search_payments)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # Таблица результатов
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Название", "Дата", "Сумма", "Тип", "Категория"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.results_table)
        
        self.setLayout(layout)
    
    def search_payments(self):
        """Выполнение поиска платежей"""
        # Здесь должна быть логика поиска
        # Пока просто показываем сообщение
        QMessageBox.information(self, "Поиск", "Функция поиска будет реализована в следующей версии!")


class ExportDialog(QDialog):
    """Диалог для экспорта данных"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Экспорт данных")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Параметры экспорта
        form_layout = QFormLayout()
        
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        form_layout.addRow("Дата от:", self.date_from)
        
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        form_layout.addRow("Дата до:", self.date_to)
        
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Excel", "JSON"])
        form_layout.addRow("Формат:", self.format_combo)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.export_button = QPushButton("Экспорт")
        self.export_button.clicked.connect(self.export_data)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def export_data(self):
        """Экспорт данных"""
        QMessageBox.information(self, "Экспорт", "Функция экспорта будет реализована в следующей версии!")


class BudgetDialog(QDialog):
    """Диалог для установки бюджета"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Установка бюджета")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Форма бюджета
        form_layout = QFormLayout()
        
        self.category_combo = QComboBox()
        categories = get_all_category()
        for _, category_name in categories:
            self.category_combo.addItem(category_name)
        form_layout.addRow("Категория:", self.category_combo)
        
        self.amount_edit = QLineEdit()
        self.amount_edit.setPlaceholderText("Введите сумму бюджета")
        form_layout.addRow("Сумма:", self.amount_edit)
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Месяц", "Неделя", "Год"])
        form_layout.addRow("Период:", self.period_combo)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.save_button.clicked.connect(self.save_budget)
        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def save_budget(self):
        """Сохранение бюджета"""
        QMessageBox.information(self, "Бюджет", "Функция бюджета будет реализована в следующей версии!")


class ReportsDialog(QDialog):
    """Диалог для просмотра отчетов"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Отчеты и аналитика")
        self.setModal(True)
        self.setFixedSize(900, 700)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Вкладки
        self.tab_widget = QTabWidget()
        
        # Вкладка общей статистики
        stats_tab = QWidget()
        stats_layout = QVBoxLayout(stats_tab)
        
        # Общая статистика
        try:
            stats = get_total_statistics()
            
            # Проверяем, что данные получены корректно
            income = stats.get('income', 0) or 0
            expense = stats.get('expense', 0) or 0
            balance = stats.get('balance', 0) or 0
            
            stats_info = QLabel(f"""
            <div style="padding: 20px; background: #f8f9fa; border-radius: 8px; font-family: Arial;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">Общая статистика</h3>
                <p style="font-size: 16px; margin: 10px 0;"><b style="color: #28a745;">Общий доход:</b> <span style="font-size: 18px; font-weight: bold;">{income:.2f} ₽</span></p>
                <p style="font-size: 16px; margin: 10px 0;"><b style="color: #dc3545;">Общий расход:</b> <span style="font-size: 18px; font-weight: bold;">{expense:.2f} ₽</span></p>
                <p style="font-size: 16px; margin: 10px 0;"><b style="color: #007bff;">Баланс:</b> <span style="font-size: 18px; font-weight: bold; color: {'#28a745' if balance > 0 else '#dc3545' if balance < 0 else '#007bff'};">{balance:.2f} ₽</span></p>
            </div>
            """)
        except Exception as e:
            stats_info = QLabel(f"""
            <div style="padding: 20px; background: #f8f9fa; border-radius: 8px; font-family: Arial;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">Общая статистика</h3>
                <p style="color: #dc3545;">Ошибка при загрузке статистики: {e}</p>
                <p style="color: #666; font-size: 12px;">Попробуйте добавить несколько платежей и обновить отчет</p>
            </div>
            """)
        
        stats_layout.addWidget(stats_info)
        stats_layout.addStretch()
        
        self.tab_widget.addTab(stats_tab, "Общая статистика")
        
        # Вкладка аналитики по датам
        analytics_tab = QWidget()
        analytics_layout = QVBoxLayout(analytics_tab)
        
        # Выбор периода
        period_layout = QHBoxLayout()
        
        period_label = QLabel("Период анализа:")
        period_label.setStyleSheet("font-weight: bold;")
        
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addDays(-30))
        self.date_from.setCalendarPopup(True)
        
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        
        self.analyze_button = QPushButton("Анализировать")
        self.analyze_button.clicked.connect(self.analyze_period)
        
        period_layout.addWidget(period_label)
        period_layout.addWidget(self.date_from)
        period_layout.addWidget(QLabel("до"))
        period_layout.addWidget(self.date_to)
        period_layout.addWidget(self.analyze_button)
        period_layout.addStretch()
        
        analytics_layout.addLayout(period_layout)
        
        # Результаты анализа
        self.analytics_results = QLabel("Выберите период и нажмите 'Анализировать'")
        self.analytics_results.setStyleSheet("padding: 20px; background: #f8f9fa; border-radius: 8px;")
        analytics_layout.addWidget(self.analytics_results)
        
        # График
        self.chart_widget = ChartWidget()
        analytics_layout.addWidget(self.chart_widget)
        
        self.tab_widget.addTab(analytics_tab, "Аналитика по датам")
        
        layout.addWidget(self.tab_widget)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.close_button = QPushButton("Закрыть")
        self.close_button.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def analyze_period(self):
        """Анализ выбранного периода"""
        date_from = self.date_from.date().toString("yyyy-MM-dd")
        date_to = self.date_to.date().toString("yyyy-MM-dd")
        
        try:
            stats = get_statistics_by_date_range(date_from, date_to)
            
            # Проверяем, что данные получены корректно
            income = stats.get('income', 0) or 0
            expense = stats.get('expense', 0) or 0
            balance = stats.get('balance', 0) or 0
            chart_data = stats.get('chart_data', [])
            
            # Обновляем результаты
            self.analytics_results.setText(f"""
            <div style="padding: 20px; background: #f8f9fa; border-radius: 8px; font-family: Arial;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">Статистика за период {date_from} - {date_to}</h3>
                <p style="font-size: 16px; margin: 10px 0;"><b style="color: #28a745;">Доходы:</b> <span style="font-size: 18px; font-weight: bold;">{income:.2f} ₽</span></p>
                <p style="font-size: 16px; margin: 10px 0;"><b style="color: #dc3545;">Расходы:</b> <span style="font-size: 18px; font-weight: bold;">{expense:.2f} ₽</span></p>
                <p style="font-size: 16px; margin: 10px 0;"><b style="color: #007bff;">Баланс:</b> <span style="font-size: 18px; font-weight: bold; color: {'#28a745' if balance > 0 else '#dc3545' if balance < 0 else '#007bff'};">{balance:.2f} ₽</span></p>
                <p style="font-size: 14px; margin: 10px 0; color: #666;"><b>Количество дней с данными:</b> {len(chart_data)}</p>
            </div>
            """)
            
            # Обновляем график
            self.chart_widget.set_data(chart_data)
            
        except Exception as e:
            self.analytics_results.setText(f"""
            <div style="padding: 20px; background: #f8f9fa; border-radius: 8px; font-family: Arial;">
                <h3 style="color: #2c3e50; margin-bottom: 15px;">Ошибка анализа</h3>
                <p style="color: #dc3545;">Ошибка при анализе данных: {e}</p>
                <p style="color: #666; font-size: 12px;">Попробуйте выбрать другой период или добавить платежи</p>
            </div>
            """) 