from django.db import IntegrityError, transaction
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import MockHelpdeskTicket, MockHelpdeskReply
from .serializers import MockTicketSerializer, MockReplySerializer
from .tasks import retry_timeout


class MockHelpdeskTicketSenderView(APIView):

    def get(self, request, format=None):

        tickets = MockHelpdeskTicket.objects.all()

        serializer = MockTicketSerializer(
            tickets,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = MockTicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            with transaction.atomic():

                ticket = MockHelpdeskTicket.objects.create(
                    **serializer.validated_data,
                    status=MockHelpdeskTicket.Status.PENDING,
                )

                retry_timeout.delay_on_commit(ticket.pk)

        except IntegrityError:

            return Response(
                {
                    "event_id": serializer.validated_data["event_id"],
                    "status": "already_received",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "ticket_id": ticket.ticket_id,
                "status": ticket.status,
                # "webhook_status": "pending",
            },
            status=status.HTTP_201_CREATED,
        )

class MockHelpdeskTicketReplierView(APIView):

    
    def get(self, request, format=None):

        replies = MockHelpdeskReply.objects.select_related(
            "ticket"
        ).all()

        serializer = MockReplySerializer(
            replies,
            many=True
        )

        return Response(serializer.data)


    def post(self, request):

        ticket_id = request.data.get("ticket_id")
        message = request.data.get("message")

        if not ticket_id or not message:
            return Response(
                {"error": "ticket_id and message are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():

            ticket = get_object_or_404(
                MockHelpdeskTicket.objects.select_for_update(),
                ticket_id=ticket_id,
            )

            reply = MockHelpdeskReply.objects.filter(
                ticket=ticket
            ).first()

            if reply:
                return Response(
                    {
                        "ticket_id": ticket.ticket_id,
                        "status": "already_received",
                    },
                    status=status.HTTP_200_OK,
                )

            MockHelpdeskReply.objects.create(
                ticket=ticket,
                message=message,
                status=MockHelpdeskReply.Status.DONE,
            )

            ticket.status = MockHelpdeskTicket.Status.DONE
            ticket.save(update_fields=["status"])

        return Response(
            {
                "ticket_id": ticket.ticket_id,
                "status": "created",
            },
            status=status.HTTP_201_CREATED,
        )


class RepliesForHelpdeskViews(APIView):

    def post(self, request, ticket_id):

        if request.method != "POST":
                return HttpResponseBadRequest(
                    "Invalid request method."
                )

        ticket = get_object_or_404(
            MockHelpdeskTicket,
            ticket_id=ticket_id,
        )

        reply = get_object_or_404(
            MockHelpdeskReply,
            ticket=ticket,
        )

        return Response(
            {
                "ticket_id": ticket.ticket_id,
                "message": reply.message,
            },
            status=status.HTTP_200_OK,
        )