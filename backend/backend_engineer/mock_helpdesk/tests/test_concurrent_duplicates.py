from concurrent.futures import ThreadPoolExecutor
from django.db import connections
from rest_framework.test import APIClient
from django.test import TransactionTestCase

from mock_helpdesk.models import MockHelpdeskTicket


class ConcurrentDuplicateTests(TransactionTestCase):

    def send_request(self, payload):
        connections.close_all()

        try:
            client = APIClient()

            return client.post(
                "/api/v1/tickets/",
                payload,
                format="json",
            )
        finally:
            connections.close_all()

    def test_concurrent_duplicate_tickets(self):

        payload = {
            "event_id": "evt_concurrent",
            "ticket_id": "T-CONCURRENT",
            "customer_email": "test@example.com",
            "message": "Test message",
        }

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(self.send_request, payload)
                for _ in range(5)
            ]

            responses = [future.result() for future in futures]

        self.assertEqual(
            MockHelpdeskTicket.objects.filter(
                event_id="evt_concurrent"
            ).count(),
            1,
        )

        statuses = [response.status_code for response in responses]

        self.assertEqual(statuses.count(201), 1)
        self.assertEqual(statuses.count(200), 4)