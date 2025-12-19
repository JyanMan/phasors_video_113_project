from manim import *
import numpy as np
import math

class IntroScene(Scene):
    def construct(self):
        center = Dot()
        # self.add(center)
        title_text = Tex("EEE 113 Wrap-Up Report", font_size=72)
        title_text.move_to(center.get_center(), aligned_edge=DOWN)
        subtitle_text = Tex("by Jian Jarapa \& Quintus Cruz")
        subtitle_text.next_to(title_text, DOWN)

        text_group = VGroup(title_text, subtitle_text)
        self.play(Write(text_group, run_time=3.5))
        self.wait(5.0)
        self.play(Unwrite(text_group, run_time=1.5))
        self.wait(1.0)
        pass


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
