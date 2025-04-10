from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

MSG = "How do tariffs influence the balance between protecting domestic industries and promoting international trade? In what ways can the imposition of tariffs impact global economic relationships and supply chains? What are the long-term effects of sustained tariff policies on national economic growth and consumer welfare?"

from langchain_core.embeddings import Embeddings
from chromadb.api.types import EmbeddingFunction
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


class ChromaEmbeddingsAdapter(Embeddings):
    def __init__(self, ef: EmbeddingFunction):
        self.ef = ef

    def embed_documents(self, texts):
        return self.ef(texts)

    def embed_query(self, query):
        return self.ef([query])[0]

#load file from data
def load():
    loader = DirectoryLoader('/app/data', glob='**/*.txt')
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
    vectorstore= Chroma.from_documents(
        documents=chunks,
        embedding=ChromaEmbeddingsAdapter(SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")))
    return vectorstore.as_retriever(search_kwargs={"k": 1})

#Query the vector database
def query(message, vectorstore):
    return vectorstore.invoke(message)

docs = load()
chunks = split(docs)
vectorstore = store(chunks)
print(query(MSG,vectorstore))