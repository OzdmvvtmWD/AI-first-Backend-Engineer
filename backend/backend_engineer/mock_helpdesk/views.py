from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MockHelpdeskTicket, MockHelpdeskReply
from .serializers import MockTicketSerializer, MockReplySerializer
from .webhook_handler import send_webhook


class MockHelpdeskTicketSenderView(APIView):

    def post(self, request, format=None):
        serializer = MockTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception = True)

        ticket = serializer.save()

        try:
            send_webhook(ticket)
        except Exception:
            
            return Response(
                {
                    'ticket_id': ticket.ticket_id,
                    'status': 'created',
                    'webhook_status': 'failed',
                },
                status=status.HTTP_202_ACCEPTED,
            )

        return Response(
            {
                'ticket_id': ticket.ticket_id,
                'status': 'created',
                'webhook_status': 'delivered',
            },
            status=status.HTTP_201_CREATED,
        )

class MockHelpdeskTicketReplierView(APIView):

    def post(self, request, ticket_id):
        
        ticket_g = get_object_or_404(
            MockHelpdeskTicket,
            ticket_id=ticket_id,
        )

        message = request.data.get('message')

        if not message:
            return Response(
                {'error': 'message are required'},
                status=status.HTTP_400_BAD_REQUEST,
            )

#         with transaction.atomic():

        reply, created = MockHelpdeskReply.objects.get_or_create(
            ticket = ticket_g.ticket_id,
            defaults={
                'message': message,
            },
        )

        if created:
      
            return Response(
                {
                    'ticket_id': reply.ticket_id,
                    'message': reply.message,
                },
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                {'status': 'already_received'},
                status=status.HTTP_200_OK,
            )