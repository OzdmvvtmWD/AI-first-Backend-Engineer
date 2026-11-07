from django.urls import path
from django.conf import settings


from .views import MockHelpdeskTicketSenderView, MockHelpdeskTicketReplierView, RepliesForHelpdeskViews

urlpatterns = [
    path("tickets/", MockHelpdeskTicketSenderView.as_view()),
    path('replies/', MockHelpdeskTicketReplierView.as_view()),
    path('tickets/<str:ticket_id>/replies/', RepliesForHelpdeskViews.as_view()),

]

