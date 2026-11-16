"""Turn a raw paragraph about a movie into a validated MovieInfo."""

from functools import cache

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

from project.config.settings import MODEL_NAME, require_env
from project.schemas.movie import MovieInfo

PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You extract structured information about movies from raw text. "
            "Only use facts stated in the text: if a detail is not mentioned, use null "
            "or an empty list. Do not invent facts. Also write a clean 2-3 sentence summary.",
        ),
        ("human", "{paragraph}"),
    ]
)


@cache
def _chain() -> Runnable:
    require_env("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME)
    return PROMPT | llm.with_structured_output(MovieInfo)


def extract_movie_info(paragraph: str) -> MovieInfo:
    return _chain().invoke({"paragraph": paragraph})
