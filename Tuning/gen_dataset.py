#Generate dataset for embeddings
from llm_serve import setup, query_llm
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
import json
def synthetic_q(llm, chunk, prompt):
    message = f"{prompt}\n{chunk}\nQuestion:\n"
    return query_llm(message,llm)

def generate_dataset(): 
    SAMPLES = 5000
    llm = setup()
    file = open('config/synthetic_question.txt','r')
    prompt = file.read()
    file.close()
    # Get five random Documents
    loader = DirectoryLoader('my_dataset/data', glob='**/*.txt',sample_size=SAMPLES)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    splits = []
    for s in text_splitter.split_documents(docs):
        splits.append(s)
    json_array = []
    data_file = open('my_dataset/train/embedding.json',mode='w',buffering=1)
    failure = 0
    chunk_num = len(splits)
    for i in range(chunk_num):
        plus_chunk = splits[i].page_content
        #Get a chunk from a different file
        minus_chunk = splits[(chunk_num//2+i)%chunk_num].page_content
        #note: need to adjust this so it outputs just the question
        response = synthetic_q(llm,plus_chunk,prompt)
        question = response.split("Question:")[-1].strip()
        if not question:
            failure+=1
        obj = {"question":question,"plus":plus_chunk,"minus":minus_chunk}
        json_array.append(obj)
        # save intermediately in case of interruption
        if len(json_array) == 250:
            data_file.write(json.dumps(json_array, indent=4))
            json_array = []
    data_file.write(json.dumps(json_array, indent=4))
    print(failure)

def test_synth():
    setup_start = time.time()
    llm = setup()
    file = open('config/synthetic_question.txt','r')
    prompt = file.read()
    file.close()
    # Get five random Documents
    loader = DirectoryLoader('my_dataset/data', glob='**/*.txt',randomize_sample=True,sample_size=3)
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    splits = []
    for s in text_splitter.split_documents(docs):
        splits.append(s)
    index = 1
    setup_end = time.time()
    gen_start = time.time()
    for chunk in splits:
        print(f"Chunk: {index}\n")
        print(synthetic_q(llm,chunk,prompt))
        index+=1
    gen_end = time.time()
    print(f"Setup Time: {setup_end-setup_start}")
    print(f"Gen time: {gen_end-gen_start}")
    print(f"Questions generated: {index}")

generate_dataset()
