def build_query(intent: dict):
    t = intent["type"]

    if t == "count_all_videos":
        return "SELECT COUNT(*) FROM videos", ()

    if t == "count_creator_videos":
        return (
            "SELECT COUNT(*) FROM videos WHERE creator_id = %s",
            (intent["creator_id"],)
        )

    if t == "videos_over_views":
        return (
            "SELECT COUNT(*) FROM videos WHERE views_count > %s",
            (intent["threshold"],)
        )

    if t == "sum_delta_views":
        return (
            """
            SELECT COALESCE(SUM(delta_views_count), 0)
            FROM video_snapshots
            WHERE DATE(created_at) = %s
            """,
            (intent["date"],)
        )

    if t == "count_active_videos":
        return (
            """
            SELECT COUNT(DISTINCT video_id)
            FROM video_snapshots
            WHERE DATE(created_at) = %s
              AND delta_views_count > 0
            """,
            (intent["date"],)
        )

    return None, None
