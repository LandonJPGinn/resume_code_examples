import pprint
from datetime import date

from CreatorPipeline.database import DatabaseHandler
from CreatorPipeline.identifier import identifier_factory

pp = pprint.PrettyPrinter(indent=4)


def data_factory(sheet, cells):
    """Returns data from a worksheet in a list of dictionaries"""
    if cells == "all":
        return sheet.get_all_records()
    return sheet.get(cells)


class Episode:
    """ Episode Class """
    def __init__(self, identifier):
        print(f"Now loading episode for {identifier=}")
        self.identifier = identifier_factory(identifier)
        self.DB = DatabaseHandler()
        self.find_db_row()
        self.today = date.today().strftime("%d/%m/%Y")

    def change_status(self, status: str):
        """Change the status of the episode"""
        try:
            col = self.DB.online.episode_headers.index("Status") + 1
            self.DB.online.episode_worksheet.update_cell(self.Number + 1, col, status)
            self.Status = status
            print(f"Status for cell {self.Title}{col} changed to {status}")
        except Exception as err:
            print(err)

    def change_videoId(self, videoId: str):
        """Change the videoId of the episode"""
        try:
            col = self.DB.online.episode_headers.index("VideoID") + 1
            self.DB.online.episode_worksheet.update_cell(self.Number + 1, col, videoId)
            self.videoId = videoId
            print(f"videoId for cell {self.Title}{col} changed to {videoId}")
        except Exception as err:
            print(err)

    def find_db_row(self):
        """Only Local Read"""
        episodes = self.DB.local.episodes
        param = list(episodes[0].keys())[self.identifier.col - 1]
        data = next(
            (row for row in episodes if row[param] == self.identifier.value), {}
        )
        print(data)
        self.__dict__.update(**data)

    def queue_up(self):
        """Set Episode to Queue Up"""
        newest_row = min(
            [
                x.get("Count")
                for x in self.DB.online.dashboard
                if not x.get("ID") and isinstance(x.get("Count"), int)
            ],
        )
        col = self.DB.online.schedule_headers.index("ID") + 1
        self.DB.online.schedule_worksheet.update_cell(newest_row + 3, col, self.ID)

    def resync(self):
        """Resync Episode"""
        # self.DB.sync()
        # self.find_db_row()
        ...

    def has_started(self):
        """Check if episode has started"""
        return self.Status != ""

    def is_queued(self):
        """Check if episode is queued"""
        try:
            return self.Queued
        except Exception as err:
            print(err)
            print(self)
            return False

    def is_upcoming(self):
        """Check if episode is upcoming"""
        if self.is_queued():
            return self.today < self.date_start

    def is_current(self):
        """Check if episode is current"""
        if self.is_queued():
            return self.today >= self.date_start and self.today <= self.date_publish

    def is_past_deadline(self):
        """Check if episode is past deadline"""
        if self.is_queued():
            return self.today > self.date_publish

    def is_completed(self):
        """Check if episode is completed"""
        return self.Status == "Complete"

    def summarize(self):
        """Prints a summary of the episode"""
        print("\n")
        print("-" * 60)
        print(f"{self.__class__=}")
        q = self.is_queued()
        print(f"Status: {q}")
        for k, v in self.__dict__.items():
            print(f"\t{k: <35}{v}")
        print("-" * 60)

    def dir_exists(self):
        """Check if episode directory exists"""
        self.DB.abbrv_title

    def check_deliverables(self, phase=None) -> bool:
        """Check if deliverables exist for a phase"""
        # Get phase deliverable requirements
        # check if all exist in file
        # check if any size == 0
        return True


## Random Tests


# print("Rows: ", wks.row_count)
# wks.col_count

# #cell
# wks.acell("A9").value

# wks.cell(3,4)#down 3, over 4

# wks.get("A7:E9")
# get list of lists, each reps a row


# ep_wks.update("G4", "Research")


# wks.update("A3", "Value")
# wks.update("D2:E3", [["Engineer", "Tennis"],["Business", "Pottery"]])
# wks.update("F2","=UPPER(E2)", raw=False)# to evaluate

# wks.delete_rows(25)

# TEST check if database is persistent
# a = DatabaseHandler()
# b = StatusChanger()
# c = Episode("G16")
# # print(a)
# # print(b.DB)
# # print(b.DB is a)


# b.change_episode_status(c, "Market")


# epi = Episode("are_3d_artists_p")

# pp.pprint(epi.__dict__)

# print(epi.is_current())
# print(epi.is_past_deadline())
# epi.summarize()
