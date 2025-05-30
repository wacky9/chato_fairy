from llm_serve import setup, query_llm
from Retrieval.rag_test import retrieve

# Load multiple prompts and append with appropriate instructions
def prepare_prompts():
    rag_prompts = []
    other_prompts = []
    with open('config/prompt_test.txt', 'r') as file:
        for line in file:
            rag_prompts.append(line.strip())
            other_prompts.append(line.strip())
    return (rag_prompts, other_prompts)

# compare prompt output using and not using RAG
def rag_compare():
    print("Loading prompts and instructions...")
    rag,other = prepare_prompts()
    file = open('config/instruction_rag.txt', 'r')
    rag_instruction = file.read()
    file.close()
    file = open('config/instruction_no_rag.txt', 'r')
    other_instruction = file.read()
    file.close()
    print("Setting up LLM...")
    llm = setup()
    print("Comparing responses...")
    for p in range(len(rag)):
        rag_prompt = rag[p]
        other_prompt = other[p]
        retrieved_docs = retrieve(rag_prompt)
        rag_message = f"{rag_instruction}\n\n{retrieved_docs}\n\nprompt:\n{rag_prompt}"
        other_message = f"{other_instruction}\n\nprompt:\n{other_prompt}"
        rag_response = query_llm(rag_message, llm)
        other_response = query_llm(other_message, llm)
        print(f"RAG Response for prompt {p+1}:\n{rag_response}\n")
        print(f"Non-RAG Response for prompt {p+1}:\n{other_response}\n")

rag_compare()