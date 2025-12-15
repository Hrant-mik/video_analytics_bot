import re
from datetime import date

MONTHS = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}

def parse_date(text: str):
    m = re.search(r"(\d{1,2})\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)\s+(\d{4})", text)
    if not m:
        return None
    day, month, year = m.groups()
    return date(int(year), MONTHS[month], int(day))

def parse_intent(text: str) -> dict:
    text = text.lower()

    # Сколько всего видео есть в системе?
    if "сколько всего видео" in text:
        return {"type": "count_all_videos"}

    # Сколько видео у креатора с id ...
    if "сколько видео у креатора" in text:
        creator_id = int(re.search(r"id\s*(\d+)", text).group(1))
        return {"type": "count_creator_videos", "creator_id": creator_id}

    # Сколько видео набрало больше 100000 просмотров
    if "больше" in text and "просмотров" in text:
        threshold = int(re.search(r"(\d+)", text).group(1))
        return {"type": "videos_over_views", "threshold": threshold}

    # На сколько просмотров выросли все видео 28 ноября 2025
    if "на сколько просмотров" in text and "выросли" in text:
        d = parse_date(text)
        return {"type": "sum_delta_views", "date": d}

    # Сколько разных видео получали новые просмотры
    if "сколько разных видео" in text and "новые просмотры" in text:
        d = parse_date(text)
        return {"type": "count_active_videos", "date": d}

    return {"type": "unknown"}
