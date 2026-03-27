from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.utils import get_current_user
from app.dictionary.service import (
    list_words,
    lookup_word,
    normalize_word,
    read_user_frequent_words,
    read_user_word_history,
    record_user_word_lookup,
)


router = APIRouter(prefix="/dictionary", tags=["dictionary"])


@router.get("/list")
async def get_dictionary_list(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50),
    search: str = Query("", min_length=0),
    start_date: str = Query("", min_length=0),
    end_date: str = Query("", min_length=0),
    current_user: dict = Depends(get_current_user),
) -> dict:
    return list_words(
        page=page,
        limit=limit,
        search=search,
        start_date=start_date,
        end_date=end_date,
    )


@router.get("")
async def get_dictionary_entry(
    word: str = Query(..., min_length=1),
    current_user: dict = Depends(get_current_user),
) -> dict:
    normalized_word = normalize_word(word)
    if not normalized_word:
        raise HTTPException(status_code=400, detail="Word is not valid.")

    result = await lookup_word(normalized_word)
    record_user_word_lookup(current_user["id"], normalized_word)
    return result


@router.get("/words/history")
async def get_words_history(
    current_user: dict = Depends(get_current_user),
) -> dict:
    history = read_user_word_history(current_user["id"], limit=50)
    return {"history": history}


@router.get("/words/frequent")
async def get_frequent_words(
    current_user: dict = Depends(get_current_user),
) -> dict:
    words = read_user_frequent_words(current_user["id"], limit=20)
    return {"words": words}
