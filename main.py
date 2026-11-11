"""Точка входа приложения PPLAB3VAR13."""

import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from app.main_window import MainWindow


def main():
    """Создать приложение и показать главное окно."""
    app = QApplication(sys.argv)
    app.setApplicationName("PPLAB3VAR13")

    # Путь к таблице стилей относительно корня проекта.
    style_path = Path(__file__).parent / "resources" / "styles" / "theme.qss"
    if style_path.exists():
        app.setStyleSheet(style_path.read_text(encoding="utf-8"))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
