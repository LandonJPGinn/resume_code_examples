import pprint
import time
import httplib2
from apiclient.http import MediaFileUpload
from authenticator import PlatformAuth as Auth
from constants import PLATFORMS
from requests.exceptions import HTTPError
from pathlib import Path

pp = pprint.PrettyPrinter(indent=4)


class YoutubeEpisodePublisher:
    """Youtube Publisher Interface"""
    def __init__(self, content):
        self.__dict__.update(**PLATFORMS.youtube)
        self.__dict__.update(**content)
        self.youtube = Auth().youtube()

    def video_params(self):
        """Returns the video parameters for the youtube video."""
        return {
            "snippet": {
                "publishAt": self.publishAt,
                "channelId": self.channelId,
                "title": self.title,
                "description": self.description,
                "tags": self.tags,
                "categoryId": self.categoryId,
            },
            "status": {
                "privacyStatus": "private",
                "publishAt": self.publishAt,
                "madeForKids": False,
            },
        }

    def message_params(self):
        """Returns the message parameters for the youtube video."""
        return {
            "snippet": {
                "title": self.title,
                "channelId": self.channelId,
                "textOriginal": self.textOriginal,
                "isPublic": False,
                "scheduledStartTime": self.scheduledTime.isoformat() + "Z",
            }
        }

    def publish_video(self):
        """Publishes the video to youtube."""
        try:
            video_response = self.youtube.videos().insert(
                part="snippet,status",
                body=self.video_params(),
                media_body=MediaFileUpload(
                    self.media_file,
                    chunksize=-1,
                    resumable=True,
                ),
            )
            vid = resumable_upload(video_response)

            if self._platform == "Youtube Video":
                thumbnail_response = (
                    self.youtube.thumbnails()
                    .set(
                        videoId=vid["id"],
                        media_body=MediaFileUpload(self.thumbnail_file),
                    )
                    .execute()
                )
        except HTTPError:
            print("An HttpError Occurred:\n{e}")

        if vid:
            _id = vid["id"]
            _thumb = thumbnail_response["items"][0]["default"]["url"]
            print(f"Video uploaded successfully with ID: {_id}")
            print(f"Thumbnail set successfully with URL: {_thumb}")
            self.update_vidId(_id)
            self.set_unlisted(vidId=_id)
            self.add_comment(vidId=_id)
            self.pin_comment(vidId=_id)
            self.add_to_playlist(vidId=_id)
            self.add_next_video(vidId=_id)
            self.set_scheduled(vidId=_id)

        print("Publisher Ran")

    def set_unlisted(self, vidId):
        """Sets the video to unlisted."""
        self.youtube.videos().update(videoId=vidId, part="status", body={"status": {"privacyStatus": "unlisted"}}).execute()

    def set_scheduled(self, vidId):
        """Sets the video to scheduled."""
        self.youtube.videos().update(videoId=vidId, part="status", body={"status": {"privacyStatus": "private", "publishAt": self.publishAt}}).execute()

    def add_comment(self, vidId):
        """Adds a comment to the video."""
        self.comment = self.youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "channelId": self.channelId,
                    "videoId": vidId,
                    'isPublic': True,
                    "topLevelComment": {
                        "snippet": {
                            "textOriginal": self.textOriginal,
                            'viewerRating': 'positive'
                        }
                    },
                }
            },
        ).execute()

    def pin_comment(self, video_id):
        """Pins the comment to the top of the video."""
        self.youtube.comments().setModerationStatus(
            id=self.comment["id"],
            moderationStatus="published"
        ).execute()

    def add_to_playlist(self, vidId):
        """Adds the video to the playlist."""
        self.youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": self.playlistId,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": vidId,
                    },
                },
                "position": 0,
            },
        ).execute()

    def update_vidId(self, vidId):
        """Updates the video ID for the episode."""
        id_file = Path(self.media_file).parents[1].joinpath("vidId.txt")
        id_file.touch()
        id_file.write_text(vidId)

    def publish_message(self):
        """Publishes the message to youtube."""
        # Todo: Youtube deprecated this feature
        try:
            response = (
                self.youtube.activities()
                .insert(part="snippet", body=self.message_params())
                .execute()
            )
        except HTTPError:
            print("An HttpError Occurred:\n{e}")

        if response:
            print("Community post scheduled successfully!")
        else:
            print(f"Error scheduling community post: {response}")
    
    def add_next_video(self, vidId):
        """Adds cards to the video."""
        # get the video id of the next video as list
        YouTubeCardManager(self.youtube, vidId, self.next_video).add_cards_to_video()


class YouTubeCardManager:
    """Youtube Post Episode Card Handler Class"""
    def __init__(self, youtube, video_id, cards):
        self.youtube = youtube
        self.video_id = video_id
        self.cards = cards

    def add_cards_to_video(self):
        """Adds cards to the video."""
        promoted_items = []
        for card_id, timing in self.cards.items():
            promoted_items.append({
                "kind": "youtube#promotedItemId",
                "videoId": self.video_id,
                "timing": {
                    "type": "offsetFromStart",
                    "offsetMs": timing,
                },
                "customMessage": "Check out my other videos!",
                "promotedByContentOwner": False,
            })

        try:
            self.youtube.promotedItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "type": "video",
                        "videoId": self.video_id,
                        "promotedItems": promoted_items,
                    },
                },
            ).execute()
            
            print("Cards added successfully!")
        
        except HTTPError as error:
            print(f"An error occurred: {error}")
        

        """

            Example Usage: Maybe a column in the spread sheet can become

            cardID@timing, cardID@timing, cardID@timing

            Maybe the ID needs to be hash in spreadsheet, and then the hash is used to get the video ID
            The very least there should be one set at the last 10 seconds of the video
            
            This is already pre-planned in the script, but maybe it needs to be a column
            Generated by markers or manually?
            
            cards = {
                "card1": 10000,  # 10 seconds
                "card2": 20000,  # 20 seconds
                "card3": 30000,  # 30 seconds
            }

            card_manager = YouTubeCardManager(youtube, video_id, cards)

            card_manager.add_cards_to_video()

        """




def resumable_upload(upload_request):
    """Resumable Upload"""
    MAX_RETRY = 5
    response = None
    retry_count = 0
    wait_time = 1
    while not response:
        try:
            status, response = upload_request.next_chunk()
            if response.get("id", None):
                print("Success")

        except (httplib2.HttpLib2Error, IOError):
            if retry_count > MAX_RETRY:
                exit("Giving Up")

            retry_count += 1
            wait_time += retry_count

            print(f"Sleeping {wait_time} seconds before retry.")
            time.sleep(wait_time)
    return response
