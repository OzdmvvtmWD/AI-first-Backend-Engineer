import json
import requests

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .tasks import send_save_reply

@csrf_exempt
def backend_webhook(request):

    if request.method != "POST":
        return HttpResponseBadRequest(
            "Invalid request method."
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest(
            "Invalid JSON payload."
        )

    event_id = data.get("event_id")
    ticket_id = data.get("ticket_id")
    customer_email = data.get("customer_email")
    message = data.get("message")
    reply_url = data.get("reply_url")

    if not ticket_id or not reply_url:
        return JsonResponse(
            {"error": "ticket_id and reply_url are required"},
            status=400,
        )

    send_save_reply(ticket_id, message)

    return JsonResponse(
        {
            "status": "success",
            "event_id": event_id,
            "ticket_id": ticket_id,
            "reply_status": "sent",
        },
        status=200,
    )