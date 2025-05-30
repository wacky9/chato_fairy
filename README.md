# chato_fairy
The Chato Fairy is an LLM applicaton designed to work specifically on economic issues. This application can summarize economic research, accurately answer economic questions, and otherwise assist in economic endeavors.

# Why Chato Fairy
There is a growing need for LLMs that are focused on and capable of assisting users in working with complex subjects. Economics is a field ripe for such an application. Economics is a deep and wide field where most people have little-to-no expertise. Nevertheless, these people are regularly asked to engage in difficult decisions where knowledge of economics would be quite useful. For example, Burke and Manz (2014) identify a link between economic literacy and more accurate inflation expectations. Households having more accurate inflation expectations would improve their budgeting and prevent nasty surprises. 

For ordinary inviduals and most businesses, reading economic research and studying economics is a prohibitively difficult task. Hiring an economist to advise you is likewise expensive. Thus there is a need to provide good information about economics without requiring years of study. Hence, LLMs. [Recent news](https://garymarcus.substack.com/p/did-an-llm-help-write-trumps-trade) has shown that people already use LLMs to alleviate this gap in knowledge and underscores the importance of having LLMs provide up-to-date, accurate information about economic subjects.

# Technical details
Chato Fairy is composed of three important sections. First is a custom dataset of high-quality information about economics. Second is an LLM fine-tuned on a modified version of this dataset. Third is a RAG component using this dataset. The entire project is inside a Docker Container and designed to run locally.

## Dataset
There are some currently existing LLM datasets for economics, ones built from a [handful of textbooks](https://huggingface.co/datasets/cxllin/economics), [paper abstracts](https://huggingface.co/datasets/onurkeles/econ_paper_abstracts), or econ-adjacent fields such as [finance](https://huggingface.co/datasets/gbharti/finance-alpaca). These are useful datasets but many of the texts contained within are too complicated or specific for ordinary use.
My dataset focuses on a specific type source: economists writing about economics for public consumption. This dataset thus contains less complicated and more conversational texts (and ones more oriented to what ordinary people care about as opposed to the inside baseball present in in econ papers) while still being high-quality and composed of the collective knowledge of hundreds of economists. 

The dataset is currently under construction and this section will be regularly updated as more sources of texts are added

Sources:
- Scott Sumner's blog, [TheMoneyIllusion](https://www.themoneyillusion.com/) (see: ```my_dataset/html/MI```)

## Fine Tuning
Fine tuning is in progress
## RAG
Made with LangChain and ChromaDB. Uses hybrid search, combining similarity score and bm25.