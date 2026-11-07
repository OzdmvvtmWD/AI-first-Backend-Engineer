import json

from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MockHelpdeskTicket, MockHelpdeskReply
from .serializers import MockTicketSerializer, MockReplySerializer
from .tasks import retry_timeout

class MockHelpdeskTicketSenderView(APIView):

    def post(self, request):

        serializer = MockTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():
                ticket = MockHelpdeskTicket.objects.create(
                    **serializer.validated_data
                )

        except IntegrityError:

            return Response(
                {
                    'event_id': serializer.validated_data["event_id"],
                    'status': 'already_received',
                },
                status=status.HTTP_200_OK,
            )

        retry_timeout.delay_on_commit(ticket.pk)

        return Response(
            {
                'ticket_id': ticket.ticket_id,
                'status': 'created',
                'webhook_status': 'pending',
            },
            status=status.HTTP_201_CREATED,
        )
    
class MockHelpdeskTicketReplierView(APIView):

    def post(self, request):

        ticket_id = request.data.get("ticket_id")

        if not ticket_id:
            return Response(
                {"error": "ticket_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = request.data.get("message")
    
        if not message:
            return Response(
                {"error": "message is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


        ticket = get_object_or_404(
            MockHelpdeskTicket,
            ticket_id=ticket_id,
        )

        reply, created = MockHelpdeskReply.objects.get_or_create(
            ticket=ticket,
            defaults={"message": message},
        )

        if created:
            return Response(
                {
                    "status": "created",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "ticket_id": ticket.ticket_id,
                "status": "already_received",
            },
            status=status.HTTP_200_OK,
        )

class RepliesForHelpdeskViews(APIView):

    def post(self, request, ticket_id):

        # if request.method != "POST":
        #     return HttpResponseBadRequest("Invalid request method.")

        ticket = get_object_or_404(
                MockHelpdeskTicket,
                ticket_id=ticket_id,
            )

        reply_t = get_object_or_404(
                MockHelpdeskReply,
                ticket_id=ticket,
            )

        return Response(
            {
                "ticket_id": ticket.ticket_id,
                "message": reply_t.message,
            },
            status=status.HTTP_201_CREATED,
        )
