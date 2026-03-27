from app.auth.routes import router as auth_router
from app.database import init_db
from app.dictionary.routes import router as dictionary_router
from app.dictionary.service import init_dictionary_cache
from app.history.routes import router as history_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.routes.training import router as training_router
from app.tts import AUDIO_DIR, ensure_audio_dir


def create_app() -> FastAPI:
    ensure_audio_dir()
    init_db()
    init_dictionary_cache()

    app = FastAPI(
        title="English Listening Trainer API",
        version="1.0.0",
        description="FastAPI backend for English listening and dictation practice.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount("/static/audio", StaticFiles(directory=AUDIO_DIR), name="audio")
    app.include_router(auth_router)
    app.include_router(dictionary_router)
    app.include_router(history_router)
    app.include_router(training_router)

    @app.get("/health")
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
