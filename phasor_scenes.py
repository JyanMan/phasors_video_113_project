from manim import *
import numpy as np
import math

class ChangingMagnitudePhasor(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        ).shift(UP*2)

        amp = ValueTracker(0.5)
        omega = 2

        volt_wave = axes.plot(lambda x: amp.get_value() * np.cos(x*omega), color=YELLOW)
        curr_phase = ValueTracker(0)
        curr_wave = always_redraw(
            lambda: axes.plot(lambda x: amp.get_value() * np.cos(x*omega - curr_phase.get_value()) , color=GREEN)
        )

        arr_mag_scale = 4
        ref_arrow = Line(start=(0, -2, 0), end=(amp.get_value() * arr_mag_scale, -2, 0))
        def ref_arrow_updater(line: Line):
            mag = amp.get_value() * arr_mag_scale
            x = mag * np.cos(curr_phase.get_value())
            y = (mag * np.sin(curr_phase.get_value()))
            line_start = line.get_start()
            line.set_points_by_ends(
                start=line_start,
                end=np.array([x, y, 0]) + line_start 
            )
        ref_arrow.add_updater(ref_arrow_updater)

        base_arrow = Line(start=ref_arrow.get_start(), end=ref_arrow.get_end())


        #### ANIMATION START ####
        
        self.play(Create(volt_wave))
        self.play(Create(curr_wave))
        self.play(Create(ref_arrow), Create(base_arrow))

        # shift current
        self.play( curr_phase.animate().set_value(np.pi / 2) )
        self.play( curr_phase.animate().set_value(np.pi / 4) )

        # increase magnitude
        self.play(amp.animate().set_value(0.75))
