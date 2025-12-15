# Telegram бот для аналитики видео

## Описание
Telegram-бот принимает вопросы на русском языке и считает метрики по видео
на основе данных в PostgreSQL.

Ответ бота — всегда одно число.

## Технологии
- Python 3.11
- PostgreSQL
- aiogram 2.x

## Структура данных

### Таблица videos
- id
- creator_id
- video_created_at
- views_count
- likes_count
- comments_count
- reports_count

### Таблица video_snapshots
- video_id
- views_count, likes_count, comments_count, reports_count
- delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count
- created_at

## Загрузка данных
JSON-файл должен быть размещён по пути:

