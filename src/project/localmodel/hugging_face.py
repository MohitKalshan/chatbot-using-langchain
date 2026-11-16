from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    task="text-generation",
    model_kwargs={
        "temperature": 0.7, 
        "max_new_tokens": 150
    },
)
chat_model = ChatHuggingFace(llm=llm)

chat_model.invoke("What is the capital of France?")