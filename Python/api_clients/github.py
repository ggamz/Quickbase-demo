import requests
from requests.auth import HTTPBasicAuth
from models.user import User

class GithubClient:
    def __init__(self, user_name, access_token):
        self.base_url = "https://api.github.com"
        self.user_name = user_name
        self.access_token = access_token
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.user_name, self.access_token)

    def get_user_info(self):
        response = self.session.get("{}/users/{}".format(self.base_url, self.user_name))
        response.raise_for_status()
        res_json = response.json()
        #return User(**response.json()) #Easy solution, but won't work for other APIs and/or if the model becomes more complex
        user_dict = {
            "username" : "github:{}".format(res_json["login"]),
            "avatar_url" : res_json.get("avatar_url", None),
            "gravatar_id" : res_json.get("gravatar_id", None),
            "name" : res_json.get("name", None),
            "company" : res_json.get("company", None),
            "blog" : res_json.get("blog", None),
            "location" : res_json.get("location", None),
            "email" : res_json.get("email", None),
            "bio" : res_json.get("bio", None),
            "twitter_username" : res_json.get("twitter_username", None),
            "hireable" : res_json.get("hireable", None)
        }
        return User(**user_dict)      