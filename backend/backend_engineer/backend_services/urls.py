from django.urls import path
from django.conf import settings

from .views import backend_webhook

urlpatterns = [
    path("/webhooks/helpdesk/",backend_webhook, name="backend_webhook"),
]
