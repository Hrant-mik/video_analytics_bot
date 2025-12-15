-- Удаляем старые таблицы, если они есть
DROP TABLE IF EXISTS video_snapshots;
DROP TABLE IF EXISTS videos;

-- Таблица итоговой статистики по видео
CREATE TABLE videos (
    id UUID PRIMARY KEY,               -- идентификатор видео
    creator_id UUID,                   -- идентификатор креатора
    video_created_at TIMESTAMP,        -- дата и время публикации
    views_count BIGINT,                -- финальное количество просмотров
    likes_count BIGINT,                -- финальное количество лайков
    comments_count BIGINT,             -- финальное количество комментариев
    reports_count BIGINT,              -- финальное количество жалоб
    created_at TIMESTAMP DEFAULT now(),-- служебное поле
    updated_at TIMESTAMP DEFAULT now() -- служебное поле
);

-- Таблица почасовых замеров по видео
CREATE TABLE video_snapshots (
    id BIGSERIAL PRIMARY KEY,          -- идентификатор снапшота
    video_id UUID REFERENCES videos(id), -- ссылка на видео
    views_count BIGINT,                -- текущее количество просмотров
    likes_count BIGINT,                -- текущее количество лайков
    comments_count BIGINT,             -- текущее количество комментариев
    reports_count BIGINT,              -- текущее количество жалоб
    delta_views_count BIGINT,          -- приращение просмотров
    delta_likes_count BIGINT,          -- приращение лайков
    delta_comments_count BIGINT,       -- приращение комментариев
    delta_reports_count BIGINT,        -- приращение жалоб
    created_at TIMESTAMP,              -- время замера
    updated_at TIMESTAMP DEFAULT now() -- служебное поле
);
