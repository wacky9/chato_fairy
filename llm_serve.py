#For now, use Python to query the LLM and return the response.
from litgpt import LLM
# When using transformers: set HF HUB cache to a local directory
# export HF_HUB_CACHE="/home/winstonbs/ai/chato_fairy/models"
from transformers import AutoTokenizer, AutoModelForCausalLM
def setup():
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-14B-Instruct", torch_dtype="auto", device_map="cuda")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-14B-Instruct") 
    return (model, tokenizer)

def query_llm(message,llm):
    model, tokenizer = llm
    # Encode the message
    inputs = tokenizer(message, return_tensors="pt").to(model.device)
    result = model.generate(**inputs, max_new_tokens=500)
    # Decode the result
    return tokenizer.decode(result[0], skip_special_tokens=True)
