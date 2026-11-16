"""Factory for the chat model used across the project."""

from langchain_google_genai import ChatGoogleGenerativeAI

from project.config.settings import MODEL_NAME, require_env


def get_llm(max_output_tokens: int = 1024) -> ChatGoogleGenerativeAI:
    require_env("GOOGLE_API_KEY")
    return ChatGoogleGenerativeAI(model=MODEL_NAME, max_output_tokens=max_output_tokens)
