import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel, QLineEdit,
    QDialog, QFormLayout, QMessageBox, QFrame, QScrollArea,
    QGridLayout, QDateEdit, QComboBox, QSpinBox, QDoubleSpinBox, QSizePolicy
)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont, QPalette, QColor
import sys
import os

# Добавляем путь к модулям БД
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
from database import add_category, del_category, get_all_category, get_category
from DB_payment import add_payment, del_payment, get_payment_by_category, get_total_statistics, get_statistics_by_date_range, get_category_statistics

# Импортируем дополнительные функции
try:
    from .advanced_features import SearchDialog, ExportDialog, BudgetDialog, ReportsDialog
except ImportError:
    # Если не удалось импортировать, создаем заглушки
    class SearchDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Поиск платежей")
            self.setModal(True)
            self.setFixedSize(400, 200)
            
            layout = QVBoxLayout()
            info_label = QLabel("🔍 Функция поиска платежей")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setStyleSheet("font-size: 16px; color: #666; padding: 20px;")
            
            desc_label = QLabel("Будет добавлена в следующей версии приложения")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setStyleSheet("color: #999; padding: 10px;")
            
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(self.accept)
            
            layout.addWidget(info_label)
            layout.addWidget(desc_label)
            layout.addWidget(ok_button)
            
            self.setLayout(layout)
    
    class ExportDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Экспорт данных")
            self.setModal(True)
            self.setFixedSize(400, 200)
            
            layout = QVBoxLayout()
            info_label = QLabel("📤 Функция экспорта данных")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setStyleSheet("font-size: 16px; color: #666; padding: 20px;")
            
            desc_label = QLabel("Будет добавлена в следующей версии приложения")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setStyleSheet("color: #999; padding: 10px;")
            
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(self.accept)
            
            layout.addWidget(info_label)
            layout.addWidget(desc_label)
            layout.addWidget(ok_button)
            
            self.setLayout(layout)
    
    class BudgetDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Управление бюджетом")
            self.setModal(True)
            self.setFixedSize(400, 200)
            
            layout = QVBoxLayout()
            info_label = QLabel("💰 Функция управления бюджетом")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setStyleSheet("font-size: 16px; color: #666; padding: 20px;")
            
            desc_label = QLabel("Будет добавлена в следующей версии приложения")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setStyleSheet("color: #999; padding: 10px;")
            
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(self.accept)
            
            layout.addWidget(info_label)
            layout.addWidget(desc_label)
            layout.addWidget(ok_button)
            
            self.setLayout(layout)
    
    class ReportsDialog(QDialog):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Отчеты и аналитика")
            self.setModal(True)
            self.setFixedSize(400, 200)
            
            layout = QVBoxLayout()
            info_label = QLabel("📊 Функция отчетов и аналитики")
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setStyleSheet("font-size: 16px; color: #666; padding: 20px;")
            
            desc_label = QLabel("Будет добавлена в следующей версии приложения")
            desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            desc_label.setStyleSheet("color: #999; padding: 10px;")
            
            ok_button = QPushButton("OK")
            ok_button.clicked.connect(self.accept)
            
            layout.addWidget(info_label)
            layout.addWidget(desc_label)
            layout.addWidget(ok_button)
            
            self.setLayout(layout)


class CategoryDialog(QDialog):
    """Диалог для добавления новой категории"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить категорию")
        self.setModal(True)
        self.setFixedSize(350, 180)
        
        layout = QVBoxLayout()
        
        # Форма
        form_layout = QFormLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введите название категории")
        self.name_edit.setMinimumHeight(35)
        self.name_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background: white;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("Название:", self.name_edit)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Добавить")
        self.cancel_button = QPushButton("Отмена")
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)


class PaymentDialog(QDialog):
    """Диалог для добавления нового платежа"""
    
    def __init__(self, category_id, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setWindowTitle("Добавить платеж")
        self.setModal(True)
        self.setFixedSize(450, 350)
        
        layout = QVBoxLayout()
        
        # Форма
        form_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Введите название платежа")
        self.name_edit.setMinimumHeight(35)
        self.name_edit.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background: white;
                color: #333;
            }
            QLineEdit:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("Название:", self.name_edit)
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumHeight(35)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background: white;
                color: #333;
            }
            QDateEdit:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("Дата:", self.date_edit)
        
        self.amount_edit = QDoubleSpinBox()
        self.amount_edit.setRange(0, 999999.99)
        self.amount_edit.setDecimals(2)
        self.amount_edit.setSuffix(" ₽")
        self.amount_edit.setMinimumHeight(35)
        self.amount_edit.setStyleSheet("""
            QDoubleSpinBox {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background: white;
                color: #333;
            }
            QDoubleSpinBox:focus {
                border-color: #007bff;
            }
        """)
        form_layout.addRow("Сумма:", self.amount_edit)
        
        self.type_combo = QComboBox()
        self.type_combo.addItems(["expense", "income"])
        self.type_combo.setMinimumHeight(35)
        self.type_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                font-size: 14px;
                border: 2px solid #ddd;
                border-radius: 5px;
                background: white;
                color: #333;
            }
            QComboBox:focus {
                border-color: #007bff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
        """)
        form_layout.addRow("Тип:", self.type_combo)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Добавить")
        self.cancel_button = QPushButton("Отмена")
        
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)


