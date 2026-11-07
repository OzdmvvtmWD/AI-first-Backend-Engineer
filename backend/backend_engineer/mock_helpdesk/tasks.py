from .models import MockHelpdeskTicket
from celery import shared_task


from .webhook_handler import send_webhook


@shared_task(
    bind=True,
    max_retries=None,
)
def retry_timeout(self, ticket_id):

    ticket = MockHelpdeskTicket.objects.get(
        pk=ticket_id
    )

    ticket.status = MockHelpdeskTicket.Status.PROCESSING
    ticket.save(update_fields=["status"])

    try:

        send_webhook(ticket)

        ticket.status = MockHelpdeskTicket.Status.DONE
        ticket.save(update_fields=["status"])

    except Exception as exc:

        ticket.status = MockHelpdeskTicket.Status.FAILURE
        ticket.save(update_fields=["status"])

        raise self.retry(
            exc=exc,
            countdown=2,
        )