from sentence_transformers import SentenceTransformer
from articles.models import Article

model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")


def get_relevant_articles(query, top_k=3, threshold=0.4):

    articles = list(Article.objects.all())

    if not articles:
        return []

    documents = [
        f"{article.title}\n{article.content}"
        for article in articles
    ]

    query_embedding = model.encode_query(query)

    document_embeddings = model.encode_document(documents)

    scores = model.similarity(
        query_embedding,
        document_embeddings
    )[0]

    relevant_articles = []

    for index in scores.argsort(descending=True):

        score = scores[index].item()

        if score < threshold:
            break

        article = articles[index]

        relevant_articles.append(article)

        if len(relevant_articles) >= top_k:
            break

    return relevant_articles