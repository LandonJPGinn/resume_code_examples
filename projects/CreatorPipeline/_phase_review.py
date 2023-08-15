#!usr/bin/env python


# from CreatorPipeline import phase
# from CreatorPipeline.constants import STATUS

# params = [[Path.cwd().parts[-1]], STATUS.review]

# if phase.check_phase_deliverables(*params):
#     phase.set_phase(*params)
# else:
#     print("Not Ready Yet")

class PhaseAnalytics:
    """Analytics Phase for an episode. Indicates episode is ready to analyze."""
    def __init__(self, episode):
        self.episode = [episode]
        #initialize_episodes(self.episode)