from api_clients.freshdesk import FreshdeskClient
from models.user import User
import unittest
from unittest.mock import patch
import requests_mock

class MockedResponse:
    def raise_for_status(self):
        pass

class FreshdeskTest(unittest.TestCase):

    def helper_create_update_contact(self, existing_contact_id, expected_post_count, expected_put_count):
        self.called_post_counter = 0
        self.called_put_counter = 0

        def _post(*args, **kwargs):
            self.called_post_counter += 1
            return MockedResponse()

        def _put(*args, **kwargs):
            self.called_put_counter += 1
            return MockedResponse()

        def _get_contact_id_by_external_id(*args, **kwargs):
            return existing_contact_id

        patchers = [
            patch('requests.Session.post', side_effect=_post),
            patch('requests.Session.put', side_effect=_put),
            patch('api_clients.freshdesk.FreshdeskClient.get_contact_id_by_external_id', side_effect=_get_contact_id_by_external_id)
            ]
        for p in patchers:
            p.start()
            self.addCleanup(p.stop)
            
        fdc = FreshdeskClient('ku', 'r')
        u = User(username="test", name='Test')
        fdc.create_or_update_contact(u)
        self.assertEqual(self.called_post_counter, expected_post_count)
        self.assertEqual(self.called_put_counter, expected_put_count)

    def test_create_contact(self):
        self.helper_create_update_contact(None, 1, 0)
    
    def test_update_contact(self):
        self.helper_create_update_contact(1, 0, 1)
