import pprint

import requests
from authenticator import PlatformAuth as Auth
from constants import DEFAULTS

pp = pprint.PrettyPrinter(indent=4)


class BuzzsproutEpisodePublisher:
    """Buzzsprout Publisher Interface"""
    def __init__(self, content):
        self.content = content
        self.podcast_params = {
            "api_key": Auth.buzzsprout().get("api_key", ""),
            "guid": Auth.buzzsprout().get("guid", ""),
            "artist": DEFAULTS.channelHost,
            "title": self.content.title,
            "description": self.content.description,
            # "episode_number": self.content.episode_number,
            # "season_number": self.content.season_number,
            "explicit": False,
            "private": True,
            "audio_file": self.content.file,
            "published_at": self.content.schedule_at,
            "email_user_after_audio_processed": True,
            "tags": self.content.tags,
        }
        self.url = Auth.buzzsprout().get("url", "")
        self.headers = {"Content-Type": "application/json; charset=utf-8"}

    def publish(self):
        """Publishes the episode to buzzsprout."""
        response = requests(
            self.url,
            headers=self.headers,
            params=self.podcast_params,
        )

        if response.status_code == 200:
            print("Episode created successfully!")
            pp.pprint(self.podcast_params)
        else:
            print("Error creating episode: ", response.text)
