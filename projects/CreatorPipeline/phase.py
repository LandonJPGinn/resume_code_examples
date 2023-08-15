import sys
import os
import argparse
from pathlib import Path
from CreatorPipeline.constants import DEFAULTS, STATUS
from CreatorPipeline.episode import Episode

# Phases
from CreatorPipeline._phase_initialize import PhaseBuild
from CreatorPipeline._phase_research import PhaseResearch
from CreatorPipeline._phase_script import PhaseScript
from CreatorPipeline._phase_record import PhaseRecord
from CreatorPipeline._phase_edit import PhaseEditSetup, PhaseEditFinish
from CreatorPipeline._phase_package import PhasePackage
from CreatorPipeline._phase_release import PhaseRelease
from CreatorPipeline._phase_review import PhaseAnalytics

"""
phase constructor loads up phase to return
"""


def runner(phase):
    """Decorator to run a phase."""
    def internal_func(*args, **kwargs):
        """Internal function to run a phase."""
        print(f"running phase {phase.__name__} - {args} - {kwargs}")
        try:
            phase(*args, **kwargs)
            print("completed")
            code = 0
        except Exception as e:
            print(e)
            code = 1
        sys.exit(code)
    return internal_func


class PhaseRunner:
    """Phase Runner for an episode."""
    def __init__(self, episode, skip=False):
        self.episode = episode
        self.skip = skip
        self.set_episode()

    @runner
    def Build(self):
        """Interface to run build commands"""
        print(f"Building Episode {self.episode}")
        PhaseBuild(self.episode)

    @runner
    def Research(self):
        """Interface to run research commands"""
        PhaseResearch(self.episode)

    @runner
    def Script(self):
        """Interface to run script commands"""
        PhaseScript(self.episode)
    
    @runner
    def Record(self):
        """Interface to run record commands"""
        PhaseRecord(self.episode)
    
    @runner
    def Plan(self):
        """Interface to run plan commands"""
        print("Planning Script")
        PhaseScript(self.episode)
        x = input("Press Any Key to continue if Script is ready (0 to quit)...")
        if x == "0":
            sys.exit(0)
        PhaseRecord(self.episode)
        print("Set to Record")
    
    @runner
    def Edit_Setup(self):
        """Interface to run edit commands"""
        PhaseEditSetup(self.episode)
    
    @runner
    def Edit_Finish(self):
        """Interface to run edit commands"""
        PhaseEditFinish(self.episode)
    
    @runner
    def Render(self):
        """Interface to run render commands"""
        print("Not implemented yet")

    @runner
    def Package(self):
        """Interface to run package commands"""
        PhasePackage(self.episode)
    
    @runner
    def Release(self):
        """Interface to run release commands"""
        PhaseRelease(self.episode)
    
    @runner
    def Analytics(self):
        """Interface to run analytics commands"""
        print("Not implemented yet")
        PhaseAnalytics(self.episode)
    
    def set_episode(self):
        """Set the episode to the current episode."""
        DEFAULTS.load_episode_defaults(self.episode)
        episode_path = DEFAULTS.root / DEFAULTS.episode_root
        print(episode_path)
        print(DEFAULTS.episode_root)
        if not self.skip:
            assert episode_path.exists(), f"{episode_path} path wasn't found"
            os.chdir(episode_path)


class Phase:
    """Phase for an episode."""
    def __init__(self, mode=None, episode=None):
        self.mode = mode
        self.episodes = episode if episode else [Path.cwd().parent.name]

    def check_phase_deliverables(self):
        """Checks if the phase deliverables are ready."""
        if not self.mode or self.mode not in DEFAULTS.phase_arguments:
            return False

        # get path where deliverables should be
        # check if they exist
        return True

    def set_phase(self, instatus):
        """Sets the phase for an episode."""
        if not self.mode or self.mode not in DEFAULTS.phase_arguments:
            return
        for episode in self.episodes:
            current_episode = episode
            if not isinstance(current_episode, Episode):
                episode_id = episode.get("ID")
                current_episode = Episode(episode_id)
            if self.check_phase_deliverables():
                current_episode.change_status(getattr(STATUS, self.mode))

def run_phase(func, episodes):
    """Run a phase for a list of episodes."""
    for ep in episodes:
        episode = Episode(ep)
        DEFAULTS.load_episode_defaults(episode)
        assert episode
        assert episode.date_launch
        assert episode.abbrv_title
        episode.summarize()
        resp = input("Y/n")
        if resp.lower() != "y":
            print("cancelling...")
            sys.exit()
        episode_path = DEFAULTS.root / DEFAULTS.episode_root
        assert episode_path.exists(), f"{episode_path} path wasn't found"
        os.chdir(episode_path)

        func(episode)

def episode_args(_description="Initialize Episode Directory and Queue up", _help="push episode(s) to initialize"):
    """Gets the episode arguments."""
    parser = argparse.ArgumentParser(
        description=_description
    )
    parser.add_argument(
        "episodes", type=str, nargs="+", help=_help
    )
    args = parser.parse_args()
    return args.episodes


def confirm_episodes(selected_episodes):
    """Confirms the episodes to be used."""
    print("You have selected the following: ")
    [ep.summarize() for ep in selected_episodes]
    print("\n\nContinue?")
    resp = input("Y/n")
    if resp.lower() != "y":
        print("cancelling...")
        sys.exit()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Initialize Episode Directory and Queue up"
    )
    parser.add_argument("phase", choices=DEFAULTS.phase_arguments)
    parser.add_argument(
        "episodes", type=str, nargs="+", help="push episode(s) to initialize"
    )
    args = parser.parse_args()
    phase_object = Phase(mode=args.phase.lower(), episode=args.episodes)
    phase_object.set_phase()