class PaymentWidget(QWidget):
    """Виджет для отображения платежа"""
    
    def __init__(self, payment_data, parent=None):
        super().__init__(parent)
        self.payment_data = payment_data
        self.parent_widget = parent
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        
        # Основная информация
        info_layout = QVBoxLayout()
        
        name_label = QLabel(self.payment_data[1])  # name (теперь индекс 1)
        name_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        
        date_label = QLabel(f"Дата: {self.payment_data[2]}")  # date (теперь индекс 2)
        date_label.setStyleSheet("color: #666; font-size: 11px;")
        
        info_layout.addWidget(name_label)
        info_layout.addWidget(date_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Сумма и тип
        amount_layout = QVBoxLayout()
        
        amount = self.payment_data[3]  # amount (теперь индекс 3)
        payment_type = self.payment_data[4]  # type (теперь индекс 4)
        
        amount_label = QLabel(f"{amount:.2f} ₽")
        amount_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        if payment_type == "income":
            amount_label.setStyleSheet("color: #28a745;")
            type_label = QLabel("Доход")
            type_label.setStyleSheet("color: #28a745; background: #d4edda; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;")
        else:
            amount_label.setStyleSheet("color: #dc3545;")
            type_label = QLabel("Расход")
            type_label.setStyleSheet("color: #dc3545; background: #f8d7da; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;")
        
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(type_label)
        
        layout.addLayout(amount_layout)
        
        # Кнопка удаления
        delete_button = QPushButton("🗑")
        delete_button.setFixedSize(30, 30)
        delete_button.setStyleSheet("""
            QPushButton {
                background: #dc3545;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #c82333;
            }
        """)
        delete_button.clicked.connect(self.delete_payment)
        
        layout.addWidget(delete_button)
        
        self.setLayout(layout)
        
        # Стили
        self.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 3px;
                padding: 5px;
            }
            QWidget:hover {
                border: 1px solid #007bff;
                background: #f8f9fa;
            }
        """)
    
    def delete_payment(self):
        """Удаление платежа"""
        payment_id = self.payment_data[0]  # ID платежа
        payment_name = self.payment_data[1]  # Название платежа
        
        # Создаем кастомный диалог подтверждения
        confirm_dialog = QDialog(self)
        confirm_dialog.setWindowTitle("Подтверждение удаления")
        confirm_dialog.setModal(True)
        confirm_dialog.setFixedSize(400, 150)
        confirm_dialog.setStyleSheet("""
            QDialog {
                background: white;
            }
            QLabel {
                color: #333;
                font-size: 14px;
            }
            QPushButton {
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
                border: none;
                min-width: 80px;
            }
            QPushButton#delete {
                background: #dc3545;
                color: white;
            }
            QPushButton#delete:hover {
                background: #c82333;
            }
            QPushButton#cancel {
                background: #6c757d;
                color: white;
            }
            QPushButton#cancel:hover {
                background: #5a6268;
            }
        """)
        
        layout = QVBoxLayout(confirm_dialog)
        
        # Текст подтверждения
        message_label = QLabel(f"Вы уверены, что хотите удалить платеж:")
        message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        payment_label = QLabel(f"«{payment_name}»")
        payment_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        payment_label.setStyleSheet("font-weight: bold; color: #dc3545; font-size: 16px;")
        
        layout.addWidget(message_label)
        layout.addWidget(payment_label)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_button = QPushButton("Отмена")
        cancel_button.setObjectName("cancel")
        cancel_button.clicked.connect(confirm_dialog.reject)
        
        delete_button = QPushButton("Удалить")
        delete_button.setObjectName("delete")
        delete_button.clicked.connect(confirm_dialog.accept)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(delete_button)
        
        layout.addLayout(button_layout)
        
        if confirm_dialog.exec() == QDialog.DialogCode.Accepted:
            del_payment(payment_id)
            if hasattr(self.parent_widget, 'load_payments'):
                self.parent_widget.load_payments()
            
            # Обновляем статистику на главной странице
            main_window = self.parent_widget.parent()
            if hasattr(main_window, 'update_statistics'):
                main_window.update_statistics()


class CategoryViewWidget(QWidget):
    """Виджет для отображения платежей категории"""
    
    def __init__(self, category_id, category_name, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.category_name = category_name
        self.setup_ui()
        self.load_payments()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        header_layout = QHBoxLayout()
        
        title_label = QLabel(f"Категория: {self.category_name}")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        
        back_button = QPushButton("← Назад")
        back_button.clicked.connect(self.go_back)
        
        add_payment_button = QPushButton("+ Добавить платеж")
        add_payment_button.clicked.connect(self.add_payment)
        
        header_layout.addWidget(back_button)
        header_layout.addStretch()
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(add_payment_button)
        
        layout.addLayout(header_layout)
        
        # Список платежей
        self.payments_list = QListWidget()
        self.payments_list.setSpacing(5)
        layout.addWidget(self.payments_list)
        
        self.setLayout(layout)
    
    def load_payments(self):
        self.payments_list.clear()
        payments = get_payment_by_category(self.category_id)
        
        if not payments:
            no_payments_label = QLabel("Платежей в этой категории пока нет")
            no_payments_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_payments_label.setStyleSheet("color: #666; padding: 20px; font-size: 14px;")
            self.payments_list.addItem("")
            self.payments_list.setItemWidget(self.payments_list.item(0), no_payments_label)
        else:
            total_income = 0
            total_expense = 0
            
            for payment in payments:
                payment_widget = PaymentWidget(payment, self)
                item = QListWidgetItem()
                item.setSizeHint(payment_widget.sizeHint())
                self.payments_list.addItem(item)
                self.payments_list.setItemWidget(item, payment_widget)
                
                # Подсчитываем общие суммы
                amount = payment[3]  # amount
                payment_type = payment[4]  # type
                if payment_type == "income":
                    total_income += amount
                else:
                    total_expense += amount
            
            # Добавляем суммарную статистику внизу
            self.add_summary_widget(total_income, total_expense)
    
    def add_summary_widget(self, total_income, total_expense):
        """Добавляет виджет с суммарной статистикой"""
        summary_widget = QWidget()
        summary_widget.setStyleSheet("""
            QWidget {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                margin: 10px;
                padding: 15px;
            }
        """)
        
        summary_layout = QHBoxLayout(summary_widget)
        
        # Заголовок
        title_label = QLabel("Итого по категории:")
        title_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #495057;")
        
        summary_layout.addWidget(title_label)
        summary_layout.addStretch()
        
        # Доходы
        if total_income > 0:
            income_label = QLabel(f"Доходы: +{total_income:.2f} ₽")
            income_label.setStyleSheet("color: #28a745; font-weight: bold; font-size: 14px; margin-right: 20px;")
            summary_layout.addWidget(income_label)
        
        # Расходы
        if total_expense > 0:
            expense_label = QLabel(f"Расходы: -{total_expense:.2f} ₽")
            expense_label.setStyleSheet("color: #dc3545; font-weight: bold; font-size: 14px;")
            summary_layout.addWidget(expense_label)
        
        # Баланс
        balance = total_income - total_expense
        if balance != 0:
            balance_color = "#28a745" if balance > 0 else "#dc3545"
            balance_sign = "+" if balance > 0 else ""
            balance_label = QLabel(f"Баланс: {balance_sign}{balance:.2f} ₽")
            balance_label.setStyleSheet(f"color: {balance_color}; font-weight: bold; font-size: 14px; margin-left: 20px;")
            summary_layout.addWidget(balance_label)
        
        # Добавляем в список
        item = QListWidgetItem()
        item.setSizeHint(summary_widget.sizeHint())
        self.payments_list.addItem(item)
        self.payments_list.setItemWidget(item, summary_widget)
    
    def add_payment(self):
        dialog = PaymentDialog(self.category_id, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.name_edit.text()
            date = dialog.date_edit.date().toString("yyyy-MM-dd")
            amount = dialog.amount_edit.value()
            payment_type = dialog.type_combo.currentText()
            
            add_payment(name, date, amount, payment_type, self.category_id)
            self.load_payments()
            
            # Обновляем статистику на главной странице
            if hasattr(self.parent(), 'update_statistics'):
                self.parent().update_statistics()
    
    def go_back(self):
        """Возврат к главному виду"""
        # Ищем главное окно в иерархии родителей
        parent = self.parent()
        while parent and not hasattr(parent, 'show_main_view'):
            parent = parent.parent()
        
        if parent and hasattr(parent, 'show_main_view'):
            parent.show_main_view()


class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление финансами")
        self.setMinimumSize(800, 600)
        self.setup_ui()
        self.load_categories()
        self.apply_styles()
    
    def setup_ui(self):
        # Центральный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Главный layout
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Создаем виджеты
        self.create_main_view()
        self.create_category_view()
        
        # Показываем главный виджет
        self.show_main_view()
    
    def create_main_view(self):
        """Создание главного вида"""
        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)
        
        # Заголовок
        title_label = QLabel("Управление финансами")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 20px;")
        
        layout.addWidget(title_label)
        
        # Статистика
        self.stats_widget = QWidget()
        self.stats_widget.setStyleSheet("""
            QWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
            }
        """)
        stats_layout = QHBoxLayout(self.stats_widget)
        
        # Доходы
        income_layout = QVBoxLayout()
        income_title = QLabel("Общий доход")
        income_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        income_title.setStyleSheet("color: #666; font-size: 12px;")
        
        self.income_label = QLabel("0.00 ₽")
        self.income_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.income_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.income_label.setStyleSheet("color: #28a745;")
        
        income_layout.addWidget(income_title)
        income_layout.addWidget(self.income_label)
        
        # Расходы
        expense_layout = QVBoxLayout()
        expense_title = QLabel("Общий расход")
        expense_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        expense_title.setStyleSheet("color: #666; font-size: 12px;")
        
        self.expense_label = QLabel("0.00 ₽")
        self.expense_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.expense_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.expense_label.setStyleSheet("color: #dc3545;")
        
        expense_layout.addWidget(expense_title)
        expense_layout.addWidget(self.expense_label)
        
        # Баланс
        balance_layout = QVBoxLayout()
        balance_title = QLabel("Баланс")
        balance_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        balance_title.setStyleSheet("color: #666; font-size: 12px;")
        
        self.balance_label = QLabel("0.00 ₽")
        self.balance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.balance_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.balance_label.setStyleSheet("color: #007bff;")
        
        balance_layout.addWidget(balance_title)
        balance_layout.addWidget(self.balance_label)
        
        stats_layout.addLayout(income_layout)
        stats_layout.addLayout(expense_layout)
        stats_layout.addLayout(balance_layout)
        
        layout.addWidget(self.stats_widget)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        self.add_category_button = QPushButton("+ Добавить категорию")
        self.add_category_button.clicked.connect(self.add_category)
        
        self.delete_category_button = QPushButton("🗑 Удалить категорию")
        self.delete_category_button.clicked.connect(self.delete_category)
        
        button_layout.addWidget(self.add_category_button)
        button_layout.addWidget(self.delete_category_button)
        button_layout.addStretch()
        
        # Дополнительные функции
        self.search_button = QPushButton("🔍 Поиск")
        self.search_button.clicked.connect(self.show_search)
        
        self.reports_button = QPushButton("📊 Отчеты")
        self.reports_button.clicked.connect(self.show_reports)
        
        self.export_button = QPushButton("📤 Экспорт")
        self.export_button.clicked.connect(self.show_export)
        
        self.budget_button = QPushButton("💰 Бюджет")
        self.budget_button.clicked.connect(self.show_budget)
        
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.reports_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.budget_button)
        
        layout.addLayout(button_layout)
        
        # Список категорий
        self.categories_list = QListWidget()
        self.categories_list.itemDoubleClicked.connect(self.open_category)
        layout.addWidget(self.categories_list)
        
        self.main_layout.addWidget(self.main_widget)
    
    def create_category_view(self):
        """Создание вида категории"""
        self.category_widget = None  # Будет создан при открытии категории
    
    def apply_styles(self):
        """Применение стилей"""
        self.setStyleSheet("""
            QMainWindow {
                background: #f8f9fa;
            }
            QPushButton {
                background: #007bff;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #0056b3;
            }
            QPushButton:pressed {
                background: #004085;
            }
            QListWidget {
                background: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 10px;
            }
            QListWidget::item {
                background: transparent;
                border: none;
                padding: 5px;
            }
            QListWidget::item:selected {
                background: #e3f2fd;
                border-radius: 5px;
            }
        """)
    
    def load_categories(self):
        """Загрузка категорий из БД"""
        self.categories_list.clear()
        categories = get_all_category()
        
        for category_id, category_name in categories:
            # Получаем статистику для категории
            category_stats = self.get_category_statistics(category_id)
            
            # Создаем виджет для отображения категории
            category_widget = QWidget()
            category_layout = QHBoxLayout(category_widget)
            category_layout.setContentsMargins(15, 10, 15, 10)
            category_widget.setMinimumHeight(48)
            
            # Название категории
            name_label = QLabel(category_name)
            name_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
            name_label.setStyleSheet("color: #2c3e50;")
            name_label.setWordWrap(True)
            name_label.setMinimumHeight(32)
            name_label.setMaximumHeight(48)
            name_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
            name_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            
            category_layout.addWidget(name_label)
            category_layout.addStretch()
            
            # Статистика категории
            if category_stats['income'] > 0:
                income_label = QLabel(f"+{category_stats['income']:.0f} ₽")
                income_label.setStyleSheet("color: #28a745; font-weight: bold; font-size: 14px;")
                category_layout.addWidget(income_label)
            if category_stats['expense'] > 0:
                expense_label = QLabel(f"-{category_stats['expense']:.0f} ₽")
                expense_label.setStyleSheet("color: #dc3545; font-weight: bold; font-size: 14px;")
                category_layout.addWidget(expense_label)
            
            # Создаем элемент списка
            item = QListWidgetItem()
            item.setData(Qt.ItemDataRole.UserRole, category_id)
            item.setData(Qt.ItemDataRole.DisplayRole, category_name)
            item.setSizeHint(category_widget.sizeHint())
            self.categories_list.addItem(item)
            self.categories_list.setItemWidget(item, category_widget)
        
        # Обновляем статистику
        self.update_statistics()
    
    def get_category_statistics(self, category_id):
        """Получить статистику для конкретной категории"""
        try:
            stats = get_category_statistics(category_id)
            return stats
        except:
            return {'income': 0, 'expense': 0}
    
    def update_statistics(self):
        """Обновление статистики"""
        stats = get_total_statistics()
        
        self.income_label.setText(f"{stats['income']:.2f} ₽")
        self.expense_label.setText(f"{stats['expense']:.2f} ₽")
        self.balance_label.setText(f"{stats['balance']:.2f} ₽")
        
        # Изменяем цвет баланса в зависимости от значения
        if stats['balance'] > 0:
            self.balance_label.setStyleSheet("color: #28a745;")
        elif stats['balance'] < 0:
            self.balance_label.setStyleSheet("color: #dc3545;")
        else:
            self.balance_label.setStyleSheet("color: #007bff;")
    
    def add_category(self):
        """Добавление новой категории"""
        dialog = CategoryDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            name = dialog.name_edit.text().strip()
            if name:
                add_category(name)
                self.load_categories()
            else:
                QMessageBox.warning(self, "Ошибка", "Название категории не может быть пустым!")
    
    def delete_category(self):
        """Удаление категории"""
        current_item = self.categories_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления!")
            return
        
        # Имя категории теперь берём из item.data(Qt.DisplayRole)
        category_name = current_item.data(Qt.ItemDataRole.DisplayRole)
        if not category_name:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить имя категории!")
            return
        reply = QMessageBox.question(
            self, 
            "Подтверждение", 
            f"Вы уверены, что хотите удалить категорию '{category_name}' и все её платежи?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            del_category(category_name)
            self.load_categories()
    
    def open_category(self, item):
        """Открытие категории для просмотра платежей"""
        category_id = item.data(Qt.ItemDataRole.UserRole)
        category_name = item.text()
        
        # Создаем виджет категории
        self.category_widget = CategoryViewWidget(category_id, category_name, self)
        self.main_layout.addWidget(self.category_widget)
        
        # Скрываем главный вид
        self.main_widget.hide()
        self.category_widget.show()
    
    def show_main_view(self):
        """Показать главный вид"""
        if self.category_widget:
            self.category_widget.hide()
            self.main_layout.removeWidget(self.category_widget)
            self.category_widget.deleteLater()
            self.category_widget = None
        
        self.main_widget.show()
    
    def show_search(self):
        """Показать диалог поиска"""
        dialog = SearchDialog(self)
        dialog.exec()
    
    def show_reports(self):
        """Показать диалог отчетов"""
        dialog = ReportsDialog(self)
        dialog.exec()
    
    def show_export(self):
        """Показать диалог экспорта"""
        dialog = ExportDialog(self)
        dialog.exec()
    
    def show_budget(self):
        """Показать диалог бюджета"""
        dialog = BudgetDialog(self)
        dialog.exec()


def main():
    app = QApplication(sys.argv)
    
    # Устанавливаем стиль приложения
    app.setStyle('Fusion')
    
    # Создаем и показываем главное окно
    window = MainWindow()
    window.show()
    
    # Запускаем приложение
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 