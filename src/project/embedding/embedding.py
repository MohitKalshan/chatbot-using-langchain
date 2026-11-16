from langchain.embeddings import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

texts = ["Hello world", "How are you?"]
vector_embeddings = embeddings.embed_documents(texts)

print("Vector embeddings:", vector_embeddings)