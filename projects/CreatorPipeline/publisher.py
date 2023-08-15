"""Simplification Layer for PublishFactory."""
import pprint

from platforms.__youtube import YoutubeEpisodePublisher

pp = pprint.PrettyPrinter(indent=4)


class PublishError:
    """Error Publisher"""
    def publish(self):
        """Publishes the error."""
        print("Error Occured. Check Release Params:")
        pp.pprint(self.params)


class PublishVideoYT:
    """Youtube Video Publisher"""
    def publish(self):
        """Publishes the video to youtube."""
        YEP = YoutubeEpisodePublisher(self.params)
        YEP.publish_video()


class PublishShortYT:
    """Youtube Short Publisher"""
    def publish(self):
        """Publishes the short to youtube."""
        YEP = YoutubeEpisodePublisher(self.params)
        YEP.publish_video()


class PublishMessageYT:
    """Youtube Message Publisher"""
    def publish(self):
        """Publishes the message to youtube."""
        YEP = YoutubeEpisodePublisher(self.params)
        YEP.publish_message()


class PublishPodcastBuzzsprout:
    """Buzzsprout Podcast Publisher"""
    def publish(self):
        """Publishes the podcast to buzzsprout."""
        print("Skipping BuzzSprout")
        # BEP = BuzzsproutEpisodePublisher(self.params)
        # BEP.publish()


_publishFactory = {
    "Youtube Video": PublishVideoYT,
    "Youtube Short": PublishShortYT,
    "Youtube Message": PublishMessageYT,
    "Buzzsprout Podcast": PublishPodcastBuzzsprout,
    "Error": PublishError,
}


class PublishFactory:
    """Factory for publishing objects."""
    def __new__(cls, params):
        obj = _publishFactory.setdefault(params.get("_platform", None), "Error")
        publish_object = super(PublishFactory, cls).__new__(obj)
        publish_object.params = params
        return publish_object

    def publish(self):
        """Publishes the object."""
        ...


class Params:
    """Params object for PublishFactory."""
    def __init__(self, params):
        self.__dict__.update(**params)
