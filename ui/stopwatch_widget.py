"""Экран секундомера."""

from PySide6.QtWidgets import QCheckBox, QMessageBox, QVBoxLayout, QWidget

from core.time_manager import format_time
from ui.control_buttons import ControlButtons
from ui.laps_list import LapsList
from ui.running_track import RunningTrack


class StopwatchWidget(QWidget):
    """Интерфейс секундомера."""

    def __init__(self, stopwatch, confirmations=None, parent=None):
        super().__init__(parent)
        self.stopwatch = stopwatch
        self.confirmations = confirmations if confirmations is not None else {
            "reset": False, "exit": False
        }
        self.track = RunningTrack("cat.png", clockwise=True)
        self.track.set_caption("STOPWATCH")
        self.controls = ControlButtons()
        self.laps = LapsList()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 12, 22, 12)
        layout.setSpacing(8)
        layout.addWidget(self.track, 3)
        layout.addWidget(self.controls, 0)
        layout.addWidget(self.laps, 2)

        self.controls.button("start").clicked.connect(self._start)
        self.controls.button("pause").clicked.connect(self._pause)
        self.controls.button("resume").clicked.connect(self._resume)
        self.controls.button("stop").clicked.connect(self._stop)
        self.controls.button("reset").clicked.connect(self._reset)
        self.controls.button("lap").clicked.connect(self._lap)
        self.refresh()
        self._refresh_laps()

    def _start(self):
        self.stopwatch.start()
        self.refresh()

    def _pause(self):
        self.stopwatch.pause()
        self.refresh()

    def _resume(self):
        self.stopwatch.resume()
        self.refresh()

    def _stop(self):
        self.stopwatch.stop()
        self.refresh()

    def _reset(self):
        if self.confirmations.get("reset", False):
            answer = QMessageBox.StandardButton.Yes
            checkbox = None
        else:
            box = QMessageBox(self)
            box.setWindowTitle("Reset stopwatch?")
            box.setText(
                "The time and all saved laps will be cleared. Continue?"
            )
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
            self.stopwatch.reset()
            self.track.reset_position()
            self.refresh()
            self._refresh_laps()

    def _lap(self):
        self.stopwatch.add_lap()
        self._refresh_laps()
        self.refresh()

    def _refresh_laps(self):
        self.laps.set_laps(self.stopwatch.laps, format_time)

    def refresh(self):
        running = self.stopwatch.is_running
        self.track.set_time(format_time(self.stopwatch.elapsed_hundredths))
        self.track.set_running(running)
        if running:
            self.controls.show_buttons("pause", "stop", "reset", "lap")
        elif self.stopwatch.elapsed_hundredths > 0:
            self.controls.show_buttons("resume", "stop", "reset")
        else:
            self.controls.show_buttons("start", "reset")
