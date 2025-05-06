from llm_serve import setup, query_llm
from Retrieval.rag_test import retrieve
#Load instruction and prompt
file = open('instruction.txt', 'r')
instruction = file.read()
file.close()
file = open('prompt.txt', 'r')
prompt = file.read()
file.close()

#setup llm
setup()
#Retrieve information
#cut off first line of prompt to get the user query
user_query = prompt.split('\n', 1)[1].strip()
retrieved_docs = retrieve(user_query)
message = f"{instruction}\n\n{retrieved_docs}\n\n{prompt}"
#Query the LLM
response = query_llm(message)
#Print the response
print(response)
