"""Набор круглых кнопок управления."""

from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget


class ControlButtons(QWidget):
    """Показывает иконки управления в едином стиле."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.buttons = {}
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(18)

        definitions = [
            ("reset", "↺", "Reset"),
            ("start", "▶", "Start"),
            ("pause", "Ⅱ", "Pause"),
            ("resume", "▶", "Resume"),
            ("stop", "■", "Stop"),
            ("lap", "⚑", "Lap"),
        ]
        for key, symbol, tooltip in definitions:
            button = QPushButton(symbol)
            button.setObjectName(
                "primaryControl" if key == "start" else "controlButton"
            )
            button.setToolTip(tooltip)
            button.setFixedSize(52, 52)
            button.setVisible(False)
            self.buttons[key] = button
            layout.addWidget(button)

        layout.addStretch()

    def button(self, name):
        return self.buttons[name]

    def show_buttons(self, *names):
        for name, button in self.buttons.items():
            button.setVisible(name in names)
