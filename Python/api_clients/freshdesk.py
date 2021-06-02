import requests
from requests.auth import HTTPBasicAuth
from loggers.console import ConsoleLogger

logger = ConsoleLogger()

class FreshdeskException(Exception):
    pass

class FreshdeskClient:
    def __init__(self, domain, access_token):
        self.base_url = "https://{}.freshdesk.com/api/v2".format(domain)
        self.access_token = access_token
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.access_token,"X")
    
    def get_contact_id_by_external_id(self, external_id):
        response = self.session.get("{}/search/contacts?query=\"unique_external_id:'{}'\"".format(self.base_url, external_id))
        response.raise_for_status()
        res_json = response.json()

        if res_json.get("total", 0) == 0:
            return None
        
        return res_json["results"][0]["id"]

    def create_or_update_contact(self, user):
        if not user.username:
            raise FreshdeskException("Username missing in parameter user!")

        #Name is mandatory acording to Freshdesk api documentation
        if not user.name:
            raise FreshdeskException("Name missing in parameter user!")

        contact_id = self.get_contact_id_by_external_id(user.username)
        payload = self.payload_from_user(user)

        if not contact_id:
            #create contact
            response = self.session.post("{}/contacts".format(self.base_url), json=payload)
        else:
            #update contact
            response = self.session.put("{}/contacts/{}".format(self.base_url, contact_id), json=payload)
        
        response.raise_for_status()
        
        if not contact_id:
            logger.log_info("Freshdesk contact created successfully")
        else:
            logger.log_info("Freshdesk contact updated successfully")  

    def payload_from_user(self, user):
        return {
            "unique_external_id": user.username,
            "name": user.name,
            "email": user.email,
            "address": user.location,
            "twitter_id": user.twitter_username,
            "description": user.bio
        }
