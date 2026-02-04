from app.db.session import get_connection


def get_summary_row() -> dict:
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT
                COUNT(*) AS total_requests,
                SUM(CASE WHEN COALESCE(success, 1) = 1 THEN 1 ELSE 0 END) AS success_count,
                SUM(CASE WHEN COALESCE(success, 1) = 0 THEN 1 ELSE 0 END) AS failure_count,
                AVG(latency_ms) AS avg_latency_ms,
                AVG(total_tokens) AS avg_tokens,
                AVG(cost_usd) AS avg_cost_usd,
                SUM(cost_usd) AS total_cost_usd
            FROM usage_logs
            """
        ).fetchone()
    return dict(row or {})


def get_latency_values() -> list[float]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT latency_ms
            FROM usage_logs
            WHERE latency_ms IS NOT NULL
            ORDER BY latency_ms
            """
        ).fetchall()
    return [row["latency_ms"] for row in rows]


def get_model_rows() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                model,
                COUNT(*) AS total_requests,
                SUM(CASE WHEN COALESCE(success, 1) = 1 THEN 1 ELSE 0 END) AS success_count,
                AVG(latency_ms) AS avg_latency_ms,
                AVG(total_tokens) AS avg_tokens,
                AVG(cost_usd) AS avg_cost_usd
            FROM usage_logs
            GROUP BY model
            ORDER BY total_requests DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]
