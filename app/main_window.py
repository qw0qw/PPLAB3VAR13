"""Главное окно приложения."""

from PySide6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.app_controller import AppController
from core.stopwatch import Stopwatch
from core.timer import CountdownTimer
from ui.stopwatch_widget import StopwatchWidget
from ui.timer_widget import TimerWidget


class MainWindow(QMainWindow):
    """Главное окно с двумя независимыми режимами."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PPLAB3VAR13")
        self.resize(900, 700)
        self.setMinimumSize(650, 550)

        self.stopwatch = Stopwatch()
        self.timer = CountdownTimer()
        # Настройки подтверждений действуют только в рамках текущего запуска.
        self.confirmations = {"reset": False, "exit": False}
        self._allow_close = False

        central = QWidget()
        central.setObjectName("mainBackground")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(14, 10, 14, 10)
        root.setSpacing(6)

        header = QHBoxLayout()
        header.addStretch()
        self.exit_button = QPushButton("⏻")
        self.exit_button.setObjectName("exitButton")
        self.exit_button.setToolTip("Exit")
        self.exit_button.setFixedSize(40, 40)
        self.exit_button.clicked.connect(self._confirm_exit)
        header.addWidget(self.exit_button)
        root.addLayout(header)

        self.stack = QStackedWidget()
        self.stopwatch_widget = StopwatchWidget(
            self.stopwatch, self.confirmations
        )
        self.timer_widget = TimerWidget(self.timer, self.confirmations)
        self.stack.addWidget(self.stopwatch_widget)
        self.stack.addWidget(self.timer_widget)
        root.addWidget(self.stack, 1)

        navigation = QHBoxLayout()
        navigation.setContentsMargins(0, 4, 0, 2)
        navigation.addStretch()
        self.stopwatch_tab = QPushButton("STOPWATCH")
        self.timer_tab = QPushButton("TIMER")
        self.stopwatch_tab.setCheckable(True)
        self.timer_tab.setCheckable(True)
        self.stopwatch_tab.setObjectName("navButton")
        self.timer_tab.setObjectName("navButton")
        self.stopwatch_tab.clicked.connect(lambda: self._switch_tab(0))
        self.timer_tab.clicked.connect(lambda: self._switch_tab(1))
        navigation.addWidget(self.stopwatch_tab)
        navigation.addWidget(self.timer_tab)
        navigation.addStretch()
        root.addLayout(navigation)

        self._switch_tab(0)
        self.controller = AppController(
            self.stopwatch_widget, self.timer_widget, self
        )

    def _switch_tab(self, index):
        self.stack.setCurrentIndex(index)
        self.stopwatch_tab.setChecked(index == 0)
        self.timer_tab.setChecked(index == 1)
        if index == 1:
            self.timer_widget.refresh()
            self.timer_widget.show_completion_dialog()

    def _confirm_exit(self):
        self.close()

    def closeEvent(self, event):
        if self._allow_close:
            event.accept()
        else:
            reply = QMessageBox.question(
                self,
                "Exit",
                "Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes |
                QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )

            if reply == QMessageBox.StandardButton.Yes:
                self._allow_close = True
                event.accept()
            else:
                event.ignore()
                return

        # Останавливаем обновление интерфейса перед закрытием приложения.
        if hasattr(self, "controller"):
            self.controller.stop()
