from CreatorPipeline.episode import Episode
from pathlib import Path

if __name__ == "__main__":
    ep_name = Path(".").resolve().name
    current_episode = Episode(ep_name)
    print(current_episode.Status)
