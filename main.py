from manim import *
import numpy as np

class TrigIssues(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        )
        axes2 = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        )

        first_wave = axes.plot(lambda x: 0.5*np.sin(x*2), color=GREEN).move_to(DOWN)
        second_wave = axes2.plot(lambda x: 0.5*np.sin(x*2), color=BLUE).move_to(UP*2)

        first_cos = MathTex(r"a = A_{1} \cos( \omega t - \phi)", font_size=40).move_to(DOWN*2.5)
        second_cos= MathTex(r"b = A_{2} \cos(\omega t - \phi)", font_size=40).move_to(UP*0.5)

        self.play(Create(first_wave), Create(second_wave), Create(first_cos), Create(second_cos))

        self.wait(2)

        sum_wave = axes.plot(lambda x: np.sin(x*2), color=YELLOW)        
        init_waves = VGroup(*[first_wave, second_wave])
        init_formulas = VGroup(*[first_cos, second_cos])
        sum_formula = MathTex(r"c = A_{1} \cos(\omega t - \phi) +  A_{1} \cos(\omega t - \phi)", font_size=40).move_to(DOWN*2.5)
        self.play(
            Transform(init_waves, sum_wave),
            Transform(init_formulas, sum_formula)
        )
        

class CurrentVoltagePowerWave(Scene):
    def construct(self):
        # in ac,
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE}
        ).shift(LEFT*0.5)

        AMP = 1

        volt_wave = axes.plot(lambda x: AMP * np.sin(x), color=YELLOW)
        curr_phase= ValueTracker(0)
        curr_wave = always_redraw(
            lambda: axes.plot(lambda x: AMP * np.sin(x - curr_phase.get_value()) , color=GREEN)
        )

        # VOLTAGE
        self.play(Create(axes), run_time=1)
        self.play(
            # Create(curr_wave),
            Create(volt_wave),
            run_time=2
        )

        # v_text = MathTex("v(t)", font_size=50, color=YELLOW).move_to(volt_wave.get_end()).shift(RIGHT*0.5)
        v_text = MathTex(
            r"v(t)",
            # substrings_to_isolate=['\phi'],
            font_size=50,
            color=YELLOW
        ).move_to(volt_wave.get_end()).shift(RIGHT*0.5)
        self.play(Create(v_text), run_time=0.5)

        self.wait(1)
        self.play(v_text.animate().center().to_edge(UP).to_edge(LEFT).shift([1, 0.5, 0]))

        new_v_text = MathTex(
            r"v(t) = V_{max} \cos(\omega t - \phi)",
            substrings_to_isolate=[r'\phi'],
            font_size=50,
            color=YELLOW
        ).to_edge(UP).to_edge(LEFT).shift([1, 0.5, 0])
        self.play(Transform(v_text, new_v_text))
        
        self.play(Create(curr_wave), run_time=2)

        # CURRENT
        i_text = MathTex("i(t)", font_size=50, color=GREEN).move_to(curr_wave.get_end()).shift(RIGHT*0.5)
        self.play(Create(i_text), run_time=0.5)

        self.wait(1)
        self.play(i_text.animate().move_to(v_text.get_left()).shift([0.5, -0.8, 0]))

        new_i_text= MathTex(r"i(t) = I_{max} \cos(\omega t - \phi)", font_size=50, color=GREEN).to_edge(UP).to_edge(LEFT).shift([1, -0.3, 0])
        self.play(Transform(i_text, new_i_text))
         
        # POWER
        pow_phase = ValueTracker(0)
        pow_offset = ValueTracker(0)
        power_wave = always_redraw(
            lambda: axes.plot(
                lambda x:
                (AMP / 2) * np.sin(x * 2 - (np.pi / 2 + pow_phase.get_value())) + 0.5 + pow_offset.get_value(), color=MAROON_C
            )
        )

        self.play(Create(power_wave), run_time=2)
        p_text = MathTex("p(t)", font_size=50, color=MAROON_C).move_to(power_wave.get_end()).shift(RIGHT*0.5)
        self.play(Create(p_text), run_time=0.5)

        # constant 60 frequency
        v_phi = MathTex(r"\phi = 0", font_size=50, color=YELLOW).move_to(v_text.get_right()).shift(RIGHT*2)
        self.play(Create(v_phi))
        v_text_phi = new_v_text.get_part_by_tex(r'\phi')
        v_text_phi_center = v_text_phi.get_center()
        new_v_phi = MathTex(r"0", font_size=50, color=YELLOW).move_to(v_text_phi_center)
        self.play( Transform( v_phi, new_v_phi), )
        self.play(FadeOut(v_phi))
        new_v_text = MathTex(
            r"v(t) = V_{max} \cos(\omega t)",
            font_size=50,
            color=YELLOW
        ).to_edge(UP).to_edge(LEFT).shift([1, 0.5, 0])
        self.play(Transform(v_text, new_v_text))

        # phase shift
        phase_shift = np.pi / 2
        shifted_curr = axes.plot(lambda x: AMP * np.sin(x  - phase_shift), color=GREEN)
        shifted_pow= axes.plot(lambda x: (AMP / 2) * np.sin(x * 2 - np.pi), color=MAROON_C)
        self.play(
            curr_phase.animate().set_value(np.pi / 2),
            pow_phase.animate().set_value(np.pi / 2),
            pow_offset.animate().set_value(-0.5),
            run_time=2
        )

        start_x = np.pi / 2
        start_line = DashedLine(
            start=axes.c2p(start_x, 0),
            end=axes.c2p(start_x, -0.5)
        )
        end_x = np.pi
        end_line = DashedLine(
            start=axes.c2p(end_x, 0),
            end=axes.c2p(end_x, -0.5)
        )
        self.play(Create(start_line))
        arrow = Arrow(
            start=start_line.get_end(),
            end=end_line.get_end(),
            max_tip_length_to_length_ratio=0,
            buff=0,
        )
        brace = Brace(arrow, DOWN, color=GREEN)
        self.play(
            Create(end_line),
            Create(arrow),
        )
        i_phase= MathTex(r"\phi", font_size=50, color=GREEN).move_to(brace.get_center()).shift(DOWN*0.5)
        self.play(
            Create(brace),
            Create(i_phase)
        )

        


        

def main():
    print("Hello from v2-write-up!")


if __name__ == "__main__":
    main()
