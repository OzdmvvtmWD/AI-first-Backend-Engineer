from sentence_transformers import SentenceTransformer

from articles.models import Article

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

def get_relevant_articles(query, top_k=3, threshold=0.4):
    most_valid_result = []

    documents = list(Article.objects.all())
        
    query_embedding = model.encode_query(query)
    document_embeddings = model.encode_document(documents)
    scores = model.similarity(query_embedding, document_embeddings)[0]

    for index in scores.argsort(descending=True):
        print(f"{scores[index]:.4f}: {documents[index]}")
        # results[documents[index]] = scores[index]

        if scores[index] >= threshold:
            most_valid_result.append(documents[index])

    return most_valid_result

