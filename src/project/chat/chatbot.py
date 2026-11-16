"""Interactive terminal chatbot backed by Google Gemini via LangChain."""

import os

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL_NAME = "gemini-3.5-flash-lite"
MAX_OUTPUT_TOKENS = 1024
MAX_HISTORY_MESSAGES = 20  # turns kept in context, excluding the system prompt
SYSTEM_PROMPT = "You are a helpful AI assistant. Respond clearly and concisely."
EXIT_COMMANDS = {"exit", "quit"}


def build_model() -> ChatGoogleGenerativeAI:
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit("GOOGLE_API_KEY not found. Add it to your .env file.")
    return ChatGoogleGenerativeAI(model=MODEL_NAME, max_output_tokens=MAX_OUTPUT_TOKENS)


def trim_history(history: list[BaseMessage]) -> list[BaseMessage]:
    """Keep the system prompt plus the most recent messages so context stays bounded."""
    system, rest = history[0], history[1:]
    return [system, *rest[-MAX_HISTORY_MESSAGES:]]


def run_chat() -> None:
    model = build_model()
    history: list[BaseMessage] = [SystemMessage(content=SYSTEM_PROMPT)]

    print("\nGemini Chatbot Started!")
    print("Type 'exit' or 'quit' to end.")

    while True:
        try:
            prompt = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not prompt:
            continue
        if prompt.lower() in EXIT_COMMANDS:
            print("Goodbye!")
            break

        history.append(HumanMessage(content=prompt))
        try:
            response = model.invoke(history)
        except Exception as error:
            history.pop()  # drop the unanswered prompt so history stays consistent
            print(f"Error: {error}")
            continue

        print(f"\nBot: {response.text}")
        history.append(response)
        history = trim_history(history)


if __name__ == "__main__":
    run_chat()
