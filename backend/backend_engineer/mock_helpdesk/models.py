from django.db import models
import random
import string


def generate_event_id():
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f'evt_{random_string}'

class MockHelpdeskTicket(models.Model):
    event_id = models.CharField(max_length=255, unique=True, default=generate_event_id)
    ticket_id = models.CharField(max_length=255, unique=True, blank=True)
    customer_email = models.EmailField()
    message = models.TextField()

    reply_url = models.CharField(max_length=1028)



class MockHelpdeskReply(models.Model):
    ticket = models.OneToOneField(
        MockHelpdeskTicket,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    message = models.TextField()
