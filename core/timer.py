"""Логика обратного отсчёта без зависимости от графического интерфейса."""

import time


class CountdownTimer:
    """Таймер, который использует монотонные временные отметки."""

    def __init__(self):
        self._remaining = 0.0
        self._deadline = None
        self._configured = False
        self._finished = False

    @property
    def is_running(self):
        return self._deadline is not None

    @property
    def is_configured(self):
        return self._configured

    @property
    def is_finished(self):
        return self._finished

    @property
    def remaining_hundredths(self):
        if self.is_running:
            return max(0, int((self._deadline - time.monotonic()) * 100))
        return max(0, int(self._remaining * 100))

    def set_duration(self, hundredths):
        """Установить длительность нового таймера."""
        self._remaining = max(0, int(hundredths)) / 100
        self._deadline = None
        self._configured = self._remaining > 0
        self._finished = False

    def start(self):
        """Запустить обратный отсчёт."""
        if not self._configured or self.is_running or self._finished:
            return
        self._deadline = time.monotonic() + self._remaining

    def pause(self):
        """Приостановить обратный отсчёт."""
        if self.is_running:
            self._remaining = max(0.0, self._deadline - time.monotonic())
            self._deadline = None

    def stop(self):
        """Остановить таймер, сохранив оставшееся время."""
        self.pause()

    def resume(self):
        """Продолжить обратный отсчёт."""
        if self._configured and not self.is_running and not self._finished:
            self._deadline = time.monotonic() + self._remaining

    def update(self):
        """Обновить состояние и вернуть True при первом достижении нуля."""
        if self.is_running and self.remaining_hundredths <= 0:
            self._remaining = 0.0
            self._deadline = None
            self._finished = True
            return True
        return False

    def reset(self):
        """Очистить таймер."""
        self._remaining = 0.0
        self._deadline = None
        self._configured = False
        self._finished = False
