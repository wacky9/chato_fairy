# Evaluate the response of the AI model against the consensus of the experts in the IGM survey.
import json
import random
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
            AI = [0, 0, 0, 0, 0]
            AI[random.randint(0, 4)] = 1
            total_loss += loss(response, AI)
        print(f"Total loss for {n} evaluations: {total_loss}")
        return total_loss
    
evaluate(10)