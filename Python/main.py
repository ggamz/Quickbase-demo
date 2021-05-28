import json
import os
import sys

from requests.exceptions import HTTPError
from api_clients.github import GithubClient
from api_clients.freshdesk import FreshdeskClient, FreshdeskException
from loggers.console import ConsoleLogger

logger = ConsoleLogger()

github_user_name = os.getenv("GITHUB_USERNAME")
github_access_token = os.getenv("GITHUB_TOKEN")
freshdesk_domain = os.getenv("FRESHDESK_DOMAIN")
freshdesk_access_token = os.getenv("FRESHDESK_TOKEN")

if github_user_name is None:
    logger.log_error("Missing environment variable 'GITHUB_USERNAME'! Exiting!")
    sys.exit()

if github_access_token is None:
    logger.log_error("Missing environment variable 'GITHUB_TOKEN'! Exiting!")
    sys.exit()

if freshdesk_domain is None:
    logger.log_error("Missing environment variable 'FRESHDESK_DOMAIN'! Exiting!")
    sys.exit()

if freshdesk_access_token is None:
    logger.log_error("Missing environment variable 'FRESHDESK_TOKEN'! Exiting!")
    sys.exit()

github_client = GithubClient(user_name=github_user_name, access_token=github_access_token)#"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")

try:
    user_info = github_client.get_user_info()
except HTTPError as ex:
    logger.log_error("Github get user info request failed with: Status code: {} Reason: {}".format(ex.response.status_code, ex.response.reason))

freshdesk_client = FreshdeskClient(domain=freshdesk_domain, access_token=freshdesk_access_token)

try:
    freshdesk_client.create_or_update_contact(user_info)
except HTTPError as ex:
    logger.log_error("Freshdesk create/update contact failed with: Status code: {} Reason: {}".format(ex.response.status_code, ex.response.reason))
except FreshdeskException as ex:
    logger.log_error("Freshdesk create/update contact failed with: {}".format(str(ex)))

#print(test2.login)