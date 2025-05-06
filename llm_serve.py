#For now, use Python to query the LLM and return the response.
from litgpt import LLM
llm = None

def setup():
    global llm
    llm = LLM.load("meta-llama/Meta-Llama-3-8B-Instruct")

def query_llm(message):
    text = llm.generate(message)
    return text