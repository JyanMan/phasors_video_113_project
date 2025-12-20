from manim import *
import numpy as np
import math


# replace transform but return new
# use to replace the old with new after animation
# e.g. old_mob = play_replace_trans_full(self, old_mob, new_mob, run_time=0.5)
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

        # phi = zero
        v_phi = MathTex(r"\phi_v = 0", font_size=50, color=YELLOW)
        def v_phi_init():
            return v_phi.move_to(v_text.get_right()).shift(RIGHT*2)
        # move phi to phi of v_text
        def v_phi_to_v_text():
            v_text_phi = v_text.get_part_by_tex(r'\phi_v')
            v_text_phi_center = v_text_phi.get_center()
            return MathTex(r"0", font_size=50, color=YELLOW).move_to(v_text_phi_center)
        # remove phi from v_text
        def v_text_no_phi():
            return MathTex(
                r"v(t) = V_{max} \cos(\omega t)",
                font_size=50,
                color=YELLOW
            ).move_to(v_text.get_left(), aligned_edge=LEFT)
        
        # phase shift
        phase_shift = np.pi / 2
        shifted_curr = axes.plot(lambda x: AMP * np.sin(x  - phase_shift), color=GREEN)
        shifted_pow= axes.plot(lambda x: (AMP / 2) * np.sin(x * 2 - np.pi), color=MAROON_C)

        # phi indicator
        start_x, end_x = np.pi / 2, np.pi
        start_line, end_line = DashedLine(
            start=axes.c2p(start_x, 0),
            end=axes.c2p(start_x, -0.5),
            color=GRAY
        ), DashedLine(
            start=axes.c2p(end_x, 0),
            end=axes.c2p(end_x, -0.5),
            color=GRAY
        )
        arrow = Arrow(
            start=start_line.get_end(),
            end=end_line.get_end(),
            max_tip_length_to_length_ratio=0,
            buff=0,
            color=GRAY,
        )
        brace = Brace(arrow, DOWN, color=GREEN)
        i_phase= MathTex(r"\phi_i", font_size=50, color=GREEN).move_to(brace.get_center()).shift(DOWN*0.5)

        # omega = pi f t
        text_v_w= MathTex(r"\omega = 2\pi f", substrings_to_isolate="f")
        def text_v_w_init():
            return text_v_w.to_edge(UP).align_to(v_text).shift(RIGHT * 2)  
        def w_with_60_freq():
            return MathTex(
                r"\omega = 2\pi 60",
                substrings_to_isolate="60"
            ).move_to(text_v_w, aligned_edge=LEFT)

        def omega_group():
            v_w = MathTex(
                r"\omega = 2\pi 60",
                substrings_to_isolate="60",
                color=YELLOW
            ).move_to(text_v_w)
            i_w = MathTex(
                r"\omega = 2\pi 60",
                substrings_to_isolate="60",
                color=GREEN
            ).move_to(text_v_w).align_to(i_text, direction=UP)
            return VGroup(*[v_w, i_w])

        def v_text_with_60_freq():
            return MathTex(
                r"v(t) = V_{max} \cos(2\pi 60t )",
                font_size=50,
                color=YELLOW
            ).move_to(v_text.get_left(), aligned_edge=LEFT)
        def i_text_with_60_freq():
            return MathTex(
                r"i(t) = I_{max} \cos(2\pi 60t + \phi_i)",
                font_size=50,
                color=GREEN
            ).move_to(i_text.get_left(), aligned_edge=LEFT)



        self.play(Create(axes), run_time=1)
        self.wait(0.5)
        # init voltage wave
        self.play(Create(volt_wave_end))
        volt_wave_end.add_updater(lambda f: f.move_to(volt_wave.get_end()))
        self.play(Create(volt_wave), run_time=2)

        self.wait(0.5)
        self.play(Write(v_text), run_time=0.5)
        self.wait(0.5)
        self.play(v_text.animate().center().to_edge(UP).to_edge(LEFT).shift(RIGHT))

        # voltage formula
        v_text = play_replace_trans_full(self, v_text, v_text_formula())
        self.play(Uncreate(volt_wave_end))
        self.wait(WAIT_FOR_VO)

        # init current wave
        self.play(Create(curr_wave_end))
        curr_wave_end.add_updater(lambda f: f.move_to(curr_wave.get_end()))
        self.play(Create(curr_wave), run_time=2)
        self.play(Write(i_text_end_curr_wave()), run_time=0.5)
        self.play(i_text.animate().next_to(v_text, DOWN, aligned_edge=LEFT))

        # current formula
        i_text = play_replace_trans_full(self, i_text, i_text_formula())
        self.play(Uncreate(curr_wave_end))
        self.wait(WAIT_FOR_VO)

        # phi of v(t) being zero
        self.play(Write(v_phi_init()))
        self.wait(WAIT_FOR_VO)
        v_phi = play_replace_trans_full(self, v_phi, v_phi_to_v_text())
        self.play(FadeOut(v_phi))

        # remove phi from v(t)
        v_text = play_replace_trans_full(self, v_text, v_text_no_phi())

        self.wait(WAIT_FOR_VO)

        # phase shift
        self.play(curr_phase.animate().set_value(np.pi / 2), run_time=2)

        # draw phase shift indicator
        self.play(Create(start_line))
        self.play(Create(end_line), Create(arrow))
        self.play(Create(brace), Write(i_phase))

        # omega = pi f t
        self.play(Write(text_v_w_init()))
        self.wait(1)
        text_v_w = play_replace_trans_full(self, text_v_w, w_with_60_freq())

        # separate omega (w) formula into two
        text_v_w = play_replace_trans_full(self, text_v_w, omega_group())

        # substitutte 2pi60 to omega of i and v
        self.play(
            Transform(v_text, v_text_with_60_freq()),
            Transform(i_text, i_text_with_60_freq())
        )
        self.play(FadeOut(VGroup(*[
            text_v_w,
            brace,
            arrow,
            end_line,
            start_line,
            i_phase
        ])))






