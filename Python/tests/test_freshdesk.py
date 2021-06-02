import unittest
import requests_mock
from unittest.mock import patch
from requests.exceptions import HTTPError
from api_clients.freshdesk import FreshdeskClient
from models.user import User

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
            patch("requests.Session.post", side_effect=_post),
            patch("requests.Session.put", side_effect=_put),
            patch("api_clients.freshdesk.FreshdeskClient.get_contact_id_by_external_id", side_effect=_get_contact_id_by_external_id)
            ]
        for p in patchers:
            p.start()
            self.addCleanup(p.stop)
            
        fdc = FreshdeskClient("doesnt", "matter")
        u = User(username="test", name="Test")
        fdc.create_or_update_contact(u)
        self.assertEqual(self.called_post_counter, expected_post_count)
        self.assertEqual(self.called_put_counter, expected_put_count)

    def test_create_contact(self):
        self.helper_create_update_contact(None, 1, 0)
    
    def test_update_contact(self):
        self.helper_create_update_contact(1, 0, 1)

    def test_get_contact_id_by_external_id_200(self):
        mock_response = {
            "results": [
                {
                    "active": False,
                    "address": None,
                    "custom_fields": {},
                    "description": None,
                    "email": "emily.dean@freshdesk.com",
                    "other_emails": [],
                    "id": 80022353975,
                    "job_title": None,
                    "language": "en",
                    "mobile": None,
                    "name": "Emily Dean",
                    "phone": None,
                    "time_zone": "Casablanca",
                    "twitter_id": None,
                    "facebook_id": None,
                    "external_id": None,
                    "created_at": "2021-05-28T12:26:08Z",
                    "updated_at": "2021-05-28T12:26:08Z",
                    "company_id": None,
                    "unique_external_id": None
                }
            ],
            "total": 1
        }
        with requests_mock.Mocker() as m:
            m.get("https://testDomain.freshdesk.com/api/v2/search/contacts?query=\"unique_external_id:'testUser'\"", json=mock_response)
            freshdesk_client = FreshdeskClient("testDomain", "doesntmatter")
            user_id = freshdesk_client.get_contact_id_by_external_id("testUser")
            self.assertEqual(user_id, 80022353975)

    def test_get_contact_id_by_external_id_404(self):
        with requests_mock.Mocker() as m:
            m.get("https://testDomain.freshdesk.com/api/v2/search/contacts?query=\"unique_external_id:'testUser'\"",status_code=404, reason="Mocked 404")
            github_client = FreshdeskClient("testDomain", "doesntmatter")
            with self.assertRaises(HTTPError) as cm:
                user_info = github_client.get_contact_id_by_external_id("testUser")
            self.assertEqual(str(cm.exception), "404 Client Error: Mocked 404 for url: https://testdomain.freshdesk.com/api/v2/search/contacts?query=%22unique_external_id:'testUser'%22")

