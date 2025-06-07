# Evaluate the response of the AI model against the consensus of the experts in the IGM survey.
import json
import random
from llm_serve import setup, query_llm


# Two arrays of 5 variables. AI array has one 1 and 4 0s. 
def loss(experts, AI):
    consensus = experts.index(max(experts))
    ai_choice = AI.index(max(AI))
    # (1-a)^2 * (i-g)^2 * b
    return (1-experts[ai_choice]/100)** 2 * (consensus-ai_choice)**2 * experts[consensus]/100

def load_evaluation():
    file = open("my_dataset/eval_data/igm_survey.json", "r")
    data = json.load(file)
    file.close()
    return data

def evaluate(n=10):
    llm = setup()
    # evaluate all the responses in the dataset
    if n <=0:
        pass
    # evaluate n random responses
    else:
        data = load_evaluation()
        total_loss = 0
        indices = random.sample(range(len(data)), n)
        data = [data[i] for i in indices]
        for i in range(n):
            # get question
            experts = data[i]
            question = experts["question"]
            response = experts["weighted"]
            # Get AI response
            AI = base_response(llm,question)
            total_loss += loss(response, AI)
        print(f"Total loss for {n} evaluations: {total_loss}")
        return total_loss

response_dict = {
    "Strongly Agree": [1, 0, 0, 0, 0],
    "Agree": [0, 1, 0, 0, 0],
    "Uncertain": [0, 0, 1, 0, 0],
    "Disagree": [0, 0, 0, 1, 0],
    "Strongly Disagree": [0, 0, 0, 0, 1]
}
def base_response(llm,question):
    file = open('config/eval_prompt.txt', 'r')
    prompt = file.read()
    file.close()
    prompt += '\n' + question + '\nResponse:\n'
    return get_response(llm, prompt)

def rag_response(llm,question):
    pass

def get_response(llm,msg):
    reply = query_llm(msg, llm)
    #remove the prompt from the reply
    reply = reply.split("Response:")[-1].strip()
    #Get first line of the reply
    reply = reply.split("\n")[0]
    reply = reply.strip()
    if reply in response_dict:
        return response_dict[reply]
    else:
        print(f"Unknown response: {reply}")
        return [1, 1, 1, 1, 1]

evaluate(10)