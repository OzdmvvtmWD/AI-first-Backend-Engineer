from django.test import TestCase
from rest_framework.test import APIClient

from mock_helpdesk.models import MockHelpdeskTicket


class TicketDuplicateTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.url = "/api/v1/tickets/"

        self.payload = {
            "event_id": "evt_123",
            "ticket_id": "T-1042",
            "customer_email": "user@example.com",
            "message": "Cannot export PDF",
        }

    def test_create_ticket(self):
        response = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        self.assertEqual(response.status_code, 201)

        self.assertEqual(
            MockHelpdeskTicket.objects.count(),
            1,
        )

    def test_duplicate_event_id(self):
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
        self.assertEqual(response2.status_code, 400)

        self.assertEqual(
            MockHelpdeskTicket.objects.count(),
            1,
        )

    def test_duplicate_ticket_id(self):
        response1 = self.client.post(
            self.url,
            self.payload,
            format="json",
        )

        payload2 = {
            **self.payload,
            "event_id": "evt_456",
        }

        response2 = self.client.post(
            self.url,
            payload2,
            format="json",
        )

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 400)

        self.assertEqual(
            MockHelpdeskTicket.objects.count(),
            1,
        )