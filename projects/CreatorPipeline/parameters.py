import json
from pathlib import Path

import tomllib
from CreatorPipeline.constants import DEFAULTS, PROMPTS


class ReleasePackage:
    """Creates a release package for an episode."""
    def __init__(self,episode):
        self.episode = episode
        self.cur_root = Path.cwd()
        self.dirname = self.cur_root.name
        
        self.episode_directory = DEFAULTS.root / DEFAULTS.episode_root
        episode_default_file = self.episode_directory / DEFAULTS.package_file

        with open(episode_default_file, "rb") as f:
            self.tomlpackage = tomllib.load(f)
        self.release_package = {self.dirname: []}

        self.gather_existing_deliverables()
        self.combine_description_details()
        self.generate_top_comment()
        self.create_release_object()

        self.save()

    def combine_description_details(self):
        """Combines the description details for the episode."""
        markers_file = self.episode_directory / DEFAULTS.edit_markers
        description_file = self.episode_directory / DEFAULTS.define_description

        with open(markers_file, "r", encoding="UTF-8") as f:
            markers = f.read()

        with open(description_file, "r", encoding="UTF-8") as f:
            desc = f.read()

        self._description = PROMPTS.Description
        self._description = str(
            self._description.substitute(MARKERS=markers, DESCRIPTION=desc)
        )
        # self._description.replace(r"{{Insert description of video here}}", self.Description)# Where is this coming from?

    def generate_top_comment(self):
        """Generates the top comment for the episode."""
        self._top_comment = PROMPTS.pinned_comment.substitute(QOTD=Path(DEFAULTS.define_qotd).read_text())

    def gather_existing_deliverables(self):
        """Gathers all existing deliverables for the episode."""
        self.real_deliverables = []
        for delivery_list in DEFAULTS.template_deliverables:
            for delivery_path in delivery_list:
                d_path = self.episode_directory / delivery_path
                if d_path.exists():
                    self.real_deliverables.append(d_path)
        self.real_deliverables.sort()

    def create_release_object(self):
        """Creates the release object for the episode."""
        for media_path in self.real_deliverables:
            release = {}
            if "Full" in media_path.stem:
                print(f"\nFound Youtube: {media_path.stem}")
                release = self.youtube_video_release(
                    str(media_path.expanduser().resolve())
                )

            elif "Short" in media_path.stem:
                print(f"\nFound Short: {media_path.stem}")
                release = self.youtube_short_release(
                    str(media_path.expanduser().resolve())
                )

            elif "Podcast" in media_path.stem:
                print(f"\nFound Podcast: {media_path.stem}")
                release = self.buzzsprout_podcast_release(
                    str(media_path.expanduser().resolve())
                )
            if release:
                self.release_package[self.dirname].append(release)

    def save(self):
        """Saves the release package to the episode directory."""
        release_path = self.episode_directory / DEFAULTS.release_path
        with open(release_path, "w", encoding="utf8") as f:
            json.dump(self.release_package, f, indent=4, ensure_ascii=False)

    def youtube_video_release(self, media_path):
        """Creates a youtube video release object."""
        return {
            "_platform": "Youtube Video",
            "publishAt": self.tomlpackage.get("ScheduleTo"),
            "channelId": DEFAULTS.channelId,
            "title": self.tomlpackage.get("Title"),
            "description": self._description,
            "tags": DEFAULTS.Tags,
            "categoryId": self.tomlpackage.get("CategoryID"),
            "playlistId": self.tomlpackage.get("PlaylistID"),
            "thumbnail_file": self.tomlpackage.get("Thumbnail"),
            "media_file": media_path,
            "textOriginal": self._top_comment,
        }

    def youtube_short_release(self, media_path):
        """Creates a youtube short release object."""
        n = Path(media_path).stem
        part = n.split("_")[-1]
        return {
            "_platform": "Youtube Video",
            "publishAt": self.tomlpackage.get(f"{n}_ScheduleTo"),
            "channelId": DEFAULTS.channelId,
            "title": self.tomlpackage.get("Title") + part,
            "description": self._description,
            "tags": DEFAULTS.Tags,
            "categoryId": self.tomlpackage.get("CategoryID"),
            "playlistId": self.tomlpackage.get("PlaylistID"),
            # "thumbnail_file": self.tomlpackage.get("Thumbnail"),
            "media_file": media_path,
        }

    def buzzsprout_podcast_release(self, media_path):
        """Creates a buzzsprout podcast release object."""
        return {
            "_platform": "Buzzsprout Podcast",
            "title": self.tomlpackage.get("Title"),
            "description": self._description,
            "explicit": False,
            "private": True,
            "audio_file": media_path,
            "published_at": self.tomlpackage.get("ScheduleTo"),
            "email_user_after_audio_processed": True,
            "tags": DEFAULTS.Tags,
        }
