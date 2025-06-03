from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from chromadb.api.types import EmbeddingFunction
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from Retrieval.rag_base import RAG
class ChromaEmbeddingsAdapter(Embeddings):
    def __init__(self, ef: EmbeddingFunction):
        self.ef = ef

    def embed_documents(self, texts):
        return self.ef(texts)

    def embed_query(self, query):
        return self.ef([query])[0]
    
class RAG_HYBRID(RAG):
    def __init__(self):
        super().__init__()
    
    # Split the text
    def split(self, docs):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        splits = []
        for s in text_splitter.split_documents(docs):
            splits.append(s)
        return splits
    
    # Store in a vector database    
    def store(self, chunks):
        k = self.chunk_num
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=ChromaEmbeddingsAdapter(SentenceTransformerEmbeddingFunction(model_name=self.model)))
        v_retriever = vectorstore.as_retriever(search_kwargs={"k": k})
        
        # Create BM25Retriever from the documents
        bm25_retriever = BM25Retriever.from_documents(documents=chunks, k=k)
        
        # Ensemble the retrievers using Langchain’s EnsembleRetriever Object
        ensemble_retriever = EnsembleRetriever(retrievers=[v_retriever, bm25_retriever], weights=[0.5, 0.5])
        return ensemble_retriever