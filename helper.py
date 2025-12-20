from manim import *
import numpy as np
import math

# replace transform but return new
# use to replace the old with new after animation
# e.g. old_mob = play_replace_trans_full(self, old_mob, new_mob, run_time=0.5)
def play_replace_trans_full(self: Scene, old: Mobject, new: Mobject, **kwargs):
    self.play(ReplacementTransform(old, new, **kwargs))
    return new
