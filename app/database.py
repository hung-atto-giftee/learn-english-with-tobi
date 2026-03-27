import os
from pathlib import Path

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "ttsdb")
DB_USER = os.getenv("POSTGRES_USER", "ttsuser")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "root")


def get_connection() -> psycopg.Connection:
    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        row_factory=dict_row,
    )


def init_db() -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email TEXT NOT NULL UNIQUE,
                hashed_password TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
            )
            cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS learning_history (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                sentence TEXT NOT NULL,
                user_input TEXT NOT NULL,
                accuracy DOUBLE PRECISION NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
            )
            cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_word_history (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                word TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
            )
        connection.commit()


def save_user_word_history(user_id: int, word: str, created_at: str) -> None:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO user_word_history (user_id, word, created_at)
                VALUES (%s, %s, %s)
                """,
                (user_id, word, created_at),
            )
        connection.commit()


def get_user_word_history(user_id: int, limit: int = 50) -> list[dict]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, user_id, word, created_at
                FROM user_word_history
                WHERE user_id = %s
                ORDER BY created_at DESC, id DESC
                LIMIT %s
                """,
                (user_id, limit),
            )
            rows = cursor.fetchall()

    return rows


def get_user_frequent_words(user_id: int, limit: int = 20) -> list[dict]:
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT word, COUNT(*) AS lookup_count, MAX(created_at) AS last_lookup_at
                FROM user_word_history
                WHERE user_id = %s
                GROUP BY word
                ORDER BY lookup_count DESC, last_lookup_at DESC
                LIMIT %s
                """,
                (user_id, limit),
            )
            rows = cursor.fetchall()

    return rows
