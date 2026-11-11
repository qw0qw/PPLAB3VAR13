"""Прямоугольная дорожка и анимация пиксельного персонажа."""

import math
import time
from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QPainter, QPen, QPixmap, QTransform
from PySide6.QtWidgets import QWidget


class RunningTrack(QWidget):
    """Рисует рамку, цифровое время и бегущего по периметру персонажа."""

    def __init__(self, image_name, clockwise=True, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(190)
        self._clockwise = clockwise
        self._running = False
        self._elapsed_seconds = 0.0
        self._animation_phase = 0.0
        image_path = (
            Path(__file__).resolve().parent.parent
            / "resources" / "images" / image_name
        )
        self._pixmap = QPixmap(str(image_path))
        self._scaled_cache = {}
        self._timer = QTimer(self)
        self._timer.setInterval(35)
        self._timer.timeout.connect(self._animate)
        self._last_tick = None
        self.display_text = "00:00:00"
        self.caption = "STOPWATCH"
        self._alert = False

    def set_running(self, running):
        running = bool(running)
        if running == self._running:
            return
        self._running = running
        if self._running:
            self._last_tick = None
            self._timer.start()
        else:
            self._timer.stop()
            self._last_tick = None
        self.update()

    def set_time(self, text):
        self.display_text = text
        self.update()

    def set_caption(self, text):
        self.caption = text
        self.update()

    def set_alert(self, enabled):
        """Включить или выключить мигание фона."""
        self._alert = bool(enabled)
        self.update()

    def reset_position(self):
        self._elapsed_seconds = 0.0
        self._animation_phase = 0.0
        self.update()

    def _animate(self):
        # Персонаж движется по времени, а не по количеству кадров.
        now = time.monotonic()
        if self._last_tick is not None:
            delta = min(now - self._last_tick, 0.1)
            self._elapsed_seconds += delta
            self._animation_phase += delta * 2.0 * math.pi * 2.2
        self._last_tick = now
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        background = QColor("#281018") if self._alert else QColor("#808080")
        painter.fillRect(self.rect(), background)

        margin_x = max(26, int(self.width() * 0.055))
        margin_y = 30
        track = self.rect().adjusted(
            margin_x, margin_y, -margin_x, -margin_y
        )

        pen = QPen(QColor("#2879E8"), 2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRect(track)

        painter.setPen(QColor("#FFFFFF"))
        font = painter.font()
        font.setFamily("DejaVu Sans")
        font.setPixelSize(max(28, min(58, int(self.height() * 0.22))))
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(
            track.adjusted(20, 8, -20, -8),
            Qt.AlignmentFlag.AlignCenter,
            self.display_text,
        )

        painter.setPen(QColor("#78869A"))
        small_font = painter.font()
        small_font.setPixelSize(10)
        small_font.setBold(False)
        painter.setFont(small_font)
        painter.drawText(
            track.adjusted(10, 12, -10, -12),
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom,
            self.caption,
        )

        if not self._pixmap.isNull():
            self._draw_character(painter, track)

    def _draw_character(self, painter, rect):
        # Периметр задаётся как путь из четырёх сторон прямоугольника.
        width = max(1, rect.width())
        height = max(1, rect.height())
        perimeter = 2 * (width + height)
        distance = (self._elapsed_seconds / 60.0) * perimeter
        if not self._clockwise:
            distance = -distance
        distance %= perimeter

        if distance < width:
            x, y = rect.left() + distance, rect.top()
            angle = 0
        elif distance < width + height:
            x, y = rect.right(), rect.top() + distance - width
            angle = 90
        elif distance < 2 * width + height:
            x = rect.right() - (distance - width - height)
            y = rect.bottom()
            angle = 180
        else:
            x = rect.left()
            y = rect.bottom() - (distance - 2 * width - height)
            angle = 270

        if not self._clockwise:
            angle = (angle + 180) % 360

        bob = math.sin(self._animation_phase) * 3 if self._running else 0
        pixmap = self._pixmap
        target_size = max(34, min(58, int(self.height() * 0.25)))
        cache_key = (target_size, angle)
        rotated = self._scaled_cache.get(cache_key)
        if rotated is None:
            scaled = pixmap.scaled(
                target_size, target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            transform = QTransform().rotate(angle)
            rotated = scaled.transformed(
                transform, Qt.TransformationMode.SmoothTransformation
            )
            self._scaled_cache[cache_key] = rotated
        painter.drawPixmap(
            int(x - rotated.width() / 2),
            int(y - rotated.height() / 2 + bob),
            rotated,
        )
