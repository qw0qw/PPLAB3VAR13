"""Виджет цифрового отображения времени."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class TimeDisplay(QWidget):
    """Цифровое время в отдельной контрастной карточке."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.value_label = QLabel("00:00:00")
        self.value_label.setObjectName("timeValue")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.caption_label = QLabel("MIN : SEC : 1/100 SEC")
        self.caption_label.setObjectName("timeCaption")
        self.caption_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(2)
        layout.addWidget(self.value_label)
        layout.addWidget(self.caption_label)
        self.setObjectName("timeCard")

    def set_time(self, value):
        self.value_label.setText(value)

    def set_caption(self, value):
        self.caption_label.setText(value)
