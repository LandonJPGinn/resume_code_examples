import json
import pprint

from CreatorPipeline.authenticator import PlatformAuth as Auth
from CreatorPipeline.constants import PLATFORMS
from requests.exceptions import HTTPError

pp = pprint.PrettyPrinter(indent=4)


class YoutubeQuery:
    """Query Youtube API for information about a channel or video."""
    def __init__(self):
        self.__dict__.update(**PLATFORMS.youtube)
        # self.__dict__.update(**content)
        self.youtube = Auth().youtube(simple=True)
        print(type(self.youtube))

    def _print(self, results):
        """Prints results from a Youtube API query."""
        print(json.dumps(results, indent=4))

    def keyword_results(self, keyword, key_type="video"):
        """Searches Youtube for a keyword and returns results."""
        try:
            search_response = (
                self.youtube.search()
                .list(q=keyword, part="snippet", type=key_type)
                .execute()
            )

            self._print(search_response)

        except HTTPError as e:
            print("An error occurred: %s" % e)

    def channel_contents(self, keyword, channelId):
        """Searches a channel for a keyword and returns results."""
        search_response = (
            self.youtube.search()
            .list(q=keyword, part="snippet", type="video", channelId=channelId)
            .execute()
        )
        self._print(search_response)

    def channel_details(self, channelId):
        """Searches a channel for a keyword and returns results."""
        search_response = (
            self.youtube.channels()
            .list(part="snippet,contentDetails,statistics", id=channelId)
            .execute()
        )
        self._print(search_response)


query = YoutubeQuery()
# query.keyword_results("Linus Tech Tips", key_type="channel")
query.channel_details("UCXuqSBlHAE6Xw-yeJA0Tunw")
# forUsername="GoogleDevelopers"
