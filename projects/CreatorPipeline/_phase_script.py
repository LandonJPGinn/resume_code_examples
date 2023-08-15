#!usr/bin/env python

from CreatorPipeline import phase
from CreatorPipeline.constants import DEFAULTS, PROMPTS, STATUS
from CreatorPipeline import _openai as oai
from pathlib import Path
import subprocess
import sys


class PhaseScript:
    """Script Generation Phase. Uses OpenAI to generate a script for the episode. And then Open to edit."""
    def __init__(self, episode):
        self.episode = episode

        self.episode_root = Path.cwd()

        self.outline_fp = self.episode_root / DEFAULTS.research_episode_outline
        self.script_fp = self.episode_root / DEFAULTS.script_episode_draft

        self._redo()
        self.episode.change_status(STATUS.record)

    def _redo(self,note=""):
        """Redo the script and prompt for a new script."""
        if Path(self.script_fp).exists():
            Path(self.script_fp).unlink()

        self.openai_generate(episode=self.episode,note=note)
        self.body = Path(self.script_fp).read_text()

        print("+"*88)
        print(self.body)
        print("+"*88)
        print("Do you approve of this script?\n\t1: Approve\n\t2: Edit\n\t3: Redo")

        choice = input("1-3")
        if choice == "1":
            self._save()
        elif choice == "2":
            self._open()
        elif choice == "3":
            notes = input("Notes: ")
            self._redo(note=notes)
        else:
            print("No choice made, exiting")
            sys.exit()

    def _save(self):
        """Save the script to the episode."""
        with open(self.script_fp, 'w') as f:
            f.write(self.body)

    def _open(self):
        """Open the script in VSCode."""
        subprocess.run(["code", str(self.script_fp)])

    def openai_generate(self, episode=None, note=""):
        """ Generate a script using OpenAI. """

        with open(self.outline_fp, 'r') as f:
            prompt = f.read()

        params = episode.__dict__
        params["OUTLINE"] = prompt

        prompts = [
            [
                PROMPTS.script_draft.substitute(**params) + f" {note}",
                DEFAULTS.script_episode_draft,
            ],
        ]

        for prompt, filepath in prompts:
            print("Building Script...\n\n")
            oai.generate_text(prompt, self.episode_root / filepath)


if __name__ == "__main__":
    episodes = phase.episode_args(_description="Generate Script Rough Draft", _help="push episode(s) to make script")
    phase.run_phase(PhaseScript, episodes)
