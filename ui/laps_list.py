"""Список кругов секундомера."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget


class LapsList(QWidget):
    """Отображает длительность каждого круга и общее время."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.title = QLabel("LAPS")
        self.title.setObjectName("sectionTitle")

        self.content = QWidget()
        self.rows_layout = QVBoxLayout(self.content)
        self.rows_layout.setContentsMargins(0, 0, 0, 0)
        self.rows_layout.setSpacing(5)
        self.rows_layout.addStretch()

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.content)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.title)
        layout.addWidget(self.scroll)

    def set_laps(self, laps, formatter):
        # Список кругов меняется только при добавлении или сбросе круга.
        # Не пересоздаём десятки виджетов на каждом тике секундомера.
        signature = tuple(
            (lap["number"], lap["duration"], lap["total"]) for lap in laps
        )
        if signature == getattr(self, "_laps_signature", None):
            return
        self._laps_signature = signature

        while self.rows_layout.count() > 1:
            item = self.rows_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for lap in laps:
            row = QWidget()
            row_layout = QVBoxLayout(row)
            row_layout.setContentsMargins(10, 7, 10, 7)
            row_layout.setSpacing(2)

            top = QLabel(
                f"Lap {lap['number']}  ·  {formatter(lap['duration'])}"
            )
            top.setObjectName("lapName")
            bottom = QLabel(f"Total  {formatter(lap['total'])}")
            bottom.setObjectName("lapTotal")
            row_layout.addWidget(top)
            row_layout.addWidget(bottom)
            row.setObjectName("lapRow")
            self.rows_layout.insertWidget(self.rows_layout.count() - 1, row)

        if not laps:
            empty = QLabel("No laps yet")
            empty.setObjectName("emptyHint")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.rows_layout.insertWidget(0, empty)
