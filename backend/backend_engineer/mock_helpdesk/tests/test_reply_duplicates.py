from django.test import TestCase
from rest_framework.test import APIClient

from mock_helpdesk.models import (
    MockHelpdeskTicket,
    MockHelpdeskReply,
)


class ReplyDuplicateTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.ticket = MockHelpdeskTicket.objects.create(
            event_id="evt_123",
            ticket_id="T-1042",
            customer_email="user@example.com",
            message="Cannot export PDF",
            reply_url="http://example.com/reply/",
        )

        self.url = (
            f"/mock/helpdesk/tickets/"
            f"{self.ticket.ticket_id}/replies/"
        )

        self.payload = {
            "message": "Open reports and click Export PDF",
        }

    def test_create_reply(self):

        response = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            MockHelpdeskReply.objects.count(),
            1,
        )

    def test_duplicate_reply(self):

        response1 = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        response2 = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 200)

        self.assertEqual(
            MockHelpdeskReply.objects.count(),
            1,
        )

    def test_duplicate_reply_does_not_overwrite_message(self):

        self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        second_payload = {
            "message": "Another different answer",
        }

        response = self.client.post(
            self.url,
            second_payload,
            format="json",
        )

        self.assertEqual(response.status_code, 200)

        reply = MockHelpdeskReply.objects.get(
            ticket=self.ticket,
        )

        self.assertEqual(
            reply.message,
            self.payload["message"],
        )