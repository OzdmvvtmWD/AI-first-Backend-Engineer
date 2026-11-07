import os

from .embedding_handler import get_relevant_articles
from .ai_handler import generate_draft, generate_static_draft


def create_draft(ticket_message):

    articles = get_relevant_articles(
        ticket_message,
        top_k=3,
        threshold=0.4,
    )

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:

        try:
            draft = generate_draft(
                ticket_message,
                articles,
            )

            if draft:
                return {
                    "draft": draft,
                    "sources": articles,
                    "generation_method": "openai",
                }

        except Exception as exc:
            print(f"OpenAI generation failed: {exc}")

    draft = generate_static_draft(articles)

    return {
        "draft": draft,
        "sources": articles,
        "generation_method": "static",
    }