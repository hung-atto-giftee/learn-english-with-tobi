from datetime import UTC, datetime

from app.database import get_connection


def save_learning_history(
    user_id: int,
    sentence: str,
    user_input: str,
    accuracy: float,
) -> None:
    created_at = datetime.now(UTC).isoformat(timespec="seconds")

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO learning_history (user_id, sentence, user_input, accuracy, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (user_id, sentence, user_input, accuracy, created_at),
            )
        connection.commit()


def get_user_learning_history(user_id: int, limit: int = 50) -> list[dict]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, sentence, user_input, accuracy, created_at
                FROM learning_history
                WHERE user_id = %s
                ORDER BY created_at DESC, id DESC
                LIMIT %s
                """,
                (user_id, limit),
            )
            rows = cursor.fetchall()

    return rows


def get_user_learning_stats(user_id: int, trend_limit: int = 20) -> dict:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    COALESCE(AVG(accuracy), 0) AS average_accuracy,
                    COUNT(*) AS total_sentences_practiced
                FROM learning_history
                WHERE user_id = %s
                """,
                (user_id,),
            )
            stats = cursor.fetchone()

            cursor.execute(
                """
                SELECT created_at, accuracy
                FROM (
                    SELECT created_at, accuracy
                    FROM learning_history
                    WHERE user_id = %s
                    ORDER BY created_at DESC, id DESC
                    LIMIT %s
                ) AS latest_results
                ORDER BY created_at ASC
                """,
                (user_id, trend_limit),
            )
            trend_rows = cursor.fetchall()

    return {
        "average_accuracy": round(float(stats["average_accuracy"]), 2),
        "total_sentences_practiced": int(stats["total_sentences_practiced"]),
        "accuracy_trend": trend_rows,
    }
