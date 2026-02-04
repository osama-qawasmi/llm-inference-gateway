from datetime import datetime, timezone
from uuid import uuid4

from app.db.session import get_connection
from app.schemas.usage import UsageListResponse, UsageRecord


def insert_usage(
    provider: str,
    model: str,
    message: str,
    response: str,
    success: bool,
    latency_ms: float | None,
    input_tokens: int | None,
    output_tokens: int | None,
    total_tokens: int | None,
    cost_usd: float | None,
    error_message: str | None,
) -> UsageRecord:
    record_id = str(uuid4())
    created_at = datetime.now(timezone.utc).isoformat()
    with get_connection() as connection:
        connection.execute(
            """
            INSERT INTO usage_logs (
                id, created_at, provider, model,
                success, latency_ms,
                input_tokens, output_tokens, total_tokens,
                cost_usd, error_message, message, response
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                record_id,
                created_at,
                provider,
                model,
                1 if success else 0,
                latency_ms,
                input_tokens,
                output_tokens,
                total_tokens,
                cost_usd,
                error_message,
                message,
                response,
            ),
        )
        connection.commit()
    return UsageRecord(
        id=record_id,
        created_at=created_at,
        provider=provider,
        model=model,
        success=success,
        latency_ms=latency_ms,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        cost_usd=cost_usd,
        error_message=error_message,
        message=message,
        response=response,
    )


def list_usage(limit: int = 50, offset: int = 0) -> UsageListResponse:
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT id, created_at, provider, model,
                   COALESCE(success, 1) AS success,
                   latency_ms,
                   input_tokens, output_tokens, total_tokens,
                   cost_usd, error_message, message, response
            FROM usage_logs
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        ).fetchall()
    items = [UsageRecord(**dict(row)) for row in rows]
    return UsageListResponse(items=items)
