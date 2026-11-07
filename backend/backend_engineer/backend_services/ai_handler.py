import os
from openai import OpenAI

from .promt import SYSTEM_PROMPT, STATIC_ANSWER

def generate_static_draft(knowledge_articles):

    articles_text = "\n\n".join(
        [
            f"Стаття: {article.title}\n"
            f"{article.content}"
            for article in knowledge_articles
        ]
    )

    return (
        f"{STATIC_ANSWER}\n\n"
        f"Статті з бази знань:\n{articles_text}"
    )

def generate_draft(ticket_message, knowledge_articles):

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    articles_text = "\n\n".join(
        [
            f"Стаття: {article.title}\n"
            f"{article.content}"
            for article in knowledge_articles
        ]
    )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"""
                    Звернення клієнта:
                    {ticket_message}

                    Статті з бази знань:
                    {articles_text}

                    Підготуй відповідь клієнту.
                """,
            },
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content