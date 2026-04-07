from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_DIR = "./chroma_db"

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 3})


def rag_tool(query: str) -> str:
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant Debales AI information found."

    result = []
    for doc in docs:
        result.append(f"Source: {doc.metadata['source']}\n{doc.page_content}")

    return "\n\n".join(result)