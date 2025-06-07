# chato_fairy
The Chato Fairy is an LLM application designed to work specifically on economic issues. This application can summarize economic research, accurately answer economic questions, and otherwise assist in economic endeavors.

# Why Chato Fairy
There is a growing need for LLMs that are focused on and capable of assisting users in working with complex subjects. Economics is a field ripe for such an application. Economics is a deep and wide field where most people have little-to-no expertise. Nevertheless, these people are regularly asked to engage in difficult decisions where knowledge of economics would be quite useful. For example, Burke and Manz (2014) identify a link between economic literacy and more accurate inflation expectations. Households having more accurate inflation expectations would improve their budgeting and prevent nasty surprises. 

For ordinary individuals and most businesses, reading economic research and studying economics is a prohibitively difficult task. Hiring an economist to advise you is likewise expensive. Thus there is a need to provide good information about economics without requiring years of study. Hence, LLMs. [Recent news](https://garymarcus.substack.com/p/did-an-llm-help-write-trumps-trade) has shown that people already use LLMs to alleviate this gap in knowledge and underscores the importance of having LLMs provide up-to-date, accurate information about economic subjects.

# Technical details
Chato Fairy is composed of three important sections. First is a custom dataset of high-quality information about economics. Second is an LLM fine-tuned on a modified version of this dataset. Third is a RAG component using this dataset. The entire project is inside a Docker Container and designed to run locally with no online or external dependencies.

## Dataset
There are some currently existing LLM datasets for economics, ones built from a [handful of textbooks](https://huggingface.co/datasets/cxllin/economics), [paper abstracts](https://huggingface.co/datasets/onurkeles/econ_paper_abstracts), or econ-adjacent fields such as [finance](https://huggingface.co/datasets/gbharti/finance-alpaca). These are useful datasets but many of the texts contained within are too complicated or specific for ordinary use.

My dataset focuses on a specific type of source: economists writing about economics for public consumption. This dataset thus contains less complicated and more conversational texts (and ones more oriented to what ordinary people care about as opposed to the inside baseball present in econ papers) while still being high-quality and composed of the collective knowledge of hundreds of economists. 

The dataset is currently under construction and this section will be regularly updated as more sources of texts are added

Sources:
- Scott Sumner's blog, [TheMoneyIllusion](https://www.themoneyillusion.com/) (see: ```my_dataset/html/MI```)
- VoxEU columns, [VoxEU](https://cepr.org/voxeu) (see: ```my_dataset/html/VOXEU```)
## Fine Tuning
Fine tuning is in progress
## RAG
Made with LangChain and ChromaDB. Uses hybrid search, combining similarity score and bm25.

# Evaluation
Evaluating the effectiveness of an LLM can be quite tricky. Oftentimes, methods rely upon establishing a ground truth against which the LLM can be judged. Finding this ground truth is naturally quite difficult in a changing and contentious field like economics. In addition, it is not clear what is the goal when effectiveness is measured. Should the LLM always adopt the consensus viewpoint in economics, even when that viewpoint is not accepted by the broader public? Should the LLM make firm judgments in cases where economists themselves are divided? Some users will benefit from receiving a single right answer that will help them quickly make a decision and some users will benefit from receiving a nuanced answer that will encourage further exploration.

Therefore, multiple evaluation methods are necessary to capture all possible uses of chato_fairy.
## IGM Evaluation
The first evaluation method measures how well the LLM can adopt the consensus viewpoint in economics. To do this, I use a novel data source: the Clark Center for Economics Experts Panel (referred to as IGM surveys because that is its old name). 

This is a survey that polls ~80 leading economists on a variety of topics of economic and political import. Economists respond to statements by stating "Strongly Agree, Agree, Uncertain, Disagree, or Strongly Disagree" and then offering a confidence level in their response. They can also offer comments as to why they responded the way they did.

I rely on the confidence-weighted responses by these experts to evaluate chato_fairy. I offer chato_fairy the same statements and then ask it to respond using the same five categories (see ```config/eval_prompt.txt```). Then I compare this response to the responses of the experts to measure how much LLM opinon deviates from consensus. From this I derive two metrics: loss and accuracy. 

### Technical Details
I take the most-selected category by experts to be the correct answer. I use this to build two metrics: a custom loss function and a measure of overall accuracy. 

Accuracy is the percentage of correct responses the LLM gives.

Consider the responses as a vector of length 5, $c$, where $c$ captures the weighted percentage of expert responses to the five categories in order. Let $i$ be the index of the most popular opinion in $c$ and let $k$ be the index of the opinion held by the LLM. The loss is $(1-c_k)^2 \cdot (i-k)^2 \cdot c_i$

This custom loss function has three terms and three goals. First, we want the LLM to not select unpopular answers. That is solved by the first term in the loss function, which corresponds inversely to the popularity of the LLM's opinion. Note that this term is 0 (and thus the loss) only when the LLM has the same opinion as every single expert. Second, we want the LLM to pick as close as possible to the correct answer. In this situation, saying Agree when the correct answer is Strongly Agree is better than saying Uncertain, which in turn is better than saying Strongly Disagree. The second term solves this by corresponding inversely to the distance between the LLM's opinion and the experts' opinion. Note that this term (and thus the loss) is 0 when the LLM has the same opinion as the experts consensus. Third, we want the LLM to be punished less in cases where the answer is unclear and more in cases where the answer is clear. This is solved by the third term, which weights the loss by the strength of the consensus. This term is never 0. 

Consider the IGM survey on the [NCAA](https://kentclarkcenter.org/surveys/the-ncaa/). The confidence-weighted consensus choice is Strongly Agree. If the LLM selects Agree, the loss will be 0.133. If the LLM selects Disagree, the loss will be 4.59. This reflects the desired goal. Being almost correct is marginally punished while deviating significantly from expert opinion is very undesirable. 

### Outcomes
Using the IGM data, I test two things. First, I test the consistency of the LLM: whether or not it maintains the same opinion when asked the same question repeatedly. Second I test the loss and accuracy for the survey questions.

LLM tested: Qwen-32b-AWQ. 

**Plain LLM:**

Average Consistency: 0.898

34 out of 1000 responses incorrectly formatted

Random sample of 250 questions:

Loss = 242.1

Accuracy = 17.6% (uncorrected: 21.2%)

11/250 responses incorrectly formatted


**chato_fairy (basic RAG, default embedding model):**

Random sample of 250 questions:

Loss = 146.6

Accuracy = 36.2% (uncorrected:  50.4%)

55/250 responses incorrectly formatted