"""Связующий объект логики приложения и его экранов."""

from PySide6.QtCore import QObject, QTimer


class AppController(QObject):
    """Обновляет независимые режимы и обрабатывает завершение таймера."""

    def __init__(self, stopwatch_widget, timer_widget, parent=None):
        super().__init__(parent)
        self.stopwatch_widget = stopwatch_widget
        self.timer_widget = timer_widget

        self._ticker = QTimer(self)
        self._ticker.setInterval(20)
        self._ticker.timeout.connect(self._update)
        self._ticker.start()

    def _update(self):
        # Оба механизма времени обновляются независимо от выбранной вкладки.
        self.stopwatch_widget.refresh()
        self.timer_widget.on_tick()

    def stop(self):
        """Остановить периодическое обновление интерфейса."""
        self._ticker.stop()
