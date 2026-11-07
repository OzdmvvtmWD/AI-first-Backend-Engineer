import requests

from celery import shared_task
from django.http import JsonResponse, HttpResponseBadRequest

from .create_draft import create_draft

@shared_task(
    bind=True,
    max_retries=None,
)
def send_save_reply(self, ticket_id, message):

    draft = create_draft(message)['draft']
    reply_url = f'http://localhost:8000/api/v1/replies/'

    reply_payload = {
        "ticket_id" : ticket_id,
        "message" : draft
    }


    try:
        response = requests.post(
            reply_url,
            json=reply_payload,
            timeout=5,
        )

        response.raise_for_status()

    # except requests.RequestException as exc:
    #     return JsonResponse(
    #         {
    #             "error": "Failed to send reply",
    #             "details": str(exc),
    #         },
    #         status=502,
    #     )

    except Exception as exc:

        raise self.retry(
            exc=exc,
            countdown=2,
        )