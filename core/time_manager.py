"""Вспомогательные функции для работы со временем."""

HUNDREDTHS_PER_SECOND = 100
HUNDREDTHS_PER_MINUTE = 60 * HUNDREDTHS_PER_SECOND


def format_time(total_hundredths: int) -> str:
    """Преобразовать сотые доли секунды в формат ММ:СС:СС."""
    total_hundredths = max(0, int(total_hundredths))
    minutes, remainder = divmod(total_hundredths, HUNDREDTHS_PER_MINUTE)
    seconds, hundredths = divmod(remainder, HUNDREDTHS_PER_SECOND)
    return f"{minutes:02d}:{seconds:02d}:{hundredths:02d}"


def keypad_value(digits: str) -> int:
    """Преобразовать ввод клавиатуры справа налево в сотые секунды."""
    clean = "".join(
        char for char in digits if char.isdigit()
    )[-6:].rjust(6, "0")
    minutes = int(clean[:2])
    seconds = int(clean[2:4])
    hundredths = int(clean[4:6])
    seconds += minutes * 60
    return (seconds * HUNDREDTHS_PER_SECOND) + hundredths


def digits_from_hundredths(value: int) -> str:
    """Вернуть шестизначное представление времени для экранной клавиатуры."""
    value = max(0, int(value))
    minutes, remainder = divmod(value, HUNDREDTHS_PER_MINUTE)
    seconds, hundredths = divmod(remainder, HUNDREDTHS_PER_SECOND)
    return f"{minutes % 100:02d}{seconds:02d}{hundredths:02d}"
