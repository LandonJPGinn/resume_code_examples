import shutil
from CreatorPipeline.constants import STATUS, DEFAULTS


def PhaseEditSetup(episode):
    """Copies the episode from the cloud to the local edit area."""
    local = DEFAULTS.edit_local_area / episode.abbrv_title
    remote = DEFAULTS.edit_remote_area / episode.abbrv_title
    shutil.copytree(remote, local)
    episode.change_status(STATUS.edit)

def PhaseEditFinish(episode):
    """Copies the episode from the local edit area to the cloud."""
    print("\n\n")
    check = input("Are you sure you want to finish editing? Y/n")
    if check.lower() == "y":
        local = DEFAULTS.edit_local_area / episode.abbrv_title
        remote = DEFAULTS.edit_remote_area / episode.abbrv_title
        shutil.copytree(local, remote, dirs_exist_ok=True)
        episode.change_status(STATUS.pack)
    print("\n\n")
