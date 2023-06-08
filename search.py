from vectordb import get_or_create_collection
from openaiembed import embed,summarize_article, get_final_answer


collection = get_or_create_collection()
collection.load()

# Search the database based on input text
def find_articles(text):
    # Search parameters for the index
    search_params = {
        "metric_type": "L2", 
        "params": {"nprobe": 10}, 
        "offset": 0
    }

    results=collection.search(
        data=[embed(text)],  # Embeded search value
        anns_field="embedding",  # Search across embeddings
        param=search_params,
        limit=3,  # Limit to five results per search
        output_fields=['content']  # Include title field in result
    )

    for result in results[0]:
        yield result.entity.get('content')
        #print(result.entity.get('content'))





def get_answer_candidates(question, article_contents):
    for content in article_contents:
        
        markdown = content[0:3500] # GPT-3 has a token limit around 4k tokens
        summary = summarize_article(question, markdown)
        if "Answer: I don't know." not in summary:
            yield (content, summary)


def answer(question):
    article_contents = find_articles(question)
    content_with_answers = list(get_answer_candidates(question, article_contents))
    summaries = [answer for _, answer in content_with_answers]
    #print(summaries)
    final_answer = get_final_answer(question, summaries)
    return final_answer


#print(answer("What is Recall in Javascript?"))
text = input("prompt")
print(answer(text))
