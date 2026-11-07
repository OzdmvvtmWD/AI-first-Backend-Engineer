import os
from openai import OpenAI

from .promt import SYSTEM_PROMPT, STATIC_ANSWER

def generate_static_draft(knowledge_articles):

    return (
       f"{STATIC_ANSWER}"
        "Статі з бази знань :"
        f"{knowledge_articles}"
    )


def generate_draft(ticket_message, knowledge_articles):

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": f"""
                    Звернення клієнта:
                    {ticket_message}

                    Статі з бази знань :
                    {knowledge_articles}

                    Підготов відповідь клієнту.
                """
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content