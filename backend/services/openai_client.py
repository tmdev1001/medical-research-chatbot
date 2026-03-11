from typing import Optional

from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from backend.config import get_settings

_settings = get_settings()


def get_embedding_client(model: Optional[str] = None) -> OpenAIEmbeddings:
    """
    Returns a LangChain embedding client configured with OpenAI.
    """
    embedding_model = model or _settings.embedding_model
    return OpenAIEmbeddings(
        model=embedding_model,
        api_key=_settings.openai_api_key,
    )


def get_chat_client(
    model: Optional[str] = None,
    temperature: float = 0.0,
) -> ChatOpenAI:
    """
    Returns a LangChain ChatOpenAI client for LLM calls.
    """
    model_name = model or _settings.model_name
    return ChatOpenAI(
        model=model_name,
        api_key=_settings.openai_api_key,
        temperature=temperature,
    )

