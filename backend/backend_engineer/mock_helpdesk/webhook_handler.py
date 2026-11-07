import random
import string

import requests
from django.conf import settings

def generate_event_id():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f'evt_{random_string}'

def send_webhook(ticket):

    event_id = generate_event_id()
    ticket_id = f"T-{ticket.pk}"

    reply_url = (
        f'{settings.MOCK_HELPDESK_PUBLIC_URL}'
        f'/mock/helpdesk/tickets/{ticket_id}/replies/'
    )
    #http://localhost:1337/api/v1/tickets/T-1042/replies/

    payload = {
        'event_id': event_id,
        'ticket_id': ticket_id,
        'customer_email': ticket.customer_email,
        'message': ticket.message,
        'reply_url': reply_url,
    }

    response = requests.post(
        settings.WEBHOOK_URL,
        json=payload,
        timeout=1.5,
    )

    response.raise_for_status()

    return response