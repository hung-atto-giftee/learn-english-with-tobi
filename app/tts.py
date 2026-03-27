from enum import Enum
from pathlib import Path
from uuid import uuid4

import edge_tts


VOICE = "en-US-AriaNeural"
APP_DIR = Path(__file__).resolve().parent
AUDIO_DIR = APP_DIR / "voice_results"


class SpeechSpeed(str, Enum):
    normal = "normal"
    slow = "slow"


RATE_BY_SPEED: dict[SpeechSpeed, str] = {
    SpeechSpeed.normal: "+0%",
    SpeechSpeed.slow: "-20%",
}


def ensure_audio_dir() -> Path:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
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
