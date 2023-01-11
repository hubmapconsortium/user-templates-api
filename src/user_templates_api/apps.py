from django.apps import AppConfig
from django.conf import settings
import globus_sdk

from hubmap_commons.hm_auth import AuthHelper

class UserTemplatesApiConfig(AppConfig):
    name = 'user_templates_api'
    auth_helper = None

    def ready(self):
        client_id = settings.CONFIG["GLOBUS_CLIENT_ID"]
        client_secret = settings.CONFIG["GLOBUS_CLIENT_SECRET"]
        if not AuthHelper.isInitialized():
            self.auth_helper = AuthHelper.create(
                clientId=client_id, clientSecret=client_secret
            )
        else:
            self.auth_helper = AuthHelper.instance()
