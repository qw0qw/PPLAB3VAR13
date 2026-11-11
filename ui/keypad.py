"""Экранная цифровая клавиатура таймера."""

from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget


class Keypad(QWidget):
    """Клавиатура с вводом справа налево."""

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(7)
        keys = [
            ("1", 0, 0), ("2", 0, 1), ("3", 0, 2),
            ("4", 1, 0), ("5", 1, 1), ("6", 1, 2),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2),
            ("⌫", 3, 0), ("0", 3, 1), ("C", 3, 2),
        ]
        self.buttons = {}
        for text, row, column in keys:
            button = QPushButton(text)
            button.setObjectName("keyButton")
            button.setMinimumHeight(34)
            self.buttons[text] = button
            layout.addWidget(button, row, column)

    def button(self, key):
        return self.buttons[key]