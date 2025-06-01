from abc import ABC, abstractmethod
from langchain_community.document_loaders import DirectoryLoader

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
    def store(self, chunks):
        pass

    def query(self, message):
        docs = self.vs.invoke(message)
        return "\n".join([doc.page_content for doc in docs])

    # Create persistent vector database
    def create(self):
        docs = self.load()
        chunks = self.split(docs)
        vectorstore = self.store(chunks)
        self.vs = vectorstore