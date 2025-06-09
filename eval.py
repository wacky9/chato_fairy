# Evaluate the response of the AI model against the consensus of the experts in the IGM survey.
import json
import random
from llm_serve import setup, query_llm
from collections import Counter
from Retrieval.rag_basic import RAG_BASIC

agent = RAG_BASIC()
agent.create()
# Two arrays of 5 variables. AI array has one 1 and 4 0s. 
def loss(experts, AI):
    # if there's an error, pretend loss is 0
    if AI == [1,1,1,1,1]:
        return 0.0
    #Choice made by the experts
    consensus = experts.index(max(experts))
    #Choice made by the AI
    ai_choice = AI.index(max(AI))
    # (1-a)^2 * (i-g)^2 * b
    return (1-experts[ai_choice]/100)** 2 * (consensus-ai_choice)**2 * experts[consensus]/100

def load_evaluation():
    file = open("my_dataset/eval_data/igm_survey.json", "r")
    data = json.load(file)
    file.close()
    return data

# Survey has 1024 questions
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
        accurate = 0
        for i in range(n):
            # get question
            experts = data[i]
            question = experts["question"]
            response = experts["weighted"]
            # Get AI response
            AI = base_response(llm,question)
            l = loss(response,AI)
            # Check if AI gets it correct
            if l < 0.001:
                accurate+=1
            total_loss += l
        print(f"Total loss for {n} evaluations: {total_loss}\n")
        print(f"Accuracy: {accurate/n * 100}%")
        return total_loss  

# Check if the AI gives consistent responses to the same questions
def consistency(n=10):
    llm = setup()
    data = load_evaluation()
    indices = random.sample(range(len(data)), n)
    data = [data[i] for i in indices]
    all_responses = []
    for i in range(n):
        single_question = []
        question = data[i]['question']
        #Check each question 20 times
        for k in range(20):
            # Get AI response
            AI = rag_response(llm,question)
            single_question.append(AI.index(1))
        all_responses.append(single_question)
    accuracy = []
    for answers in all_responses:
        occurrences = Counter(answers)
        accuracy.append(occurrences.most_common(1)[0][1]/len(answers))
    return accuracy
      
    
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
    retrieved_docs = agent.query(question)
    file = open('config/eval_prompt.txt', 'r')
    prompt = file.read()
    file.close()
    message = f"{prompt} \n{question}\nContext:\n{retrieved_docs}\nResponse:\n"
    return get_response(llm,message)

def get_response(llm,msg):
    reply = query_llm(msg, llm)
    #remove the prompt from the reply
    response = reply.split("Response:")[-1].strip()
    #Get first line of the reply
    response = response.split("\n")[0]
    response = response.strip()
    response = response.strip('.,!')
    if response in response_dict:
        return response_dict[response]
    else:
        print(f"Unknown response: {response}")
        return [1, 1, 1, 1, 1]

evaluate(100)


#c = consistency(50)
#print(f"Consistency: {c}")
#avg_c = sum(c)/len(c)
#print(f"\nAverage Consistency: {avg_c}")