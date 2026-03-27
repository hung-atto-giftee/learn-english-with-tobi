from fastapi import APIRouter, Depends

from app.auth.utils import get_current_user
from app.history.models import LearningHistoryResponse, LearningStatsResponse
from app.history.service import get_user_learning_history, get_user_learning_stats


router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=LearningHistoryResponse)
async def read_learning_history(
    current_user: dict = Depends(get_current_user),
) -> LearningHistoryResponse:
    history = get_user_learning_history(current_user["id"], limit=50)
    return LearningHistoryResponse(history=history)


@router.get("/stats", response_model=LearningStatsResponse)
async def read_learning_stats(
    current_user: dict = Depends(get_current_user),
) -> LearningStatsResponse:
    stats = get_user_learning_stats(current_user["id"])
    return LearningStatsResponse(**stats)
