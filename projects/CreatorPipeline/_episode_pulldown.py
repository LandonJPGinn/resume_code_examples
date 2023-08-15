from pathlib import Path
import shutil


# Todo: Episodes should include a path awareness
def pulldown(episode):
    """Pulls down an episode from the cloud."""
    cloud_path = Path()  # is dir
    local_root = Path()
    local_path = local_root.with_name(cloud_path.name)
    if local_path.exists:
        action = input(
            "local version found\n (O)verwrite | (S)kip New Files | (C)ancel"
        )
        if action.lower() == "c":
            return
        if action.lower() == "s":
            all_files = cloud_path.glob("**/*.*")
            for file in all_files:
                dest = str(file).replace(cloud_path, local_path)
                if not dest.exists():
                    shutil.copy2(str(file), dest)

        if action.lower() == "o":
            shutil.copytree(cloud_path, local_path, dirs_exist_ok=True)
