#!/usr/bin/env python3
"""
Скрипт для запуска приложения управления финансами
"""

import sys
import os

# Добавляем путь к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from fin.GUI.main_window import main

if __name__ == "__main__":
    main() 