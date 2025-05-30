from llm_serve import setup, query_llm
from Retrieval.hybrid_rag import create, retrieve
print("Loading instruction and prompt...")
#Load instruction and prompt
file = open('config/instruction_rag.txt', 'r')
instruction = file.read()
file.close()
file = open('config/prompt.txt', 'r')
prompt = file.read()
file.close()
print("Processing")
#Retrieve information
#cut off first line of prompt to get the user query
user_query = prompt.split('\n', 1)[1].strip()
print("Creating vector database")
db = create()
retrieved_docs = retrieve(user_query, db)
print(retrieved_docs)
message = f"{instruction}\n\n{retrieved_docs}\n\n{prompt}"
print("Setting up LLM")
#setup llm
llm = setup()
#Query the LLM
response = query_llm(message,llm)
#Print the response
print(response)
