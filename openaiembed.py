import os
import openai
from dotenv import load_dotenv

load_dotenv()
model = 'ada'
#OPENAI_ENGINE = 'text-embedding-ada-002'  # Which engine to use
OPENAI_ENGINE = f'text-embedding-{model}-002'
ANSWER_ENGINE='text-davinci-003'
openai.api_key = os.getenv("OPENAI_API") 
# Use your own Open AI API Key here


def embed(text):
    text = text.replace("\n", " ")
    return openai.Embedding.create(
        input=text, 
        engine=OPENAI_ENGINE)["data"][0]["embedding"]
def get_insert_embed(data):
    ins = [
        [data['id']],
        [data['category']],
        [embed(data['text'])],
        [data['text']]
        ]
    return ins

def summarize_article(question, markdown):
    prompt = f"""Question: {question}
Article:
{markdown}

###
Does the given article contain all information required to answer the question? If not, return "Answer: I don't know."

If the article contains the answer, answer the question using the given article.
Don't use your own knowledge. If the answer is not in the provided article text, return "Answer: I don't know."
Examples:
---
Answer: I don't know.
---
---
Answer: here is the answer (one or two paragraphs)
---
"""
    response = openai.Completion.create(model=ANSWER_ENGINE, prompt=prompt, temperature=0, max_tokens=200)
    return response['choices'][0]['text']


def get_final_answer(question, summaries):
    answers = "\n".join(summaries)
    prompt = f"""Question: {question}
    Answers: {answers}

    ###
    Write a final answer to the question using the answers provided above.
    If the answer is not in the provided answers, return "Answer: I don't know."
    If the provided answer does not answer the question, skip it.
"""
    response = openai.Completion.create(model=ANSWER_ENGINE, prompt=prompt, temperature=0, max_tokens=200)
    return response['choices'][0]['text']