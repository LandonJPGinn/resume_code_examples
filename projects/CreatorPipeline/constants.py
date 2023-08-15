import json
import os
from dataclasses import dataclass
from pathlib import Path
from string import Template

import tomllib


class DefaultLoader:
    """Loads the default.toml file. This file contains all the default paths and settings for the pipeline."""
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DefaultLoader, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        local_path = Path(__file__).parent.parent
        database = local_path / os.environ["DATABASE_DEFAULTS"]
        print(database)
        for dd in local_path.iterdir():
            print(dd)

        with open(database, "rb") as f:
            self.__dict__.update(**tomllib.load(f))
        self.gspread = local_path / os.environ["GSPREAD"]

        self.globals()

    def globals(self):
        """Converts all paths to Path objects and sets them as attributes."""
        self.root = Path(self.root)
        self.repo_root = Path(self.repo_root)
        self.show_episode_root = Path(self.root) / self.episode_root
        self.code_root = Path(self.code_root)
        self.docs_root = Path(self.code_root).parent.parent
        self.edit_local_area = Path(self.edit_local_area)
        self.edit_remote_area = Path(self.edit_remote_area)
        self.database_root = self.root / self.database_root
        self.database_sync = self.root / self.database_sync
        self.database_episodes = self.root / self.database_episodes
        self.database_categories = self.root / self.database_categories
        self.database_dashboard = self.root / self.database_dashboard
        self.database_playlists = self.root / self.database_playlists
        self.database_statuses = self.root / self.database_statuses
        self.database_active = self.root / self.database_active
        self.template_deliverables = [getattr(self, d) for d in self.deliverables]

        self.thumbnail_graphics = self.root / self.research_graphics_root
        self.thumbnail_fonts = self.root / self.research_thumb_fonts
        self.thumbnail_backgrounds = self.root / self.research_thumb_backgrounds
        self.thumbnail_subjects = self.root / self.research_thumb_subjects
        self.episode_release_schedule_path = self.repo_root / self.episode_release_schedule_path

    def load_episode_defaults(self, episode=None):
        """Loads the episode defaults for a given episode."""
        if episode:
            if episode.abbrv_title == Path(self.episode_root).name:
                self.episode_root = self.episode_root
            else:
                self.episode_root = self.root / self.episode_root / episode.abbrv_title
        else:
            self.episode_root = Path.cwd()

        episodic = self.episode_root / self.episodic_check
        if not episodic.exists():
            self.thumbnail_topics = ""
            self.thumbnail_output = ""
            return

        self.thumbnail_topics = self.episode_root / self.research_thumb_topics
        self.thumbnail_output = self.episode_root / self.research_thumb_output


@dataclass
class Status:
    """Status class for the episode pipeline."""
    start = "Define"
    research = "Research"
    script = "Script"
    record = "Record"
    edit = "Edit"
    pack = "Package"
    release = "Release"
    market = "Market"
    done = "Complete"
    review = "Review"
    replace = "Replace"

    def __init__(self):
        self.cycle = [
            self.start,
            self.research,
            self.script,
            self.record,
            self.edit,
            self.pack,
            self.release,
            self.market,
            self.done,
            self.review,
            self.replace,
        ]
        self.phase_dir = {
            self.start: "01_define",
            self.research: "02_research",
            self.script: "03_script",
            self.record: "04_record",
            self.edit: "05_edit",
            self.pack: "06_pack",
            self.release: "07_release",
            self.market: "08_market",
            self.review: "09_review",
            self.replace: "10_replace",
        }

    def next_step(self, current_step):
        """Returns the next step in the pipeline."""
        i = self.cycle.index(current_step) + 1
        return self.cycle[i]

    def prev_step(self, current_step):
        """Returns the previous step in the pipeline."""
        i = self.cycle.index(current_step) - 1
        return self.cycle[i]


class Platform:
    """Loads the platform secrets for the episode pipeline."""
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Platform, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        local_path = Path(__file__).parent.parent / os.environ["PLATFORM_SECRETS"]
        for platform_path in local_path.glob("**/*.toml"):
            name = platform_path.stem.split("_")[-1]
            with open(platform_path, "rb") as f:
                self.__dict__.update({name: tomllib.load(f)})

        for client_path in local_path.glob("**/*secrets.json"):
            with open(client_path, "rb") as f:
                self.__dict__.update({"client": json.load(f)})

        self.client_secret = Path(self.youtube["client_secret"]).expanduser().resolve()


class Prompts:
    """Loads the prompt templates for the episode pipeline."""
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Prompts, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        prompt_path = Path(__file__).parent.parent / os.environ["PROMPT_TEMPLATES"]
        with open(prompt_path, "rb") as f:
            data = tomllib.load(f)

        for k, v in data.items():
            if isinstance(v, str):
                data[k] = Template(v)

        with open(prompt_path, "rb") as f:
            self.__dict__.update(**data)


# class Graphics:
#     def __new__(cls):
#         if not hasattr(cls, "instance"):
#             cls.instance = super(Graphics, cls).__new__(cls)
#         return cls.instance

#     def __init__(self):
#         ...

STATUS = Status()
DEFAULTS = DefaultLoader()
PLATFORMS = Platform()
PROMPTS = Prompts()
