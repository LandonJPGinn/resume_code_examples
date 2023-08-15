from CreatorPipeline.database import DatabaseSynchronizer
from CreatorPipeline.database import ActiveEpisodeDatabase
from CreatorPipeline.schedule import ScheduledEpisodes

if __name__ == "__main__":
    synch = DatabaseSynchronizer()
    synch.sync_local()
    AED = ActiveEpisodeDatabase()
    SE = ScheduledEpisodes()
    AED.active["active"] = list(set([x.get("ID") for x in SE.queued_working()]))
    AED.active["released"] = list(set([x.get("ID") for x in SE.completed()]))
    AED.save()