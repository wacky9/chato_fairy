# When using transformers: set HF HUB cache to a local directory
# export HF_HUB_CACHE="/home/winstonbs/ai/chato_fairy/models"
# or rely on code below
import os
os.environ['HF_HUB_CACHE']='/home/winstonbs/ai/chato_fairy/models'
from transformers import AutoTokenizer, AutoModelForCausalLM

def setup():
    model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-32B-AWQ", torch_dtype="auto", device_map="cuda")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-32B-AWQ") 
    return (model, tokenizer)

def query_llm(message,llm):
    model, tokenizer = llm
    # Encode the message
    inputs = tokenizer(message, return_tensors="pt").to(model.device)
    result = model.generate(**inputs, max_new_tokens=50)
    # Decode the result
    return tokenizer.decode(result[0], skip_special_tokens=True)
