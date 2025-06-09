# Same as RAG basic but with a fine-tuned embedding model
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from chromadb.api.types import EmbeddingFunction
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from Retrieval.rag_base import RAG
from sentence_transformers import SentenceTransformer

class ChromaEmbeddingsAdapter(Embeddings):
    def __init__(self, ef: EmbeddingFunction):
        self.ef = ef

    def embed_documents(self, texts):
        return self.ef(texts)

    def embed_query(self, query):
        return self.ef([query])[0]

class RAG_FT(RAG):
    def __init__(self):
        super().__init__()
        self.model = "Qwen/Qwen3-Embedding-4B"
        

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
    def store(self,chunks,cache):
        if cache:
            vectorstore = Chroma(collection_name="ft_vs", persist_directory='my_dataset/vectorstor/ft', embedding_function=ChromaEmbeddingsAdapter(SentenceTransformerEmbeddingFunction(model_name=self.model)))
        else:
            vectorstore = Chroma.from_documents(
                collection_name="ft_vs",
                documents=chunks,
                embedding=ChromaEmbeddingsAdapter(SentenceTransformerEmbeddingFunction(model_name=self.model, normalize_embeddings=True, device="cuda", model_kwargs={"torch_dtype": "float16"})),
                persist_directory='my_dataset/vectorstore/ft' 
                )
        return vectorstore.as_retriever(search_kwargs={"k": self.chunk_num})