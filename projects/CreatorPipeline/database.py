import json
from datetime import datetime
from itertools import cycle
from sys import stdout as terminal
from threading import Thread
from time import sleep

import gspread
from CreatorPipeline.constants import DEFAULTS

def data_factory(sheet, cells):
    """Returns data from a worksheet in a list of dictionaries"""
    if cells == "all":
        return sheet.get_all_records()

    values = sheet.get(cells)

    if not isinstance(values, (list, dict)):
        return [values]
    return values


class DatabaseSynchronizer:
    """Synchronizes local database with online database"""
    def __init__(self):
        """Initializes the database synchronizer
        """
        _handler = DatabaseHandler()
        self.online = _handler.online
        self.local = _handler.local

    def is_local_current(self):
        """Checks if the local database is current"""
        return self.online.latest == self.local.latest

    def sync_local(self):
        """Syncs the local database with the online database"""
        # Todo: Get this working
        # if self.is_local_current():
        #     return
        print("store to local " + str(DEFAULTS.database_episodes))

        """stores information from online into local db. set Sync Timestamp in state worksheet"""
        DEFAULTS.database_categories.write_text("\n".join(self.online.categories))
        DEFAULTS.database_playlists.write_text("\n".join(self.online.playlists))
        DEFAULTS.database_statuses.write_text("\n".join(self.online.statuses))
        json.dump(
            self.online.dashboard,
            DEFAULTS.database_dashboard.open(mode="w"),
            indent=4,
        )
        json.dump(
            self.online.episodes,
            DEFAULTS.database_episodes.open(mode="w"),
            indent=4,
        )

        self.online.timestamp()

        json.dump(
            self.online.state_timestamp,
            DEFAULTS.database_sync.open(mode="w"),
            indent=4,
        )


class LocalDatabase:
    """Local Database for the Creator Pipeline

    This class is a singleton. It is used to store the local database
    """
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(LocalDatabase, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self):
        if self.__initialized:
            return

        self.dashboard = json.load(DEFAULTS.database_dashboard.open())
        self.episodes = json.load(DEFAULTS.database_episodes.open())
        self.categories = DEFAULTS.database_categories.read_text()
        self.playlists = DEFAULTS.database_playlists.read_text()
        self.statuses = DEFAULTS.database_statuses.read_text()
        self.state_timestamp = json.load(DEFAULTS.database_sync.open())

        self.latest_time()

        self.__initialized = True

    def latest_time(self):
        """Gets the latest time from the state timestamp"""
        if not self.state_timestamp:
            self.latest = datetime.strptime(
                datetime.now().strftime(DEFAULTS.timestamp_format),
                DEFAULTS.timestamp_format,
            )
            return
        self.latest = datetime.strptime(
            max(self.state_timestamp[0].values()), DEFAULTS.timestamp_format
        )


class OnlineDatabase:
    """Online Database for the Creator Pipeline"""
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(OnlineDatabase, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self):
        if self.__initialized:
            return
        self.service_account = gspread.service_account(filename=DEFAULTS.gspread)
        self.sheet = self.service_account.open(DEFAULTS.service_account)

        self.episode_worksheet = self.sheet.worksheet(DEFAULTS.episode_worksheet)
        self.schedule_worksheet = self.sheet.worksheet(DEFAULTS.schedule_worksheet)
        self.type_worksheet = self.sheet.worksheet(DEFAULTS.type_worksheet)
        self.state_worksheet = self.sheet.worksheet(DEFAULTS.state_worksheet)
        self.dashboard = data_factory(self.schedule_worksheet, DEFAULTS.episodes)
        self.episodes = data_factory(self.episode_worksheet, DEFAULTS.episodes)
        self.categories = data_factory(self.type_worksheet, DEFAULTS.categories)
        self.playlists = data_factory(self.type_worksheet, DEFAULTS.playlists)
        self.statuses = data_factory(self.type_worksheet, DEFAULTS.statuses)
        self.state_timestamp = data_factory(
            self.state_worksheet, DEFAULTS.sync_timestamps
        )
        self.clean_lists()

        self.episode_headers = self.episode_worksheet.row_values(1)
        self.schedule_headers = self.schedule_worksheet.row_values(1)
        self.state_header = self.state_worksheet.row_values(1)
        self.latest_time()

        self.__initialized = True

    def clean_lists(self):
        """Cleans the lists from the database"""
        self.categories = dict(self.categories)
        self.playlists = dict(self.playlists)
        self.statuses = dict(self.statuses)

    def latest_time(self):
        """Gets the latest time from the state timestamp"""
        if not self.state_timestamp:
            self.latest = datetime.strptime(
                datetime.now().strftime(DEFAULTS.timestamp_format),
                DEFAULTS.timestamp_format,
            )
            return
        self.latest = datetime.strptime(
            max(self.state_timestamp[0].values()), DEFAULTS.timestamp_format
        )

    def timestamp(self):
        """Sets the timestamp for the state worksheet"""
        timestamp = str(datetime.now().strftime(DEFAULTS.timestamp_format))
        self.state_worksheet.append_row([timestamp], table_range="A1")


class DatabaseHandler:
    """Allows swapping between Database modes"""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(DatabaseHandler, cls).__new__(cls)
            cls.instance.__initialized = False
        return cls.instance

    def __init__(self):
        if self.__initialized:
            return

        self.done = False
        t = Thread(target=self.animate)
        t.start()
        try:
            self.online = OnlineDatabase()
            self.local = LocalDatabase()
        except Exception as err:
            print(err)
            raise err
        finally:
            self.__initialized = True
            self.done = True

    def animate(self):
        """Animates the loading of the database"""
        for c in cycle(["|", "/", "-", "\\"]):
            if self.done:
                break
            terminal.write(f"\rloading database {c}")
            terminal.flush()
            sleep(0.1)
        terminal.flush()


class ActiveEpisodeDatabase:
    """Database for active episodes"""
    def __init__(self):
        with open(DEFAULTS.database_active, 'r') as f:
            data = json.load(f)
        self.active = data
    
    def clean(self):
        """Cleans the active database"""
        self.active["active"] = list(set(self.active.get("active")))
        self.active["released"] = list(set(self.active.get("released")))

    def save(self):
        """Saves the active database"""
        with open(DEFAULTS.database_active, 'w') as f:
            json.dump(self.active, f, indent=4)

    def add_episode(self, episode):
        """Adds an episode to the active database"""
        try:
            self.active.get("active").append(episode)
            self.save()
        except AttributeError as err:
            print(err)
            print(self.active)

    def release_episode(self, episode):
        """Releases an episode from the active database"""
        self.active.get("active").remove(episode)
        self.active.get("released").append(episode)
        self.clean()
        self.save()

DatabaseHandler()
