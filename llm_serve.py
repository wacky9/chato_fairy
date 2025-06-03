#For now, use Python to query the LLM and return the response.
from litgpt import LLM

def setup():
    return LLM.load("Qwen/Qwen2.5-14B-Instruct")

def query_llm(message,llm):
    return llm.generate(message,max_new_tokens=500)
