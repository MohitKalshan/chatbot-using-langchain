"""Interactive terminal chatbot with conversation memory."""

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from project.cli import prompt_loop
from project.config.llm import get_llm

MAX_HISTORY_MESSAGES = 20  # past messages kept in context
SYSTEM_PROMPT = "You are a helpful AI assistant. Respond clearly and concisely."

PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{input}"),
    ]
)


def run_chat() -> None:
    chain = PROMPT | get_llm()
    history: list[BaseMessage] = []

    print("\nGemini Chatbot Started!")
    print("Type 'exit' or 'quit' to end.")

    for prompt in prompt_loop("\nYou: "):
        try:
            response = chain.invoke({"history": history, "input": prompt})
        except Exception as error:
            print(f"Error: {error}")
            continue

        print(f"\nBot: {response.text}")
        history.extend([HumanMessage(content=prompt), AIMessage(content=response.text)])
        history = history[-MAX_HISTORY_MESSAGES:]


if __name__ == "__main__":
    run_chat()
