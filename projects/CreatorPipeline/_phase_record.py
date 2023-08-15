#!usr/bin/env python
from CreatorPipeline import phase
from CreatorPipeline.constants import STATUS


class PhaseRecord:
    """Record Phase for an episode. Indicates episode is ready to record."""
    def __init__(self, episode):
        self.episode = episode
        #initialize_episodes(self.episode)
        # Setup prompter
        # setup directories

        self.episode.change_status(STATUS.record)


if __name__ == "__main__":
    episodes = phase.episode_args(_description="Ready Episode for Recording", _help="push episode(s) to record")
    phase.run_phase(PhaseRecord, episodes)