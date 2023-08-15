#!usr/bin/env python

import shutil
from datetime import datetime, timedelta
from pathlib import Path
import os

# import _episode_pushup
import pytz
import toml
import tomllib
from CreatorPipeline import phase
from CreatorPipeline.constants import DEFAULTS, STATUS
from CreatorPipeline.episode import Episode
from CreatorPipeline.parameters import ReleasePackage


class PhasePackage:
    """Package Phase for an episode to be released."""
    def __init__(self, episode):
        self.episode = episode
        cur_root = Path.cwd()
        self.dirname = cur_root.name
        self.episode_root_dir = DEFAULTS.root / DEFAULTS.episode_root
        self.episode_toml = self.episode_root_dir / DEFAULTS.package_file
        self.copy_files_to_pack()
        self.load_episode_toml()
        self.update_episode_toml()
        self.generate_releases()
        print("Success!")
        self.episode.change_status(STATUS.release)

    def generate_releases(self):
        """Interface call to generate release packages."""
        ReleasePackage(self.episode)

    def load_episode_toml(self):
        """Loads the episode toml file."""
        with open(self.episode_toml, "rb") as f:
            self.tomlpackage = tomllib.load(f)

    def update_episode_toml(self):
        """Updates the episode toml file to clarify release directory locations."""
        new_details = {
            "Title": self.episode.Title,
            "CategoryName": self.episode.Category,
            "CategoryID": self.episode.CategoryID,
            "PlaylistName": self.episode.Playlist,
            "PlaylistID": self.episode.PlaylistID,
            "Full": DEFAULTS.deliver_full[0],
            "Podcast": DEFAULTS.deliver_podcast[0],
            "Short1": DEFAULTS.deliver_shorts[0],
            "Short2": DEFAULTS.deliver_shorts[1],
            "Short3": DEFAULTS.deliver_shorts[2],
            "Thumbnail": DEFAULTS.deliver_thumbnail[0],
            "Markers": DEFAULTS.edit_markers,
            "ScheduleTo": self.format_timezone(),
            "Short1_ScheduleTo": self.format_timezone(5),
            "Short2_ScheduleTo": self.format_timezone(3),
            "Short3_ScheduleTo": self.format_timezone(1),
        }

        self.tomlpackage.update(**new_details)
        with open(self.episode_toml, "w") as f:
            data = toml.dumps(self.tomlpackage)
            f.write(data)

    def copy_files_to_pack(self):
        """Collects all required files for release and copies them to the release directory."""
        rendered = Path(DEFAULTS.edit_root).glob("**/*.*")
        for src in rendered:
            src = str(src.expanduser().resolve().as_posix())
            dest = src.replace(DEFAULTS.edit_renders, DEFAULTS.package_media)
            try:
                shutil.copy2(src, dest)
            except shutil.SameFileError as err:
                print(err)

    def get_episode_root(self):
        """Returns the episode root directory."""
        return DEFAULTS.root / DEFAULTS.episode_root

    def format_timezone(self, offset=0):
        """Formats the timezone for the episode to be released."""
        _date = datetime.strptime(self.episode.date_launch, "%m/%d/%Y") - timedelta(
            days=offset
        )
        timezone = pytz.timezone(DEFAULTS.timezone)
        return str(timezone.localize(_date).isoformat())


def main(episodes):
    """Main function for the package phase."""
    for ep in episodes:
        episode = Episode(ep)
        assert episode
        assert episode.date_launch
        assert episode.abbrv_title
        episode_path = DEFAULTS.root / DEFAULTS.episode_root / episode.abbrv_title
        assert episode_path.exists()
        os.chdir(episode_path)

        PhasePackage(episode)

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description="Package Episodes for Release"
#     )
#     parser.add_argument(
#         "episodes", type=str, nargs="+", help="push episode(s) to package"
#     )
#     args = parser.parse_args()
#     given_episodes = args.episodes if args.episodes else [Path.cwd().name]
#     main(given_episodes)



if __name__ == "__main__":
    episodes = phase.episode_args(_description="Package Episodes for Release", _help="push episode(s) to package")
    phase.run_phase(PhasePackage, episodes)