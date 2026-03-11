from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.rag.pipeline import RAGPipeline

router = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(..., description="User's research question.")


class SourceChunk(BaseModel):
    label: str
    text: str
    metadata: Dict[str, Any]


class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceChunk]


_pipeline: RAGPipeline | None = None


def get_pipeline() -> RAGPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline()
    return _pipeline


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Ask a clinical research question",
)
def chat_endpoint(
    payload: ChatRequest,
    pipeline: RAGPipeline = Depends(get_pipeline),
) -> ChatResponse:
    if not payload.question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question must not be empty.",
        )

    try:
        result = pipeline.answer_question(payload.question)
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {e}",
        )

    sources = [SourceChunk(**src) for src in result.get("sources", [])]

    return ChatResponse(
        answer=result.get("answer", ""),
        sources=sources,
    )

