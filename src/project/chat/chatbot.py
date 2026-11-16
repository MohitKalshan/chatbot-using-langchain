"""Interactive terminal chatbot backed by Google Gemini via LangChain."""

import os

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from langchain_google_genai import ChatGoogleGenerativeAI

MODEL_NAME = "gemini-3.5-flash-lite"
MAX_OUTPUT_TOKENS = 1024
MAX_HISTORY_MESSAGES = 20  # past messages kept in context
SYSTEM_PROMPT = "You are a helpful AI assistant. Respond clearly and concisely."
EXIT_COMMANDS = {"exit", "quit"}

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)


def build_chain() -> Runnable:
    load_dotenv()
    if not os.getenv("GOOGLE_API_KEY"):
        raise SystemExit("GOOGLE_API_KEY not found. Add it to your .env file.")
    model = ChatGoogleGenerativeAI(model=MODEL_NAME, max_output_tokens=MAX_OUTPUT_TOKENS)
    return PROMPT | model


def run_chat() -> None:
    chain = build_chain()
    history: list[BaseMessage] = []

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

        try:
            response = chain.invoke({"history": history, "input": prompt})
        except Exception as error:
            print(f"Error: {error}")
            continue

        print(f"\nBot: {response.text}")
        history.extend([HumanMessage(content=prompt), response])
        history = history[-MAX_HISTORY_MESSAGES:]


if __name__ == "__main__":
    run_chat()
