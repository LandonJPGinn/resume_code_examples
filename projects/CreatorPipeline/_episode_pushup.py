from pathlib import Path
import shutil


# Todo: Episodes should include a path awareness
def pushup(episode):
    """Pushes up an episode to the cloud."""
    local_path = Path()  # is dir
    cloud_root = Path()
    cloud_path = cloud_root.with_name(local_path.name)
    shutil.copytree(local_path, cloud_path, dirs_exist_ok=True)
