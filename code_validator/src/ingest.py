# src/ingest.py

from pathlib import Path
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embeddings import CodeEmbeddings
import os

class CodeIngestor:
    def __init__(self, data_dir="../data/c_samples"):
        self.data_dir = Path(data_dir)
        self.embedder = CodeEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ";", "{", "}", " ", ""]
        )

    def load_documents(self):
        """Load all C files from the data directory"""
        documents = []
        for file_path in self.data_dir.glob("**/*.c"):
            try:
                loader = TextLoader(str(file_path))
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        return documents

    def process_and_store(self, save_path="vectorstore.faiss"):
        """Process documents and create vector store"""
        # Load documents
        documents = self.load_documents()
        if not documents:
            raise ValueError("No documents found in the specified directory")

        # Create vector store
        vector_store = self.embedder.create_vector_store(documents)
        
        # Save the vector store
        vector_store.save_local(save_path)
        print(f"Processed {len(documents)} documents and saved vector store to {save_path}")
        return vector_store

def main():
    ingestor = CodeIngestor()
    ingestor.process_and_store()

if __name__ == "__main__":
    main()
