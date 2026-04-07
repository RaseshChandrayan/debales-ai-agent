from scraper import crawl_site
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DB_DIR = "./chroma_db"
START_URL = "https://debales.ai"


def main():
    print("[INFO] Scraping...")
    docs = crawl_site(START_URL, max_pages=15)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []
    for doc in docs:
        for chunk in splitter.split_text(doc["content"]):
            chunks.append({
                "content": chunk,
                "metadata": doc["metadata"]
            })

    print(f"[INFO] Chunks: {len(chunks)}")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    db = Chroma.from_texts(
        texts=[c["content"] for c in chunks],
        embedding=embeddings,
        metadatas=[c["metadata"] for c in chunks],
        persist_directory=DB_DIR
    )

    db.persist()
    print("[INFO] Vector DB ready!")


if __name__ == "__main__":
    main()