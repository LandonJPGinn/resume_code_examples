#!usr/bin/env python

from CreatorPipeline import phase
from CreatorPipeline.constants import DEFAULTS, PROMPTS, STATUS
# from CreatorPipeline.thumbnail import ThumbnailPSD
from CreatorPipeline import _openai as oai
from pathlib import Path
import json
import sys

class PhaseResearch:
    """Research Episode and generate datafiles. Uses OpenAI to generate datafiles for the episode."""
    def __init__(self, episode):
        self.episode = episode
        DEFAULTS.load_episode_defaults(self.episode)
        # this is supposed to also be doing the heavy lifting to ensure theres a market for the episode # doing this may need to be a later thing
        self.load_ideas()
        self.make_selection()
        self.openai_generate(episode_root=DEFAULTS.episode_root, episode=self.episode)
        #ThumbnailPSD()
        self.episode.change_status(STATUS.script)

    def load_ideas(self):
        """Load proposal prompts from json file."""
        idea_path = Path(DEFAULTS.episode_root) / DEFAULTS.define_proposals
        assert idea_path.exists(), "No proposals found"
        with open(idea_path, 'r') as f:
            self.ideas = {str(i): x for i, x in enumerate(json.load(f).get("videos"))}
        assert self.ideas, f"No proposals found. Go Manually fix this: \n{idea_path}\n"


    def make_selection(self):
        """Selects a proposal from the list of proposals."""
        cap = max(self.ideas)
        for i, each_idea in self.ideas.items():
            print(f"{i}\t: {each_idea.get('title')}")
            for k, v in each_idea.items():
                print(f"\t\t{k}: {v}")
        print(f"\n Select an episode 0-{cap}")
        choice = input(f"0-{cap}")
        if choice:
            self.selected_proposal = self.ideas[choice]
            return
        print("No choice made, exiting")
        sys.exit()


    def openai_generate(self, episode_root=".", episode=None):
        """Generates the initial text ideas for an episode using OpenAI."""
        episode_root = Path(episode_root).expanduser().resolve()
        params = episode.__dict__
        params["JSON"] = f"{self.selected_proposal}"

        prompts = [
            [
                PROMPTS.script_outline.substitute(**params),
                DEFAULTS.research_episode_outline,
            ],
        ]

        for prompt, filepath in prompts:
            oai.generate_text(prompt, episode_root / filepath)



if __name__ == "__main__":
    episodes = phase.episode_args(_description="Research Episode and generate datafiles", _help="push episode(s) to research")
    phase.run_phase(PhaseResearch, episodes)
