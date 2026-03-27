from enum import Enum
from pathlib import Path
import re
from uuid import uuid4

import edge_tts


VOICE = "en-US-AriaNeural"
APP_DIR = Path(__file__).resolve().parent
AUDIO_DIR = APP_DIR / "voice_results"
WORD_AUDIO_DIR = AUDIO_DIR / "words"
WORD_FILENAME_PATTERN = re.compile(r"[a-z0-9]+")


class SpeechSpeed(str, Enum):
    normal = "normal"
    slow = "slow"


RATE_BY_SPEED: dict[SpeechSpeed, str] = {
    SpeechSpeed.normal: "+0%",
    SpeechSpeed.slow: "-20%",
}


def ensure_audio_dir() -> Path:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    WORD_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    return AUDIO_DIR


async def generate_audio_file(text: str, speed: SpeechSpeed) -> Path:
    ensure_audio_dir()
    filename = f"{uuid4().hex}_{speed.value}.mp3"
    output_path = AUDIO_DIR / filename
    communicator = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE_BY_SPEED[speed],
    )
    await communicator.save(str(output_path))
    return output_path


def normalize_word_audio_key(word: str) -> str:
    return "".join(WORD_FILENAME_PATTERN.findall(word.lower()))


async def generate_word_audio_file(word: str) -> Path:
    normalized_word = normalize_word_audio_key(word)
    if not normalized_word:
        raise ValueError("Word is not valid.")

    ensure_audio_dir()
    output_path = WORD_AUDIO_DIR / f"{normalized_word}.mp3"
    if output_path.exists():
        return output_path

    communicator = edge_tts.Communicate(
        text=normalized_word,
        voice=VOICE,
        rate=RATE_BY_SPEED[SpeechSpeed.normal],
    )
    await communicator.save(str(output_path))
    return output_path
