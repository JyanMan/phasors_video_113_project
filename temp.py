from manim import *
import numpy as np
import math


# replace transform but return new
# use to replace the old with new after animation
def play_replace_trans_full(self: Scene, old: Mobject, new: Mobject, **kwargs):
    self.play(ReplacementTransform(old, new, **kwargs))
    return new


class Test(Scene):
    def construct(self):
        WAIT_FOR_VO = 2.5
        AMP = 1
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        ).shift(LEFT*0.5)

        ###### VOLTAGE WAVE INITIAL ANIMATION ######
        volt_wave = axes.plot(lambda x: AMP * np.cos(x), color=YELLOW)
        volt_wave_end = Dot(axes.c2p(0, AMP), color=YELLOW_C)
        v_text = MathTex(
            r"v(t)",
            # substrings_to_isolate=['\phi'],
            font_size=50,
            color=YELLOW
        ).next_to(volt_wave.get_end(), RIGHT)

        def v_text_formula():
            return MathTex(
                r"v(t) = V_{max} \cos(\omega t + \phi_v)",
                substrings_to_isolate=[r'\phi_v'],
                font_size=50,
                color=YELLOW
            ).move_to(v_text.get_left(), aligned_edge=LEFT)


        ###### VOLTAGE WAVE INITIAL ANIMATION ######
        

        ###### CURRENT WAVE INITIAL ANIMATION  ######
        curr_phase= ValueTracker(0)
        curr_wave = always_redraw(
            lambda: axes.plot(lambda x: AMP * np.cos(x - curr_phase.get_value()) , color=GREEN)
        )
        curr_wave_end = Dot(axes.c2p(0, AMP), color=PURE_GREEN)

        i_text = MathTex(
            "i(t)",
            font_size=50,
            color=GREEN
        )
        def i_text_end_curr_wave():
            return i_text.move_to(curr_wave.get_end()).shift(RIGHT*0.5)

        def i_text_below_v():
            return MathTex(
                "i(t)",
                font_size=50,
                color=GREEN
            ).move_to(curr_wave.get_end()).shift(RIGHT*0.5)


        def i_text_formula():
            return MathTex(
                r"i(t) = I_{max} \cos(\omega t + \phi_i)",
                font_size=50,
                color=GREEN
            ).move_to(i_text.get_left(), aligned_edge=LEFT)

        v_phi = MathTex(r"\phi_v = 0", font_size=50, color=YELLOW)
        def v_phi_init():
            return v_phi.move_to(v_text.get_right()).shift(RIGHT*2)
        def v_phi_to_v_text():
            v_text_phi = v_text.get_part_by_tex(r'\phi_v')
            v_text_phi_center = v_text_phi.get_center()
            return MathTex(r"0", font_size=50, color=YELLOW).move_to(v_text_phi_center)

        self.play(Create(axes), run_time=1)
        self.wait(0.5)
        self.play(Create(volt_wave_end))
        volt_wave_end.add_updater(lambda f: f.move_to(volt_wave.get_end()))
        self.play(Create(volt_wave), run_time=2)

        self.wait(0.5)
        self.play(Write(v_text), run_time=0.5)
        self.wait(0.5)
        self.play(v_text.animate().center().to_edge(UP).to_edge(LEFT).shift(RIGHT))
        self.play(Uncreate(volt_wave_end))

        v_text = play_replace_trans_full(self, v_text, v_text_formula())
        self.wait(WAIT_FOR_VO)

        self.play(Create(curr_wave_end))
        curr_wave_end.add_updater(lambda f: f.move_to(curr_wave.get_end()))
        self.play(Create(curr_wave), run_time=2)
        self.play(Write(i_text_end_curr_wave()), run_time=0.5)
        self.play(i_text.animate().next_to(v_text, DOWN, aligned_edge=LEFT))

        i_text = play_replace_trans_full(self, i_text, i_text_formula())
        self.play(Uncreate(curr_wave_end))
        self.wait(WAIT_FOR_VO)

        ###### CURRENT WAVE INITIAL ANIMATION  ######
        # phi of v(t) being zero
        self.play(Write(v_phi_init()))
        self.wait(WAIT_FOR_VO)
        v_phi = play_replace_trans_full(self, v_phi, v_phi_to_v_text())
        self.play(FadeOut(v_phi))
