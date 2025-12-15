import json
import psycopg2
from psycopg2.extras import execute_values
from app.db import DB_CONFIG

def get_connection():
    return psycopg2.connect(
        dbname=DB_CONFIG["dbname"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        port=DB_CONFIG.get("port", 5432)
    )


def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DROP TABLE IF EXISTS video_snapshots;
        DROP TABLE IF EXISTS videos;

        CREATE TABLE videos (
            id UUID PRIMARY KEY,
            creator_id UUID,
            video_created_at TIMESTAMP,
            views_count BIGINT,
            likes_count BIGINT,
            comments_count BIGINT,
            reports_count BIGINT,
            created_at TIMESTAMP DEFAULT now(),
            updated_at TIMESTAMP DEFAULT now()
        );

        CREATE TABLE video_snapshots (
            id BIGSERIAL PRIMARY KEY,
            video_id UUID REFERENCES videos(id),
            views_count BIGINT,
            likes_count BIGINT,
            comments_count BIGINT,
            reports_count BIGINT,
            delta_views_count BIGINT,
            delta_likes_count BIGINT,
            delta_comments_count BIGINT,
            delta_reports_count BIGINT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP DEFAULT now()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Tables created successfully.")


def load_json(json_file="data/videos.json"):
    conn = get_connection()
    cur = conn.cursor()

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for video in data["videos"]:
        cur.execute("""
            INSERT INTO videos (
                id, creator_id, video_created_at,
                views_count, likes_count, comments_count, reports_count
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (id) DO NOTHING
        """, (
            video["id"],           # UUID
            video["creator_id"],   # UUID
            video["video_created_at"],
            video["views_count"],
            video["likes_count"],
            video["comments_count"],
            video["reports_count"],
        ))


        for snap in video.get("snapshots", []):
            cur.execute("""
                INSERT INTO video_snapshots (
                    video_id,
                    views_count, likes_count, comments_count, reports_count,
                    delta_views_count, delta_likes_count,
                    delta_comments_count, delta_reports_count,
                    created_at
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """, (
                video["id"],                # UUID
                snap["views_count"],
                snap["likes_count"],
                snap["comments_count"],
                snap["reports_count"],
                snap["delta_views_count"],
                snap["delta_likes_count"],
                snap["delta_comments_count"],
                snap["delta_reports_count"],
                snap["created_at"],
            ))

    conn.commit()
    cur.close()
    conn.close()
    print("JSON data loaded successfully.")


if __name__ == "__main__":
    create_tables()
    load_json()
