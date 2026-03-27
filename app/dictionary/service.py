import asyncio
import json
import logging
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx

from app.database import (
    get_user_frequent_words,
    get_user_word_history,
    save_user_word_history,
)

DICTIONARY_API_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
TRANSLATION_API_URL = "https://api.mymemory.translated.net/get?q={text}&langpair=en|vi"
WORD_PATTERN = re.compile(r"[A-Za-z']+")
REQUEST_TIMEOUT = httpx.Timeout(5.0, connect=3.0)
MAX_RETRIES = 2
DICTIONARY_CACHE_DB = Path(__file__).resolve().parent.parent.parent / "dictionary_cache.db"
logger = logging.getLogger(__name__)

VIETNAMESE_MEANING_MAP: dict[str, list[dict[str, str]]] = {
    "learning": [{"part_of_speech": "noun", "en": "the process of gaining knowledge", "vi": "việc học"}],
    "english": [{"part_of_speech": "noun", "en": "the English language", "vi": "tiếng Anh"}],
    "fun": [{"part_of_speech": "adjective", "en": "enjoyable or entertaining", "vi": "vui, thú vị"}],
    "example": [{"part_of_speech": "noun", "en": "a representative form or pattern", "vi": "ví dụ"}],
    "hello": [{"part_of_speech": "interjection", "en": "used as a greeting", "vi": "xin chào"}],
    "world": [{"part_of_speech": "noun", "en": "the earth and all people", "vi": "thế giới"}],
    "practice": [{"part_of_speech": "noun", "en": "repeated exercise for improvement", "vi": "sự luyện tập"}],
    "sentence": [{"part_of_speech": "noun", "en": "a set of words expressing a statement", "vi": "câu"}],
    "word": [{"part_of_speech": "noun", "en": "a single distinct meaningful element of speech", "vi": "từ"}],
    "listen": [{"part_of_speech": "verb", "en": "give attention with the ear", "vi": "lắng nghe"}],
}

PHONETIC_MAP: dict[str, str] = {
    "learning": "/ˈlɝː.nɪŋ/",
    "english": "/ˈɪŋ.ɡlɪʃ/",
    "fun": "/fʌn/",
    "example": "/ɪɡˈzæm.pəl/",
    "hello": "/həˈloʊ/",
    "world": "/wɝːld/",
    "practice": "/ˈpræk.tɪs/",
    "sentence": "/ˈsen.təns/",
    "word": "/wɝːd/",
    "listen": "/ˈlɪs.ən/",
}


def normalize_word(word: str) -> str:
    matches = WORD_PATTERN.findall(word.lower())
    return "".join(matches)


async def translate_to_vi(text: str) -> str | None:
    if not text.strip():
        return None

    candidates = [text.strip()]

    shortened_by_clause = re.split(r"[;,:()]", text, maxsplit=1)[0].strip()
    if shortened_by_clause and shortened_by_clause not in candidates:
        candidates.append(shortened_by_clause)

    shortened_by_length = text.strip()[:120].rsplit(" ", 1)[0].strip()
    if shortened_by_length and shortened_by_length not in candidates:
        candidates.append(shortened_by_length)

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            for candidate in candidates:
                response = await client.get(
                    TRANSLATION_API_URL,
                    params={
                        "q": candidate,
                        "langpair": "en|vi",
                    },
                )
                response.raise_for_status()
                payload = response.json()
                translated_text = (
                    payload.get("responseData", {}).get("translatedText", "").strip()
                )

                if translated_text and translated_text.lower() != candidate.lower():
                    return translated_text
    except (httpx.HTTPError, ValueError):
        logger.info("Translation to Vietnamese failed for text: %s", text)
        return None

    logger.info("Translation API returned no useful Vietnamese output for text: %s", text)
    return None


def init_dictionary_cache() -> None:
    with sqlite3.connect(DICTIONARY_CACHE_DB) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS dictionary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                phonetic TEXT NOT NULL,
                meanings_json TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        migrate_dictionary_table(connection)
        connection.commit()


