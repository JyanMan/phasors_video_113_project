import numpy as np
import math

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService
from helper import play_replace_trans_full

class CurrentVoltagePowerWave(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())

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



        #### ANIMATION START ####
        self.play(Create(axes), run_time=1)

        # init voltage wave
        with self.voiceover(
            "With this measurement device, we were able to see the voltage"
        ) as tracker:
            self.play(Create(volt_wave_end), run_time=0.5)
            volt_wave_end.add_updater(lambda f: f.move_to(volt_wave.get_end()))
            self.play(Create(volt_wave), run_time=1)
            self.play(Write(v_text), run_time=0.5)

        # init current wave
        with self.voiceover("and current waveforms that come out of your outlet") as tracker:
            self.play(
                Create(curr_wave_end),
                v_text.animate().center().to_edge(UP).to_edge(LEFT).shift(RIGHT)
            )
            curr_wave_end.add_updater(lambda f: f.move_to(curr_wave.get_end()))
            self.play(Create(curr_wave), run_time=1)
            self.play(Write(i_text_end_curr_wave()), run_time=0.5)
            self.play(i_text.animate().next_to(v_text, DOWN, aligned_edge=LEFT))


        with self.voiceover(
            "and as we learned from school, these waveforms are\
            mathematically defined as a sinusoid with amplitude\
            V max and I max respectively of voltage and current"
        ) as tracker:
            # voltage formula
            self.wait(3)
            v_text = play_replace_trans_full(self, v_text, v_text_formula(), run_time=1)
            self.play(Uncreate(volt_wave_end))
            # current formula
            self.wait(1)
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


        
class NegativePower(Scene):
    def init_setup(self):
        # in ac,
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        ).shift(LEFT*0.5)

        AMP = 1

        volt_wave = axes.plot(lambda x: AMP * np.sin(x), color=YELLOW)
        curr_phase = ValueTracker(np.pi/2)
        curr_wave = always_redraw(
            lambda: axes.plot(lambda x: AMP * np.sin(x - curr_phase.get_value()) , color=GREEN)
        )
        v_text = MathTex(
            r"v(t) = V_{max} \cos(", r"2\pi 60t", r")",
            font_size=50,
            color=YELLOW
        ).to_edge(UP).to_edge(LEFT).shift([1, 0.5, 0])
        i_text = MathTex(
            r"i(t) = I_{max} \cos(", r"2\pi 60t", r"+\phi", r")",
            substrings_to_isolate=[r'\phi'],
            font_size=50,
            color=GREEN
        ).to_edge(UP).to_edge(LEFT).shift([1, -0.3, 0])

        return (
            VGroup(*[axes, volt_wave, curr_wave, i_text, v_text]),
            curr_phase,
            AMP
        )


    def create_phase_indicator(self, axes):
        start_x = np.pi / 2
        start_line = DashedLine(
            start=axes.c2p(start_x, 0),
            end=axes.c2p(start_x, -0.5),
            color=GRAY
        )
        end_x = np.pi
        end_line = DashedLine(
            start=axes.c2p(end_x, 0),
            end=axes.c2p(end_x, -0.5),
            color=GRAY
        )
        self.play(Create(start_line))
        arrow = Arrow(
            start=start_line.get_end(),
            end=end_line.get_end(),
            max_tip_length_to_length_ratio=0,
            buff=0,
            color=GRAY,
        )
        brace = Brace(arrow, DOWN, color=GREEN)
        i_phase= MathTex(r"\phi", font_size=50, color=GREEN).move_to(brace.get_center()).shift(DOWN*0.5)
        self.play(
            Create(end_line),
            Create(arrow),
            Create(brace),
            Create(i_phase)
        )

        return VGroup(*[start_line, end_line, arrow, brace, i_phase])


    def phase_to_zero_animation(self, phase_group):
        start_line = phase_group[0]
        end_line = phase_group[1]
        arrow = phase_group[2]
        brace = phase_group[3]
        i_phase = phase_group[4]

        new_end_line = end_line.copy().move_to(start_line.get_center())
        return [
            Transform(end_line, new_end_line),
            arrow.animate().scale(0).move_to(new_end_line.get_center()).shift(DOWN*0.4),
            brace.animate().scale(0).move_to(new_end_line.get_center()).shift(DOWN*0.8),
            i_phase.animate().move_to(new_end_line.get_center()).shift(DOWN*1.2)
        ]


    def construct(self):

        init_group, curr_phase, AMP = self.init_setup()
        self.add(init_group)

        axes = init_group[0]
        i_formula = init_group[3]
        v_formula = init_group[4]

        # POWER
        pow_phase = ValueTracker(np.pi/2)
        pow_offset = ValueTracker(-0.5)
        power_wave = always_redraw(
            lambda: axes.plot(
                lambda x:
                # (AMP / 2) * np.sin(x * 2 - (np.pi / 2 + pow_phase.get_value())) + 0.5 + pow_offset.get_value(), color=MAROON_C
                (AMP / 2) * np.sin(x * 2 - (np.pi / 2 + pow_phase.get_value())) + 0.5 + pow_offset.get_value(),
                color=MAROON_C
            )
        )

        self.play(Create(power_wave), run_time=2)
        p_of_t = MathTex("p(t)", font_size=50, color=MAROON_C).move_to(power_wave.get_end()).shift(RIGHT*0.5)
        self.play(Create(p_of_t), run_time=0.5)

        new_pow_formula = MathTex(
            r"p(t) = v(t)i(t)",
            color=MAROON_C,
            font_size=50
        ).to_edge(UP).shift(DOWN*0.5)
        self.play(
            Transform(p_of_t, new_pow_formula),
            FadeOut(v_formula),
            i_formula.animate().to_edge(DOWN)
        )

        phase_group = self.create_phase_indicator(axes)
        self.play(
            self.phase_to_zero_animation(phase_group),
            curr_phase.animate().set_value(0),
            pow_phase.animate().set_value(0),
            pow_offset.animate().set_value(0),
            run_time=3
        )

        start_line = phase_group[0]
        end_line = phase_group[1]
        i_phase = phase_group[4]
        new_i_phase = MathTex(
            r"\phi =", r"\phantom{+0.00}",
            font_size=50,
            color=GREEN
        ).move_to(i_phase.get_left()).shift(RIGHT*0.5)
        i_phase_num = DecimalNumber(
            number=curr_phase.get_value(),
            num_decimal_places=2,
            color=BLUE_C,
        ).move_to(new_i_phase.get_right()).shift(RIGHT*0.5)
        self.play(
            FadeOut(end_line), FadeOut(start_line),
            Transform(i_phase, new_i_phase),
            Create(i_phase_num)
        )
        def i_phase_updater(mob):
            value = curr_phase.get_value()
            mob.set_value(value)
        i_phase_num.add_updater(i_phase_updater)

        # focus on phi / i_phase
        self.play(
            FadeToColor(i_phase, color=BLUE_C),
            FadeToColor(i_formula[3], color=BLUE_C)
        )
        new_i_formula = MathTex(
            r"i(t) = I_{max} \cos(", r"2\pi 60t", r"\phantom{+}", r"\phantom{0.00}", r")",
            substrings_to_isolate=[r"\phi"],
            font_size=50,
            color=GREEN
        ).move_to(i_formula.get_center()).shift(RIGHT*0.2)

        # set phi to a constant
        # self.play(Transform(i_formula, new_i_formula) )
        self.play(ReplacementTransform(i_formula, new_i_formula))
        phase_number = MathTex(
            r"+0.00",
            color=BLUE_C,
            font_size=50,
        # ).move_to(i_formula.get_right()).shift(LEFT*2)
        ).move_to(new_i_formula.get_right()).shift(LEFT*0.8)
        def phase_number_updater(mob):
            value = curr_phase.get_value()
            sign = "+" if value >= 0 else "-"
            mob.become(
                MathTex(
                    rf"{sign}{abs(value):.2f}",
                    font_size=50,
                    color=BLUE_C
                ).move_to(mob.get_center())
            )
        phase_number.add_updater(phase_number_updater)
        self.play(Create(phase_number))

        # shift the current left and right
        def pow_offset_follow_current(mob):
            value = curr_phase.get_value() % (2 * np.pi)
            half_value = value % np.pi
            sign = math.copysign(1, value)
            ratio = abs(half_value) / np.pi
            if abs(value) < np.pi:
                value = sign * ratio
                mob.set_value(-value)
            else:
                value = sign * (1 - ratio) 
                mob.set_value(-value)
                
        pow_offset.add_updater(pow_offset_follow_current)

        # purely resistive load
        purely_res_load = Text(
            "Purely Resistive Load", color=BLUE_C, font_size=40
        ).to_edge(RIGHT).shift(DOWN*2)
        self.play(Create(purely_res_load))

        self.wait(4)
        
        self.play(
            FadeOut(purely_res_load),
            run_time=0.5,
        )
        self.play(
            curr_phase.animate().set_value(-2*np.pi),
            pow_phase.animate().set_value(-2*np.pi),
            lag_ratio=0.8,
            run_time=4
        )
        self.play(
            curr_phase.animate().set_value(2*np.pi),
            pow_phase.animate().set_value(2*np.pi),
            lag_ratio=0.8,
            # pos_offset.animate().set_value()
            run_time=8
        )

        # add approximation of phase in terms of pi
        pi_terms_phase = MathTex(
            r"\approx 2\pi",
            color=PINK
        ).move_to(new_i_phase.get_right()).shift([0.2, -0.5, 0])
        self.play(Create(pi_terms_phase), run_time=0.5)


