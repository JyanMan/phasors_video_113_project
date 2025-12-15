from manim import *
import numpy as np
import math

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
            r"v(t) = V_{max} \cos(", r"\omega t", r"+ \phi)",
            substrings_to_isolate=[r'\phi'],
            font_size=50,
            color=YELLOW
        ).to_edge(UP).to_edge(LEFT).shift([1, 0.5, 0])
        self.play(Transform(v_text, new_v_text))
        
        self.play(Create(curr_wave), run_time=2)

        # CURRENT
        i_text = MathTex(
            "i(t)",
            font_size=50,
            color=GREEN
        ).move_to(curr_wave.get_end()).shift(RIGHT*0.5)

        self.play(Create(i_text), run_time=0.5)

        self.wait(1)
        self.play(i_text.animate().move_to(v_text.get_left()).shift([0.3, -0.8, 0]))

        new_i_text= MathTex(
            r"i(t) = I_{max} \cos(", r"\omega t", r"+ \phi", r")",
            font_size=50,
            color=GREEN
        ).to_edge(UP).to_edge(LEFT).shift([1, -0.3, 0])
        self.play(Transform(i_text, new_i_text))
         

        # phi of v(t) being zero
        v_phi = MathTex(r"\phi = 0", font_size=50, color=YELLOW).move_to(v_text.get_right()).shift(RIGHT*2)
        self.play(Create(v_phi))
        v_text_phi = new_v_text.get_part_by_tex(r'\phi')
        v_text_phi_center = v_text_phi.get_center()
        new_v_phi = MathTex(r"0", font_size=50, color=YELLOW).move_to(v_text_phi_center)
        self.play( Transform( v_phi, new_v_phi), )
        self.play(FadeOut(v_phi))
        new_v_text = MathTex(
            r"v(t) = V_{max} \cos(", r"\omega t", r")",
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
            # pow_phase.animate().set_value(np.pi / 2),
            # pow_offset.animate().set_value(-0.5),
            run_time=2
        )

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
        self.play(
            Create(end_line),
            Create(arrow),
        )
        i_phase= MathTex(r"\phi", font_size=50, color=GREEN).move_to(brace.get_center()).shift(DOWN*0.5)
        self.play(
            Create(brace),
            Create(i_phase)
        )

        # omega = pi f t
        text_v_w= MathTex(
            r"\omega = 2\pi f",
            substrings_to_isolate="f"
        ).to_edge(RIGHT).to_edge(UP).shift(LEFT*2)
        self.play(Create(text_v_w))

        self.wait(1)
        new_text_v_w = MathTex(
            r"\omega = 2\pi 60",
            substrings_to_isolate="60"
        ).to_edge(RIGHT).to_edge(UP).shift(LEFT*2)
        self.play(Transform(text_v_w, new_text_v_w))

        # frequency is constant 60
        v_w = MathTex(
            r"\omega = 2\pi 60",
            substrings_to_isolate="60",
            color=YELLOW
        ).move_to(text_v_w.get_left()).shift(UP*0.5)
        i_w = MathTex(
            r"\omega = 2\pi 60",
            substrings_to_isolate="60",
            color=GREEN
        ).move_to(text_v_w.get_left()).shift(DOWN*0.2)
        omega_group = VGroup(*[v_w, i_w])
        self.play(Transform(text_v_w, omega_group))

        # substitutte 2pi60 to omega of i and v
        new_v_text = MathTex(
            r"v(t) = V_{max} \cos(", r"2\pi 60t", r")",
            font_size=50,
            color=YELLOW
        ).to_edge(UP).to_edge(LEFT).shift([1, 0.5, 0])
        new_i_text = MathTex(
            r"i(t) = I_{max} \cos(", r"2\pi 60t", r"+ \phi", r")",
            font_size=50,
            color=GREEN
        ).to_edge(UP).to_edge(LEFT).shift([1, -0.3, 0])
        self.play(
            Transform( v_text, new_v_text ),
            Transform( i_text, new_i_text )
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
        curr_phase= ValueTracker(np.pi/2)
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


class RecallPower(Scene):
    def construct(self):
        recall_text = Text(
            "Recall",
            color=BLUE_C,
            font_size=40
        ).to_edge(LEFT).to_edge(UP) 

        pow_formula = MathTex(
            r"P=VI",
            substrings_to_isolate=['V', 'I'],
            font_size=50
        ).move_to([-2, 1, 0])

        self.play(Create(recall_text), run_time=0.5)

        self.play( Create(pow_formula), run_time=0.5)
        self.wait(1)

        p_in_terms_vr = MathTex(
            r"P = \frac{V^{2}}{R}", r"= I^{2}R",
            substrings_to_isolate=['R'],
            font_size=50,
        ).next_to(pow_formula).shift(RIGHT)

        arrow_to_other_forms = Arrow(
            start=pow_formula.get_right(),
            end=p_in_terms_vr.get_left(),
            buff=LARGE_BUFF
        )

        self.play(Create(arrow_to_other_forms), run_time=1)

        self.play(Create(p_in_terms_vr), run_time=1.5)

        # show v and i as functions of time
        v_part_of_pow = pow_formula.get_part_by_tex('V')
        v_of_t = MathTex(
            r"v(t)",
            color=YELLOW,
            font_size=50
        ).move_to(v_part_of_pow.get_center()).shift([-2, -2, 0])
        arrow_to_v_of_t = Arrow(
            start=v_part_of_pow.get_center(),
            end=v_of_t.get_center(),
            buff=MED_LARGE_BUFF,
            color=YELLOW,
        )
        self.play(
            Create(arrow_to_v_of_t),
            pow_formula.animate().set_color_by_tex('V', color=YELLOW)
        )
        self.play(Create(v_of_t))

        i_part_of_pow = pow_formula.get_part_by_tex('I')
        i_of_t = MathTex(
            r"i(t)",
            color=GREEN,
           font_size=50 
        ).move_to(v_of_t.get_center()).shift(DOWN)
        arrow_to_i_of_t = Arrow(
            start=i_part_of_pow.get_center(),
            end=i_of_t.get_center(),
            buff=MED_LARGE_BUFF,
            color=GREEN,
        )
        self.play(
            Create(arrow_to_i_of_t),
            pow_formula.animate().set_color_by_tex('I', color=GREEN)
        )
        self.play(Create(i_of_t))

        # show r is constant
        constant_text = Text(
            "constant",
            color=BLUE_C,
            font_size=40,
        ).move_to(p_in_terms_vr.get_center()).shift(DOWN)
        self.play( p_in_terms_vr.animate().set_color_by_tex('R', color=BLUE_C), )
        self.play( Create(constant_text) )

        self.wait(1)

        # fade all
        to_fade = VGroup(*[
            constant_text,
            pow_formula,
            p_in_terms_vr,
            recall_text,
            arrow_to_i_of_t,
            arrow_to_v_of_t,
            v_of_t,
            i_of_t,
            arrow_to_other_forms
        ])
        self.play(FadeOut(to_fade))


class ForAcSignals(Scene):
    def construct(self):
        for_ac_text = Text(
            "For Ac Signals",
            color=BLUE_C,
            font_size=40
        ).to_edge(LEFT).to_edge(UP)
        self.play(Create(for_ac_text), run_time=0.5)

        # show R -> Z
        r_text = MathTex(
            "R",
            color=BLUE_C,
            font_size=50
        ).move_to([-2, 2, 0])
        z_text = MathTex(
            "Z",
            color=MAROON_C,
            font_size=50
        ).next_to(r_text).shift(RIGHT*2)
        arrow_r_to_z = Arrow(
            start=r_text.get_center(),
            end=z_text.get_center(),
            color=GRAY,
            buff=MED_LARGE_BUFF
        )
        self.play(
            AnimationGroup(*[
                Create(r_text),
                Create(arrow_r_to_z),
                Create(z_text)                   
            ], lag_ratio=0.8), run_time=3, 
        )

        # where Z is impedance, show formula
        where_text = Text(
            "where", color=GRAY, font_size=40
        ).move_to(r_text.get_center()).shift([-1, -1, 0])
        self.play(Create(where_text), run_time=0.5)

        impedance_formula = MathTex(
            r"Z=R+jX",
            color=MAROON_C,
            font_size=50
        ).move_to(r_text.get_center()).shift(DOWN*2)
        self.play(Create(impedance_formula), run_time=0.5)


class Summary(Scene):
    def construct(self):
        def point_statement(text: str):
            point = Circle(color=MAROON_A, radius=0.2)
            text_mob = Tex(text, font_size=50).next_to(point)
            return VGroup(*[point, text_mob])

        first_point = point_statement("They are periodic").to_edge(LEFT).shift(UP)
        second_point = point_statement("$V_{max}$, $I_{max}$ doesn't depend on t"
        ).to_edge(LEFT)
        third_point = point_statement("$\\phi$ doesn't rely on t"
        ).to_edge(LEFT).shift(DOWN)
        self.play(Create(first_point), )
        self.play(Create(second_point))
        self.play(Create(third_point))

        self.play(FadeOut(VGroup(*[
            first_point, second_point, third_point                             
        ])))

        final_text = Tex(
            r"Basically the shape of v(t) and i(t)\\",
            r"doesn't change over time,",
            font_size=50
        )
        self.play(Create(final_text))
        it_shifts = Tex(
            "it only shifts by $\\phi$",
            font_size=50
        ).move_to(final_text.get_center()).shift(DOWN)
        self.play(Create(it_shifts))
        
        

def main():
    print("Hello from v2-write-up!")


if __name__ == "__main__":
    main()
