import calendar
import pprint
import shutil
from datetime import datetime, timedelta
from itertools import cycle
from pathlib import Path
from sys import stdout as terminal
from threading import Thread
from time import sleep

from CreatorPipeline.constants import DEFAULTS
from CreatorPipeline.episode import Episode

pp = pprint.PrettyPrinter(indent=4)


class Directory:
    """Directory object for an episode."""
    full = DEFAULTS.deliver_full
    podcast = DEFAULTS.deliver_podcast
    thumbnail = DEFAULTS.deliver_thumbnail
    shorts = DEFAULTS.deliver_shorts
    posts = DEFAULTS.deliver_posts

    def __init__(self, root):
        self.episode_root = Path(root).resolve()
        self.verify_root()
        self.episode = Episode(self.episode_root.parts[-1])
        pp.pprint(self.episode.__dict__)

    def find_schedule(self):
        """Finds the schedule for the episode."""
        publish_at = f"{self.episode.date_publish} {DEFAULTS.base_timecode}"
        self.root_date = datetime.strptime(publish_at, DEFAULTS.date_format)
        self.root_date += timedelta(hours=DEFAULTS.hour_primary)

    def verify_root(self):
        """Verifies the root directory."""
        try:
            assert self.episode_root.exists()
            assert self.episode_root.is_dir()
        except AssertionError:
            raise "Directory Does not exist: Create"
        dirs = [x.name for x in self.episode_root.iterdir() if x.is_dir()]
        assert "package" in dirs

    def dry_run(self):
        """Dry run for the directory."""
        if self.episode.Queued:
            self.find_schedule()
            self.store = []
            self.run_posts()
            self.run_shorts()
            self.run_podcast()
            self.run_full()

            for x in self.store:
                print(calendar.timegm(x[0].timetuple()), x[1])

    def run_posts(self):
        """Runs the posts for the episode."""
        cur_date = self.root_date - timedelta(days=DEFAULTS.posts_day)
        cur_date += timedelta(hours=DEFAULTS.hour_secondary)
        for post in self.posts:
            self.store.append([cur_date, self.episode_root / post])
            cur_date += timedelta(days=DEFAULTS.posts_day)

    def run_shorts(self):
        """Runs the shorts for the episode."""
        cur_date = self.root_date - timedelta(days=DEFAULTS.short_day)
        for short in self.shorts:
            cur_date += timedelta(days=1)
            self.store.append([cur_date, self.episode_root / short])

    def run_podcast(self):
        """Runs the podcast for the episode."""
        self.store.append([self.root_date, self.episode_root / self.podcast])

    def run_full(self):
        """Runs full for the episode."""
        self.store.append([self.root_date, self.episode_root / self.full])


class DirectoryCreator:
    """Creates the directory for an episode."""
    def __init__(self, episode:Episode):

        self.dirname = episode.abbrv_title
        assert self.dirname, "No Episode Object Provided"
        self.template_episode_dir = (
            DEFAULTS.repo_root / DEFAULTS.template_episode_directory
        )
        self.destination = DEFAULTS.root / DEFAULTS.episode_root / self.dirname
        self.done = False

    def generate_new_episode(self):
        """Generates a new episode directory."""
        print(self.destination)
        if not Path(self.destination).exists():
            t = Thread(target=self.animate)
            t.start()
            try:
                shutil.copytree(self.template_episode_dir, self.destination)
            except Exception as err:
                raise err
            finally:
                sleep(2)
                self.done = True

    def animate(self):
        """Animates the creation of the directory."""
        for c in cycle(["|", "/", "-", "\\"]):
            if self.done:
                break
            terminal.write(f"\rgenerating folder for {self.dirname} {c}")
            terminal.flush()
            sleep(0.1)
        terminal.write("\rDone!    ")
        terminal.flush()


def create_episode_directory(episode):
    """Creates an episode directory."""
    try:
        a = DirectoryCreator(episode)
        print('Directory Object created')
        a.generate_new_episode()
        print("directories made")
        print(f"destination: {a.destination}")
        return a.destination
    except Exception as err:
        print(err)
        print(dir(episode))