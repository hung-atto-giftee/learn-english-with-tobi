import asyncio
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.auth.utils import get_current_user
from app.evaluator import evaluate_sentence
from app.history.service import save_learning_history
from app.tts import (
    SpeechSpeed,
    generate_audio_file,
    generate_word_audio_file,
    normalize_word_audio_key,
)


router = APIRouter(tags=["training"])


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1)
    speed: SpeechSpeed


class PracticeRequest(BaseModel):
    sentence: str = Field(..., min_length=1)


class EvaluateRequest(BaseModel):
    sentence: str = Field(..., min_length=1)
    user_input: str


def build_audio_url(request: Request, audio_path: Path) -> str:
    base_url = str(request.base_url).rstrip("/")
    return f"{base_url}/static/audio/{audio_path.name}"


def build_nested_audio_url(request: Request, audio_path: Path) -> str:
    base_url = str(request.base_url).rstrip("/")
    relative_path = audio_path.relative_to(audio_path.parents[1]).as_posix()
    return f"{base_url}/static/audio/{relative_path}"


@router.post("/tts")
async def create_tts_audio(payload: TTSRequest) -> FileResponse:
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    audio_path = await generate_audio_file(text, payload.speed)
    return FileResponse(
        path=audio_path,
        media_type="audio/mpeg",
        filename=audio_path.name,
    )


@router.get("/tts/word")
async def create_word_audio(
    word: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
) -> dict[str, str]:
    normalized_word = normalize_word_audio_key(word)
    if not normalized_word:
        raise HTTPException(status_code=400, detail="Word is not valid.")

    audio_path = await generate_word_audio_file(normalized_word)
    relative_url = f"/static/audio/{audio_path.relative_to(audio_path.parents[1]).as_posix()}"
    return {
        "audio_url": relative_url,
        "absolute_audio_url": build_nested_audio_url(request, audio_path),
    }


@router.post("/practice")
async def create_practice_audio(
    payload: PracticeRequest,
    request: Request,
    current_user: dict = Depends(get_current_user),
) -> dict:
    sentence = payload.sentence.strip()
    if not sentence:
        raise HTTPException(status_code=400, detail="Sentence cannot be empty.")

    audio_normal, audio_slow = await asyncio.gather(
        generate_audio_file(sentence, SpeechSpeed.normal),
        generate_audio_file(sentence, SpeechSpeed.slow),
    )

    return {
        "sentence": sentence,
        "audio_normal_url": build_audio_url(request, audio_normal),
        "audio_slow_url": build_audio_url(request, audio_slow),
    }


@router.post("/evaluate")
async def evaluate_practice(
    payload: EvaluateRequest,
    current_user: dict = Depends(get_current_user),
) -> dict:
    sentence = payload.sentence.strip()
    if not sentence:
        raise HTTPException(status_code=400, detail="Sentence cannot be empty.")

    result = evaluate_sentence(sentence, payload.user_input.strip())
    save_learning_history(
        user_id=current_user["id"],
        sentence=sentence,
        user_input=payload.user_input.strip(),
        accuracy=result["accuracy"],
    )
    return result
