# app/core/rag_pipeline.py
import os
from pathlib import Path

from langchain_anthropic import ChatAnthropic
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain_core.documents import Document
from pinecone import Pinecone

# ─── Pinecone client (v6) ─────────────────────────────────────
# In v6, api_key is passed directly to Pinecone()
# Index is accessed via pc.Index(host=...) using the host from your .env
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(host=os.getenv("PINECONE_HOST"))

# ─── Models ───────────────────────────────────────────────────
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0.3,   # Lower temp for factual beauty advice
    max_tokens=1024,
)

# ─── Chunking strategy ────────────────────────────────────────
# chunk_size=500: fits one product description comfortably
# chunk_overlap=50: prevents ingredient lists from being split across chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " "],
)

# ─── Vector store ─────────────────────────────────────────────
_vectorstore: PineconeVectorStore | None = None


def build_vectorstore(documents: list[Document]) -> PineconeVectorStore:
    """
    Chunk documents, embed them, and upsert into Pinecone.
    Call this once at startup after loading the knowledge base.
    """
    global _vectorstore
    chunks = splitter.split_documents(documents)
    _vectorstore = PineconeVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=os.getenv("PINECONE_INDEX_NAME", "maison-beatute-project"),
    )
    print(f"✅ Pinecone vector store built — {len(chunks)} chunks upserted")
    return _vectorstore


def get_vectorstore() -> PineconeVectorStore:
    """
    Return the existing Pinecone vector store.
    If build_vectorstore() hasn't been called yet, connects to the
    existing index directly (useful if data was already upserted).
    """
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = PineconeVectorStore(
            index=index,
            embedding=embeddings,
        )
        print("✅ Connected to existing Pinecone index")
    return _vectorstore


def build_rag_chain() -> ConversationalRetrievalChain:
    """
    Build and return a ConversationalRetrievalChain over the Pinecone index.
    Can be called with or without build_vectorstore() — connects to
    the existing index if already populated.
    """
    retriever = get_vectorstore().as_retriever(
        search_kwargs={"k": 4}  # Retrieve 4 most relevant chunks per query
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        verbose=False,
    )


def load_knowledge_base(data_dir: str = "data") -> list[Document]:
    """
    Load product catalogue and FAQ/policy files from the data/ directory.
    Returns a list of LangChain Document objects ready for chunking.
    """
    documents = []
    data_path = Path(data_dir)

    for file in data_path.glob("*.md"):
        text = file.read_text(encoding="utf-8")
        documents.append(Document(page_content=text, metadata={"source": file.name}))
        print(f"  Loaded: {file.name}")

    if not documents:
        print("⚠️  No .md files found in data/. Add knowledge base files to populate Pinecone.")

    return documents