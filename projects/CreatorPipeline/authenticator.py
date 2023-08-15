import os

import httplib2
from apiclient.discovery import build
from CreatorPipeline.constants import PLATFORMS
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


class PlatformAuth:
    """Class that handles authenticating a platform for web access to publish episode content"""

    def youtube(self, simple=False):
        """Authenticates Youtube API for web access."""
        keys = PLATFORMS.youtube
        if simple:
            youtube = build(
                keys["api_service_name"],
                keys["api_version"],
                developerKey=keys["developerKey"],
            )
            return youtube

        flow = flow_from_clientsecrets(
            PLATFORMS.client_secret,
            keys["youtube_upload_scope"],
        )

        oauth_file = os.environ["OAUTH2_FILE"]
        storage = Storage(oauth_file)
        credentials = storage.get()
        print(oauth_file)
        print(dir(credentials))

        # if this is first time, sign in with oauth
        if credentials is None or credentials.invalid:
            print("not")
            flags = argparser.parse_args(args=[])
            flags.noauth_local_webserver = True
            credentials = run_flow(flow, storage, flags)

        youtube = build(
            keys["api_service_name"],
            keys["api_version"],
            http=credentials.authorize(httplib2.Http()),
        )
        return youtube

    def buzzsprout(self):
        """Authenticates Buzzsprout API for web access."""
        return PLATFORMS.buzzsprout

    def openai(self):
        """Authenticates OpenAI API for web access."""
        return PLATFORMS.openai
