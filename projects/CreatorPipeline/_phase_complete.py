#!usr/bin/env python

from pathlib import Path

from CreatorPipeline import phase
from CreatorPipeline.constants import STATUS

params = [[Path.cwd().parts[-1]], STATUS.done]

if phase.check_phase_deliverables(*params):
    phase.set_phase(*params)
else:
    print("Not Ready Yet")
