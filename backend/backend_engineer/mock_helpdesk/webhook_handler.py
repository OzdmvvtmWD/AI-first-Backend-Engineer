import requests
from django.conf import settings


def send_webhook(ticket):

    event_id = f'evt_{ticket.pk}'

    reply_url = (
        f'{settings.MOCK_HELPDESK_PUBLIC_URL}'
        f'/mock/helpdesk/tickets/{ticket.ticket_id}/replies/'
    )
    #http://localhost:1337/api/v1/tickets/T-1042/replies/

    payload = {
        'event_id': event_id,
        'ticket_id': ticket.ticket_id,
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