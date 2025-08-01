# Приложение управления финансами

Современное приложение для управления личными финансами с красивым пользовательским интерфейсом.

## Возможности

- **Управление категориями**: добавление, удаление категорий расходов и доходов
- **Управление платежами**: добавление, удаление платежей с указанием суммы, даты и типа
- **Статистика в реальном времени**: отображение общих доходов, расходов и баланса
- **Современный интерфейс**: красивый и интуитивно понятный UI на PySide6
- **База данных SQLite**: надежное хранение данных
- **Дополнительные функции**: поиск, отчеты, экспорт данных, управление бюджетом

## Установка

1. Убедитесь, что у вас установлен Python 3.13
2. Установите зависимости с помощью Poetry:

```bash
poetry install
```

3. Инициализируйте базу данных:

```bash
python init_database.py
```

## Запуск приложения

### Способ 1: Из корневой директории
```bash
python run_app.py
```

### Способ 2: Из директории GUI
```bash
cd src/fin/GUI
python main.py
```

### Способ 3: С помощью Poetry
```bash
poetry run python run_app.py
```

## Использование

### Главная страница
- Отображает статистику: общий доход, расход и баланс
- Список всех категорий
- Кнопки управления категориями: "Добавить категорию", "Удалить категорию"
- Дополнительные функции: "Поиск", "Отчеты", "Экспорт", "Бюджет"
- Двойной клик по категории открывает её для просмотра платежей

### Просмотр категории
- Отображает все платежи выбранной категории
- Кнопка "Добавить платеж" для создания новых платежей
- Кнопка "Назад" для возврата к главной странице
- Платежи отображаются с цветовой индикацией (зеленый - доход, красный - расход)
- Кнопка удаления для каждого платежа

### Добавление платежа
- Название платежа
- Дата (с календарем)
- Сумма (с поддержкой копеек)
- Тип платежа (доход/расход)

### Дополнительные функции
- **Поиск**: поиск платежей по различным критериям
- **Отчеты**: просмотр статистики и графиков
- **Экспорт**: экспорт данных в различных форматах
- **Бюджет**: установка и отслеживание бюджета по категориям

## Структура проекта

```
fin/
├── src/fin/
│   ├── db/                    # Модули базы данных
│   │   ├── database.py        # Функции для работы с категориями
│   │   ├── DB_payment.py      # Функции для работы с платежами
│   │   ├── init_db.py         # Инициализация базы данных
│   │   └── finance.db         # База данных SQLite
│   └── GUI/                   # Пользовательский интерфейс
│       ├── main_window.py     # Главное окно приложения
│       ├── advanced_features.py # Дополнительные функции
│       └── main.py            # Точка входа
├── run_app.py                 # Скрипт запуска
├── init_database.py           # Скрипт инициализации БД
└── pyproject.toml             # Конфигурация Poetry
```

## Технологии

- **Python 3.13** - основной язык программирования
- **PySide6** - современный Qt фреймворк для GUI
- **SQLite** - встроенная база данных
- **Poetry** - управление зависимостями

## Разработка

Для разработки используйте Poetry:

```bash
# Активация виртуального окружения
poetry shell

# Добавление новой зависимости
poetry add package_name

# Запуск в режиме разработки
poetry run python run_app.py
```

## Планы развития

- [ ] Реализация функции поиска платежей
- [ ] Добавление графиков и диаграмм
- [ ] Экспорт данных в Excel и CSV
- [ ] Система уведомлений о превышении бюджета
- [ ] Мобильная версия приложения
- [ ] Синхронизация с облачными сервисами
