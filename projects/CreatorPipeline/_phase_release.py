#!usr/bin/env python

import os
import argparse
import json
import tomllib
from pathlib import Path

from CreatorPipeline.constants import DEFAULTS, STATUS
from CreatorPipeline.episode import Episode
from CreatorPipeline.publisher import PublishFactory
from CreatorPipeline.schedule import ScheduledEpisodes
from CreatorPipeline.database import ActiveEpisodeDatabase

# Todo: make sure the newly added sequence of privacy statuses with comments is working.
class PackageFinder:
    """Finds all packages ready for release."""
    def __init__(self) -> None:
        self.packages = []

        ready_episodes = ScheduledEpisodes().ready_for_release()
        for ep in ready_episodes:
            ep_path = DEFAULTS.root / DEFAULTS.episode_root / DEFAULTS.release_path
            self.get_packages(ep_path)

        self.packages = list(set(self.packages))

    def load_episode_toml(self):
        """Loads the episode toml file."""
        self.episode_toml = self.get_episode_root() / DEFAULTS.package_file
        with open(self.episode_toml, "rb") as f:
            self.tomlpackage = tomllib.load(f)

    def get_packages(self, path):
        """Gets all packages from a given path."""
        package_files = [x for x in path.iterdir() if x.is_dir() and x.name.startswith("release.json")]
        for release in package_files:
            with open(release, "r"):
                data = json.load()
            for k, v in data.items():
                self.packages += v


class PhaseRelease:
    """Release Phase for an episode. Indicates episode is ready to release."""
    def __init__(self, episode):
        self.episode = episode

        self.releases = {}
        self.root = Path.cwd()

        self.episode_est = self.root.name
        self.package_path = self.root / DEFAULTS.package_root
        self.release_file = self.root / DEFAULTS.release_path

        assert (
            self.release_file.exists()
        ), f"No Release.json found at: {self.release_file}"

        self.get_releases()
        self.validate_episode()
        self.submit_releases()

    def get_releases(self):
        """Gets all releases from the release.json file."""
        with open(self.release_file, "r", encoding="utf8") as f:
            self.releases = json.load(f)

    def validate_episode(self):
        """Validates the episode."""
        self.episode = Episode(self.episode_est)
        assert self.episode

    def submit_releases(self):
        """Submits all releases to the appropriate platform."""
        print("\nSubmitting Releases")
        for release in self.releases.get(self.episode_est, [{}]):
            publish = PublishFactory(release)
            publish.publish()
        print("\nReleases Submitted; Changing Status to Complete")
        self.episode.change_status(STATUS.complete)
        self.update_vidID()
        print("\nStatus Changed to Complete; Video ID Updated")

    def update_vidID(self):
        """Updates the video ID for the episode."""
        id_file = self.package_path / "vidId.txt" #Todo move to constsants
        vidId = id_file.read_text()
        self.episode.change_videoId(vidId)


def main(episodes):
    """Main function for release phase."""
    for ep in episodes:
        episode = Episode(ep)
        assert episode
        assert episode.date_launch
        assert episode.abbrv_title
        episode_path = DEFAULTS.root / DEFAULTS.episode_root / episode.abbrv_title
        assert episode_path.exists()
        os.chdir(episode_path)

        PhaseRelease(episode)
        ActiveEpisodeDatabase().release_episode(episode.ID)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Release Episodes for Release"
    )
    parser.add_argument(
        "episodes", type=str, nargs="+", help="push episode(s) to release"
    )
    args = parser.parse_args()
    given_episodes = args.episodes if args.episodes else [Path.cwd().name]

    main(given_episodes)


# Todo: Setup send to queue.