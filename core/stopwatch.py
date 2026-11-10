"""Логика секундомера без зависимости от графического интерфейса."""

import time


class Stopwatch:
    """Секундомер с независимым монотонным отсчётом."""

    def __init__(self):
        self._elapsed_before_start = 0.0
        self._started_at = None
        self._laps = []
        self._last_lap_hundredths = 0

    @property
    def is_running(self):
        return self._started_at is not None

    @property
    def elapsed_hundredths(self):
        elapsed = self._elapsed_before_start
        if self.is_running:
            elapsed += time.monotonic() - self._started_at
        return int(elapsed * 100)

    @property
    def laps(self):
        return list(self._laps)

    def start(self):
        """Начать новый отсчёт, если секундомер ещё не запускался."""
        if self.is_running:
            return
        if self._elapsed_before_start == 0 and not self._laps:
            self._last_lap_hundredths = 0
        self._started_at = time.monotonic()

    def pause(self):
        """Приостановить отсчёт."""
        if self.is_running:
            self._elapsed_before_start += time.monotonic() - self._started_at
            self._started_at = None

    def resume(self):
        """Продолжить отсчёт после паузы или Stop."""
        if not self.is_running:
            self._started_at = time.monotonic()

    def stop(self):
        """Остановить отсчёт, сохранив время и круги."""
        self.pause()

    def reset(self):
        """Полностью очистить секундомер."""
        self._elapsed_before_start = 0.0
        self._started_at = None
        self._laps.clear()
        self._last_lap_hundredths = 0

    def add_lap(self):
        """Сохранить длительность круга и общее время."""
        if not self.is_running:
            return None
        total = self.elapsed_hundredths
        lap_time = total - self._last_lap_hundredths
        self._last_lap_hundredths = total
        lap = {
            "number": len(self._laps) + 1,
            "duration": lap_time,
            "total": total,
        }
        self._laps.append(lap)
        return lap
