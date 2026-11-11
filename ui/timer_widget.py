"""Экран обратного таймера."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.time_manager import (
    digits_from_hundredths, format_time, keypad_value
)
from ui.control_buttons import ControlButtons
from ui.keypad import Keypad
from ui.running_track import RunningTrack


class TimerWidget(QWidget):
    """Интерфейс таймера с быстрым выбором и цифровой клавиатурой."""

    def __init__(self, timer, confirmations=None, parent=None):
        super().__init__(parent)
        self.timer = timer
        self.confirmations = confirmations if confirmations is not None else {
            "reset": False, "exit": False
        }
        self.digits = ""
        self._editing = False
        self._completion_dialog_pending = False
        self._dialog_open = False

        self.track = RunningTrack("dog.png", clockwise=False)
        self.track.setMinimumHeight(125)
        self.track.set_caption("TIMER")
        self.quick_buttons = []
        quick_layout = QHBoxLayout()
        quick_layout.setSpacing(8)
        for minutes in (10, 15, 30, 60):
            button = QPushButton(f"{minutes} MIN")
            button.setObjectName("quickButton")
            button.clicked.connect(
                lambda checked=False, value=minutes: self._set_quick(value)
            )
            self.quick_buttons.append(button)
            quick_layout.addWidget(button)

        self.keypad = Keypad()
        self.controls = ControlButtons()
        self.status = QLabel("")
        self.status.setObjectName("timerStatus")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(5)
        layout.addWidget(self.track, 3)
        layout.addLayout(quick_layout)
        layout.addWidget(self.keypad, 2)
        layout.addWidget(self.controls)
        layout.addWidget(self.status)

        for key in "0123456789":
            self.keypad.button(key).clicked.connect(
                lambda checked=False, value=key: self._press_digit(value)
            )
        self.keypad.button("⌫").clicked.connect(self._backspace)
        self.keypad.button("C").clicked.connect(self._clear)

        self.controls.button("start").clicked.connect(self._start)
        self.controls.button("pause").clicked.connect(self._pause)
        self.controls.button("resume").clicked.connect(self._resume)
        self.controls.button("stop").clicked.connect(self._stop)
        self.controls.button("reset").clicked.connect(self._reset)
        self.refresh()

    def _set_quick(self, minutes):
        self.digits = digits_from_hundredths(minutes * 60 * 100)
        self._editing = True
        self.timer.set_duration(keypad_value(self.digits))
        self.status.setText("")
        self.refresh()

    def _press_digit(self, digit):
        self.digits = (self.digits + digit)[-6:]
        self._editing = True
        self.timer.set_duration(keypad_value(self.digits))
        self.status.setText("")
        self.refresh()

    def _backspace(self):
        self.digits = self.digits[:-1]
        self._editing = True
        self.timer.set_duration(keypad_value(self.digits))
        self.refresh()

    def _clear(self):
        self.digits = ""
        self._editing = True
        self.timer.reset()
        self.track.reset_position()
        self.status.setText("")
        self.refresh()

    def _start(self):
        self._editing = False
        self.timer.start()
        self.track.reset_position()
        self.refresh()

    def _pause(self):
        self.timer.pause()
        self.refresh()

    def _resume(self):
        self.timer.resume()
        self.refresh()

    def _stop(self):
        self.timer.stop()
        self.refresh()

    def _reset(self):
        if self.confirmations.get("reset", False):
            answer = QMessageBox.StandardButton.Yes
            checkbox = None
        else:
            box = QMessageBox(self)
            box.setWindowTitle("Reset timer?")
            box.setText("The timer value will be cleared. Continue?")
            box.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            box.setDefaultButton(QMessageBox.StandardButton.No)
            checkbox = QCheckBox("Don't ask again", box)
            box.setCheckBox(checkbox)
            answer = box.exec()
        if answer == QMessageBox.StandardButton.Yes:
            if checkbox is not None and checkbox.isChecked():
                self.confirmations["reset"] = True
            self._editing = True
            self.timer.reset()
            self.digits = ""
            self.track.reset_position()
            self.status.setText("")
            self.refresh()

    def on_tick(self):
        just_finished = self.timer.update()
        self.refresh()
        if just_finished:
            self._completion_dialog_pending = True
            if self.isVisible():
                self.show_completion_dialog()

    def show_completion_dialog(self):
        if not self._completion_dialog_pending or self._dialog_open:
            return
        self._completion_dialog_pending = False
        self._dialog_open = True
        QMessageBox.information(
            self, "Timer", "Time's up!",
            QMessageBox.StandardButton.Ok
        )
        self._dialog_open = False
        # После закрытия возвращаем обычный экран настройки таймера.
        self.timer.reset()
        self.digits = ""
        self.status.setText("")
        self.track.reset_position()
        self.refresh()

    def refresh(self):
        running = self.timer.is_running
        remaining = self.timer.remaining_hundredths
        self.track.set_time(format_time(remaining))
        self.track.set_running(running)

        configured = self.timer.is_configured
        finished = self.timer.is_finished
        if running:
            self.controls.show_buttons("pause", "stop", "reset")
            self.keypad.setVisible(False)
            for button in self.quick_buttons:
                button.setVisible(False)
        elif (
            configured
            and not finished
            and remaining > 0
            and not self._editing
        ):
            self.controls.show_buttons("resume", "stop", "reset")
            self.keypad.setVisible(False)
            for button in self.quick_buttons:
                button.setVisible(False)
        else:
            self.controls.show_buttons("start", "reset")
            self.keypad.setVisible(True)
            for button in self.quick_buttons:
                button.setVisible(True)

        # Кнопка Start активна только при установленном ненулевом времени.
        self.controls.button("start").setEnabled(configured and remaining > 0)
        self.controls.button("resume").setEnabled(configured and remaining > 0)

        should_alert = (
            running
            and remaining <= 1000
            and (remaining // 25) % 2 == 0
        )
        self.track.set_alert(should_alert)
