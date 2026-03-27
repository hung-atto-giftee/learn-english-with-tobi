from pydantic import BaseModel


class LearningHistoryItem(BaseModel):
    id: int
    user_id: int
    sentence: str
    user_input: str
    accuracy: float
    created_at: str


class LearningHistoryResponse(BaseModel):
    history: list[LearningHistoryItem]


class AccuracyTrendItem(BaseModel):
    created_at: str
    accuracy: float


class LearningStatsResponse(BaseModel):
    average_accuracy: float
    total_sentences_practiced: int
    accuracy_trend: list[AccuracyTrendItem]
