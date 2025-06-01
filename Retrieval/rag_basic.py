from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from chromadb.api.types import EmbeddingFunction
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from rag_base import RAG

class ChromaEmbeddingsAdapter(Embeddings):
    def __init__(self, ef: EmbeddingFunction):
        self.ef = ef

    def embed_documents(self, texts):
        return self.ef(texts)

    def embed_query(self, query):
        return self.ef([query])[0]

class RAG_BASIC(RAG):
    def __init__(self):
        super().__init__()

    #Split the text
    def split(self,docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        splits = []
        for s in text_splitter.split_documents(docs):
            splits.append(s)
        return splits

    #Store in a vector database
    def store(self,chunks):
        vectorstore= Chroma.from_documents(
            documents=chunks,
            embedding=ChromaEmbeddingsAdapter(SentenceTransformerEmbeddingFunction(model_name=self.model)))
        return vectorstore.as_retriever(search_kwargs={"k": self.chunk_num})