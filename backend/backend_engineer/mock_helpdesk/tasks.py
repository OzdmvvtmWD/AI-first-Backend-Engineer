from .models import MockHelpdeskTicket
from celery import shared_task


from .webhook_handler import send_webhook

@shared_task(
    bind=True,
    max_retries=None, 
)
def retry_timeout(self, ticket_id):

    try:
        ticket = MockHelpdeskTicket.objects.get(pk=ticket_id)
        send_webhook(ticket)

    except Exception as exc:

        raise self.retry(
            exc=exc,
            countdown=2,
        )