def migrate_dictionary_table(connection: sqlite3.Connection) -> None:
    rows = connection.execute(
        """
        SELECT id, word, phonetic, meanings_json, created_at, updated_at
        FROM dictionary
        ORDER BY updated_at DESC, id DESC
        """
    ).fetchall()

    latest_by_word: dict[str, tuple[Any, ...]] = {}
    for row in rows:
        normalized = normalize_word(row[1])
        if not normalized:
            continue
        if normalized not in latest_by_word:
            latest_by_word[normalized] = (
                row[0],
                normalized,
                row[2],
                row[3],
                row[4],
                row[5],
            )

    connection.execute("DROP TABLE IF EXISTS dictionary_migrated")
    connection.execute(
        """
        CREATE TABLE dictionary_migrated (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            phonetic TEXT NOT NULL,
            meanings_json TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    for _, normalized, phonetic, meanings_json, created_at, updated_at in latest_by_word.values():
        connection.execute(
            """
            INSERT INTO dictionary_migrated (
                word,
                phonetic,
                meanings_json,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (normalized, phonetic, meanings_json, created_at, updated_at),
        )

    connection.execute("DROP TABLE dictionary")
    connection.execute("ALTER TABLE dictionary_migrated RENAME TO dictionary")
    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_dictionary_word
        ON dictionary(word)
        """
    )


def get_word(word: str) -> dict[str, Any] | None:
    with sqlite3.connect(DICTIONARY_CACHE_DB) as connection:
        row = connection.execute(
            """
            SELECT id, word, phonetic, meanings_json, created_at, updated_at
            FROM dictionary
            WHERE word = ?
            """,
            (word,),
        ).fetchone()

    if not row:
        return None

    return {
        "id": row[0],
        "word": row[1],
        "phonetic": row[2],
        "meanings": json.loads(row[3]),
        "created_at": row[4],
        "updated_at": row[5],
        "cached": True,
    }


def save_word(data: dict[str, Any]) -> dict[str, Any]:
    normalized_word = normalize_word(data.get("word", ""))
    if not normalized_word:
        return data

    with sqlite3.connect(DICTIONARY_CACHE_DB) as connection:
        connection.execute(
            """
            INSERT INTO dictionary (word, phonetic, meanings_json)
            VALUES (?, ?, ?)
            ON CONFLICT(word) DO UPDATE SET
                phonetic = excluded.phonetic,
                meanings_json = excluded.meanings_json,
                updated_at = CURRENT_TIMESTAMP
            """,
            (
                normalized_word,
                data.get("phonetic", ""),
                json.dumps(data.get("meanings", []), ensure_ascii=False),
            ),
        )
        connection.commit()

    cached_word = get_word(normalized_word)
    return cached_word if cached_word else data


def list_words(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    start_date: str = "",
    end_date: str = "",
) -> dict[str, Any]:
    normalized_search = normalize_word(search) if search else ""
    offset = (page - 1) * limit
    conditions: list[str] = []
    parameters: list[Any] = []

    if normalized_search:
        conditions.append("word LIKE ?")
        parameters.append(f"%{normalized_search}%")

    if start_date:
        conditions.append("date(COALESCE(updated_at, created_at)) >= date(?)")
        parameters.append(start_date)

    if end_date:
        conditions.append("date(COALESCE(updated_at, created_at)) <= date(?)")
        parameters.append(end_date)

    where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

    with sqlite3.connect(DICTIONARY_CACHE_DB) as connection:
        total_row = connection.execute(
            f"""
            SELECT COUNT(*) FROM dictionary
            {where_clause}
            """,
            parameters,
        ).fetchone()
        rows = connection.execute(
            f"""
            SELECT DISTINCT id, word, phonetic, meanings_json, created_at, updated_at
            FROM dictionary
            {where_clause}
            ORDER BY updated_at DESC, id DESC
            LIMIT ? OFFSET ?
            """,
            [*parameters, limit, offset],
        ).fetchall()

    total = int(total_row[0] if total_row else 0)
    items = [
        {
            "id": row[0],
            "word": row[1],
            "phonetic": row[2],
            "meanings": normalize_cached_meanings(json.loads(row[3])),
            "created_at": row[4],
            "updated_at": row[5],
            "cached": True,
        }
        for row in rows
    ]

    total_pages = max(1, (total + limit - 1) // limit) if limit else 1
    return {
        "items": items,
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "search": normalized_search,
        "start_date": start_date,
        "end_date": end_date,
    }


def choose_best_phonetic(entry: dict[str, Any], word: str) -> str:
    phonetics = entry.get("phonetics", [])
    candidates: list[tuple[int, str]] = []

    if entry.get("phonetic"):
        candidates.append((3, entry["phonetic"]))

    for item in phonetics:
        text = item.get("text", "")
        if not text:
            continue

        score = 1
        if item.get("audio"):
            score += 2
        if text.startswith("/"):
            score += 1

        candidates.append((score, text))

    if candidates:
        candidates.sort(key=lambda item: (-item[0], len(item[1])))
        return candidates[0][1]

    return PHONETIC_MAP.get(word, "")


def format_meaning(
    part_of_speech: str,
    english_definition: str,
    vietnamese_definition: str,
) -> dict[str, str]:
    return {
        "part_of_speech": part_of_speech,
        "en": english_definition,
        "vi": vietnamese_definition,
        "definition": vietnamese_definition or english_definition,
    }


def normalize_cached_meanings(meanings: list[dict[str, Any]]) -> list[dict[str, str]]:
    normalized_meanings: list[dict[str, str]] = []

    for item in meanings:
        part_of_speech = str(item.get("part_of_speech", "unknown"))
        english_definition = str(item.get("en") or item.get("definition") or "").strip()
        vietnamese_definition = str(item.get("vi") or "").strip()
        normalized_meanings.append(
            format_meaning(part_of_speech, english_definition, vietnamese_definition)
        )

    return normalized_meanings


def build_mock_response(word: str) -> dict[str, Any]:
    raw_meanings = VIETNAMESE_MEANING_MAP.get(
        word,
        [
            {
                "part_of_speech": "unknown",
                "en": "No English definition available.",
                "vi": "Chua co nghia tieng Viet cho tu nay.",
            }
        ],
    )
    meanings = [
        format_meaning(
            item.get("part_of_speech", "unknown"),
            item.get("en", ""),
            item.get("vi", ""),
        )
        for item in raw_meanings
    ]
    return {
        "word": word,
        "phonetic": PHONETIC_MAP.get(word, ""),
        "meanings": meanings,
    }


async def parse_dictionary_response(word: str, payload: list[dict[str, Any]]) -> dict[str, Any]:
    entry = payload[0] if payload else {}
    phonetic = choose_best_phonetic(entry, word)

    meanings: list[dict[str, str]] = [
        format_meaning(
            item.get("part_of_speech", "unknown"),
            item.get("en", ""),
            item.get("vi", ""),
        )
        for item in VIETNAMESE_MEANING_MAP.get(word, [])
    ]
    seen_meanings = {
        (item["part_of_speech"], item["en"])
        for item in meanings
    }

    for meaning in entry.get("meanings", []):
        part_of_speech = meaning.get("partOfSpeech", "unknown")
        for definition_item in meaning.get("definitions", [])[:3]:
            english_definition = definition_item.get("definition", "").strip()
            if not english_definition:
                continue

            meaning_key = (part_of_speech, english_definition)
            if meaning_key in seen_meanings:
                continue

            vietnamese_definition = await translate_to_vi(english_definition) or ""
            meanings.append(
                format_meaning(part_of_speech, english_definition, vietnamese_definition)
            )
            seen_meanings.add(meaning_key)

            if len(meanings) >= 6:
                break

        if len(meanings) >= 6:
            break

    return {
        "word": word,
        "phonetic": phonetic,
        "meanings": meanings or build_mock_response(word)["meanings"],
    }


async def fetch_dictionary_from_api(word: str) -> dict[str, Any] | None:
    last_error: Exception | None = None

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await client.get(DICTIONARY_API_URL.format(word=word))
                if response.status_code == 404:
                    logger.info("Dictionary entry not found for word '%s'.", word)
                    return None

                response.raise_for_status()
                return await parse_dictionary_response(word, response.json())
            except httpx.TimeoutException as exc:
                last_error = exc
                logger.warning(
                    "Dictionary timeout for word '%s' on attempt %s/%s.",
                    word,
                    attempt,
                    MAX_RETRIES,
                )
            except httpx.HTTPStatusError as exc:
                last_error = exc
                logger.warning(
                    "Dictionary HTTP error for word '%s' on attempt %s/%s: %s",
                    word,
                    attempt,
                    MAX_RETRIES,
                    exc.response.status_code,
                )
            except (httpx.HTTPError, ValueError) as exc:
                last_error = exc
                logger.exception(
                    "Dictionary lookup failed for word '%s' on attempt %s/%s.",
                    word,
                    attempt,
                    MAX_RETRIES,
                )

            if attempt < MAX_RETRIES:
                await asyncio.sleep(0.2 * attempt)

    if last_error:
        logger.warning("Dictionary fallback activated for word '%s'.", word)

    return None


async def lookup_word(word: str) -> dict[str, Any]:
    normalized_word = normalize_word(word)
    if not normalized_word:
        return {
            "word": "",
            "phonetic": "",
            "meanings": [{"part_of_speech": "unknown", "definition": "Tu khong hop le."}],
            "cached": False,
        }

    cached_result = get_word(normalized_word)
    if cached_result:
        cached_result["meanings"] = normalize_cached_meanings(cached_result.get("meanings", []))

        needs_translation = any(
            meaning.get("en") and not meaning.get("vi")
            for meaning in cached_result["meanings"]
        )
        if needs_translation:
            updated_meanings = []
            for meaning in cached_result["meanings"]:
                english_definition = meaning.get("en", "")
                vietnamese_definition = meaning.get("vi", "")
                if english_definition and not vietnamese_definition:
                    vietnamese_definition = await translate_to_vi(english_definition) or ""
                updated_meanings.append(
                    format_meaning(
                        meaning.get("part_of_speech", "unknown"),
                        english_definition,
                        vietnamese_definition,
                    )
                )

            cached_result["meanings"] = updated_meanings
            saved_cached_result = save_word(cached_result)
            saved_cached_result["cached"] = True
            return saved_cached_result

        return cached_result

    result = await fetch_dictionary_from_api(normalized_word)
    if result is None:
        result = build_mock_response(normalized_word)

    saved_result = save_word(result)
    saved_result["cached"] = False
    return saved_result


def record_user_word_lookup(user_id: int, word: str) -> None:
    created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    save_user_word_history(user_id=user_id, word=word, created_at=created_at)


def read_user_word_history(user_id: int, limit: int = 50) -> list[dict]:
    return get_user_word_history(user_id=user_id, limit=limit)


def read_user_frequent_words(user_id: int, limit: int = 20) -> list[dict]:
    return get_user_frequent_words(user_id=user_id, limit=limit)
