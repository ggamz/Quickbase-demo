import unittest
import requests_mock
from api_clients.github import GithubClient
from requests.exceptions import HTTPError

class GithubTest(unittest.TestCase):
    def test_get_user_info_200(self):
        mock_response = {
            "login": "defunkt",
            "id": 2,
            "node_id": "MDQ6VXNlcjI=",
            "avatar_url": "https://avatars.githubusercontent.com/u/2?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/defunkt",
            "html_url": "https://github.com/defunkt",
            "followers_url": "https://api.github.com/users/defunkt/followers",
            "following_url": "https://api.github.com/users/defunkt/following{/other_user}",
            "gists_url": "https://api.github.com/users/defunkt/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/defunkt/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/defunkt/subscriptions",
            "organizations_url": "https://api.github.com/users/defunkt/orgs",
            "repos_url": "https://api.github.com/users/defunkt/repos",
            "events_url": "https://api.github.com/users/defunkt/events{/privacy}",
            "received_events_url": "https://api.github.com/users/defunkt/received_events",
            "type": "User",
            "site_admin": False,
            "name": "Chris Wanstrath",
            "company": None,
            "blog": "http://chriswanstrath.com/",
            "location": None,
            "email": None,
            "hireable": None,
            "bio": "🍔",
            "twitter_username": None,
            "public_repos": 107,
            "public_gists": 273,
            "followers": 21205,
            "following": 210,
            "created_at": "2007-10-20T05:24:19Z",
            "updated_at": "2019-11-01T21:56:00Z"
        }
        with requests_mock.Mocker() as m:
            m.get("https://api.github.com/users/testuser", json=mock_response)
            github_client = GithubClient("testuser", "doesntmatter")
            user_info = github_client.get_user_info()
            self.assertEqual(user_info.username, "github:defunkt")

    def test_get_user_info_404(self):
        with requests_mock.Mocker() as m:
            m.get("https://api.github.com/users/testuser",status_code=404, reason="Mocked 404")
            github_client = GithubClient("testuser", "doesntmatter")
            with self.assertRaises(HTTPError) as cm:
                user_info = github_client.get_user_info()
            self.assertEqual(str(cm.exception), "404 Client Error: Mocked 404 for url: https://api.github.com/users/testuser")

