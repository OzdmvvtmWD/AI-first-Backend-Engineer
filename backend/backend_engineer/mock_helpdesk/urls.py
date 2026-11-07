from django.urls import path
from django.conf import settings

# from rest_framework.urlpatterns import format_suffix_patterns


from .views import MockHelpdeskTicketSenderView, MockHelpdeskTicketReplierView

urlpatterns = [
    path("tickets/", MockHelpdeskTicketSenderView.as_view()),
   path('tickets/<str:ticket_id>/replies/', MockHelpdeskTicketReplierView.as_view()),

]

# urlpatterns = format_suffix_patterns(urlpatterns)