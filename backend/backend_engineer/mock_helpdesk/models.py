from django.db import models

# Create your models here.

class MockHelpdeskTicket(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    ticket_id = models.CharField(max_length=255, unique=True)
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
