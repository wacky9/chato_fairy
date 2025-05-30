from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.embeddings import Embeddings
from chromadb.api.types import EmbeddingFunction
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever

class ChromaEmbeddingsAdapter(Embeddings):
    def __init__(self, ef: EmbeddingFunction):
        self.ef = ef

    def embed_documents(self, texts):
        return self.ef(texts)

    def embed_query(self, query):
        return self.ef([query])[0]

#load file from data
def load():
    loader = DirectoryLoader('my_dataset/data', glob='**/*.txt')
    docs = loader.load()
    return docs

#Split the text
def split(docs):
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
def store(chunks):
    k = 5
    vectorstore= Chroma.from_documents(
        documents=chunks,
        embedding=ChromaEmbeddingsAdapter(SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")))
    v_retriever = vectorstore.as_retriever(search_kwargs={"k": k})
     # Create BM25Retriever from the documents
    bm25_retriever = BM25Retriever.from_documents(documents=chunks, k=k)
    # Ensemble the retrievers using Langchain’s EnsembleRetriever Object
    ensemble_retriever = EnsembleRetriever(retrievers=[v_retriever, bm25_retriever], weights=[0.5, 0.5])
    return ensemble_retriever

#Query the vector database
def query(message, vectorstore):
    docs = vectorstore.invoke(message)
    return "\n".join([doc.page_content for doc in docs])

# Create persistent vector database
def create():
    docs = load()
    chunks = split(docs)
    vectorstore = store(chunks)
    return vectorstore

def retrieve(message, db):
    return query(message, db)