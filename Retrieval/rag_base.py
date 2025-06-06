from abc import ABC, abstractmethod
from langchain_community.document_loaders import DirectoryLoader
import time
class RAG(ABC):
    def __init__(self):
        self.vs = None
        self.chunk_num = 5 # Default number of chunks to retrieve
        self.model = "all-MiniLM-L6-v2" # Default model for embeddings
        pass

    def load(self):
        loader = DirectoryLoader('my_dataset/data', glob='**/*.txt')
        docs = loader.load()
        return docs

    @abstractmethod
    def split(self, docs) -> list:
        pass

    @abstractmethod
    def store(self, chunks,cache):
        pass

    def query(self, message):
        docs = self.vs.invoke(message)
        a = ""
        for i in range(len(docs)):
            a += f"Document {i+1}:\n{docs[i].page_content}\n\n"
        return a

    # Create persistent vector database
    def create(self, cache=True):
        if cache:
            self.vs = self.store([], cache=True)
        else:
            docs = self.load()
            chunks = self.split(docs)
            vectorstore = self.store(chunks)
            self.vs = vectorstore
    
    #version of create with benchmarking
    def create_bm(self):
        doc_start = time.time()
        docs = self.load()
        doc_end = time.time()
        print(f"Document loading time: {doc_end - doc_start:.2f} seconds")
        split_start = time.time()
        chunks = self.split(docs)
        split_end = time.time()
        print(f"Document splitting time: {split_end - split_start:.2f} seconds")
        store_start = time.time()
        vectorstore = self.store(chunks)
        store_end = time.time()
        print(f"Vector store creation time: {store_end - store_start:.2f} seconds")
        self.vs = vectorstore