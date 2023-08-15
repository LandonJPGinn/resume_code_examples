from datetime import datetime
from pathlib import Path

from CreatorPipeline.constants import DEFAULTS
from CreatorPipeline.database import DatabaseHandler
from CreatorPipeline.episode import Episode


def date_sort(x):
    """Sorts a list of episodes by date."""
    return datetime.strptime(x.get("date_publish"), "%m/%d/%Y")


class ScheduledEpisodes:
    """Class that Informs Queued up Episodes"""

    def __init__(self):
        self.DB = DatabaseHandler().local

    def upcoming(self):
        """Returns a list of upcoming episodes."""
        return sorted(
            [x for x in self.DB.episodes if x.get("Queued")],
            key=date_sort,
        )

    def next(self):
        """Returns the next episode."""
        return self.batch(n=1)[:1]

    def this_week(self):
        """Returns the upcoming 4 episodes."""
        return self.upcoming()[:4]

    def next_week(self):
        """Returns the next 4 episodes."""
        return self.upcoming()[4:8]

    def following_weeks(self):
        """Returns the next next 4 episodes."""
        return self.upcoming()[8:12]

    def batch(self, n=4):
        """Returns the next n episodes."""
        return self.upcoming()[:n]

    def queued(self):
        """Returns a list of queued episodes."""
        return self.upcoming()

    def queued_working(self):
        """Returns a list of queued episodes that are not complete."""
        return [x for x in self.queued() if x.get("Status") not in ("On Hold", "Release", "Market", "Review", "Complete")]
    
    def completed(self):
        """Returns a list of queued episodes that are not complete."""
        return [x for x in self.queued() if x.get("Status") in ("Release", "Market", "Review", "Complete")]
    
    def is_status(self, status):
        """Returns a list of queued episodes that are not complete."""
        if isinstance(status, str):
            status = (status)
        return [x for x in self.queued() if x.get("Status") in status]

    def ready_for_release(self):
        """Returns a list of queued episodes that are ready for release."""
        return [x for x in self.queued() if x.get("Status") == "Package"]

    def needs_dir(self):
        """Returns a list of queued episodes that need a directory."""
        episode_directory = DEFAULTS.root / DEFAULTS.episode_root
        episode_directory = [x.name for x in episode_directory.iterdir()]
        return [
            x for x in self.queued() if x.get("abbrv_title") not in episode_directory
        ]

    def this(self):
        """Returns the current episode."""
        working_dir = Path.cwd().parts[-1]
        return [Episode(working_dir)]


class Scheduler:
    """Enacting Class to perform schedule tasks"""

    def __init__(self):
        self.DB = DatabaseHandler()
        self.Schedule = ScheduledEpisodes()

    def sync_database(self):
        """Syncs the database."""
        self.DB.sync()

    def populate_queued_directories(self):
        """Populates the queued directories."""
        # phase_init.initialize_episodes(self.Schedule.needs_dir())
        ...

    def package_episodes(self):
        """Packages the episodes."""
        ...

    def publish_episodes(self):
        """Publishes the episodes."""
        ...

    def check_reviewable_episodes(self):
        """Checks the reviewable episodes."""
        ...

    def check_replacable_episodes(self):
        """Checks the replacable episodes."""
        ...

    def archive_database_local(self):
        """Archives the database locally."""
        ...

    def archive_database_online(self):
        """Archives the database online."""
        ...
