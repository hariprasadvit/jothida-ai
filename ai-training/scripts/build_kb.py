"""
Build Knowledge Base for Tamil Astrology RAG
"""

import os
import json
from pathlib import Path
from typing import List, Dict

# Uncomment when running:
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.vectorstores import Chroma
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.document_loaders import TextLoader, JSONLoader

# Configuration
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
PERSIST_DIR = "./data/embeddings/chroma_db"


def load_documents(data_dir: str) -> List[Dict]:
    """Load all documents from data directory"""
    documents = []
    data_path = Path(data_dir)
    
    # Load text files
    for txt_file in data_path.glob("**/*.txt"):
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append({
                "content": content,
                "source": str(txt_file),
                "type": "text"
            })
    
    # Load JSON files (Q&A pairs)
    for json_file in data_path.glob("**/*.json"):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    documents.append({
                        "content": f"Q: {item.get('question', '')}\nA: {item.get('answer', '')}",
                        "source": str(json_file),
                        "type": "qa"
                    })
    
    return documents


def chunk_documents(documents: List[Dict], chunk_size: int, overlap: int) -> List[Dict]:
    """Split documents into chunks"""
    chunks = []
    
    for doc in documents:
        content = doc["content"]
        
        # Simple chunking (replace with RecursiveCharacterTextSplitter in production)
        words = content.split()
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append({
                "content": chunk_text,
                "source": doc["source"],
                "type": doc["type"]
            })
    
    return chunks


def build_vectorstore(chunks: List[Dict], persist_dir: str):
    """Build and persist ChromaDB vectorstore"""
    print(f"Building vectorstore with {len(chunks)} chunks...")
    
    # In production, uncomment:
    # embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    # 
    # texts = [c["content"] for c in chunks]
    # metadatas = [{"source": c["source"], "type": c["type"]} for c in chunks]
    # 
    # vectorstore = Chroma.from_texts(
    #     texts=texts,
    #     embedding=embeddings,
    #     metadatas=metadatas,
    #     persist_directory=persist_dir
    # )
    # 
    # vectorstore.persist()
    # print(f"Vectorstore saved to {persist_dir}")
    
    print("(Dry run - uncomment ChromaDB code to actually build)")


def main():
    """Main function to build knowledge base"""
    print("=" * 50)
    print("Building Tamil Astrology Knowledge Base")
    print("=" * 50)
    
    # Load documents
    print("\n1. Loading documents...")
    documents = load_documents("./data/raw")
    print(f"   Loaded {len(documents)} documents")
    
    # Chunk documents
    print("\n2. Chunking documents...")
    chunks = chunk_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    print(f"   Created {len(chunks)} chunks")
    
    # Build vectorstore
    print("\n3. Building vectorstore...")
    build_vectorstore(chunks, PERSIST_DIR)
    
    print("\n" + "=" * 50)
    print("Knowledge base build complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
