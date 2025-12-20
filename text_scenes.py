from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService
import numpy as np
import math

class IntroScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService())
        
        ### Slide 1 ###
        center = Dot()
        title_text = Tex("EEE 113 Wrap-Up Report", font_size=72)
        title_text.move_to(center.get_center(), aligned_edge=DOWN)
        subtitle_text = Tex("by Jian Jarapa \& Quintus Cruz")
        subtitle_text.next_to(title_text, DOWN)
        title_texts = VGroup(title_text, subtitle_text)
        ### Slide 1 ###

        ### Slide 2 ###
        question_text = Paragraph(
            "Were there topics that were covered in class",
            "but were not emphasized in the long-exam?",
            "We assume that you learned it well, so here's an",
            "opportunity to demonstrate what you learned.",
            alignment='center',
            font_size=32
        )
        ### Slide 2 ###

        ### Slide 3 ###
        assumed_topics = Paragraph(
            "○ Ohm's Law (V = IR)",
            "○ Power Law (P = VI)",
            alignment='left',
            font_size=36
        ).to_corner(UL)
        
        ### Slide 3 ###

        with self.voiceover("Good day! Welcome to our wrap-up report for the Power component of EEE 113.") as tracker:
            self.play(Write(title_texts, run_time=1.5))
            self.wait(tracker.duration - 1.5)
            self.play(Unwrite(title_texts, run_time=1.5))

        self.wait(0.5)

        with self.voiceover("For this video, we decided to tackle the following prescribed question: "):
            self.play(Write(question_text), run_time=2.0)

        with self.voiceover("By showing our own interpretation of the theory behind AC Power Analysis, specifically, with Phasor Analysis."):
            self.wait(tracker.duration + 1.5)
            self.play(Unwrite(question_text))

        with self.voiceover("This video assumes basic knowledge of the following concepts from DC Circuit Analysis."):
            self.play(Write(assumed_topics), run_time=1.5)
            self.wait(tracker.duration)

        self.play(Unwrite(assumed_topics))

class PowerLaw(Scene):
    def construct(self):
        power_eqn = MathTex(r"P =", r"V", r"I", font_size=60)
        power_eqn_t = MathTex(r"p(t) =", r"v(t)", r"i(t)", font_size=60).next_to(power_eqn, DOWN)

        v_eqn = MathTex(r"v(t)", r"= ", r"V_{max}", r"\cos(", r"\omega", r"t", r"+", r"\phi_v", r")")
        i_eqn = MathTex(r"i(t)", r"= ", r"I_{max}", r"\cos(", r"\omega", r"t", r"+", r"\phi_i", r")").next_to(v_eqn, DOWN)
        eqn_group = VGroup(v_eqn, i_eqn)

        v_max = v_eqn.get_part_by_tex(r'V_{max}').copy()
        v_max.generate_target()
        v_max.target.next_to(v_eqn.get_part_by_tex(r'V_{max}'), UP * 1.5)
        i_max = i_eqn.get_part_by_tex(r'I_{max}').copy()
        i_max.generate_target()
        i_max.target.next_to(i_eqn.get_part_by_tex(r'I_{max}'), DOWN * 1.5)

        v_max_defn = MathTex(r"= V_{rms}", r"\sqrt{2}").next_to(v_max.target, RIGHT)
        i_max_defn = MathTex(r"= I_{rms}", r"\sqrt{2}").next_to(i_max.target, RIGHT)

        omega = MathTex(r'\omega').move_to(v_max.target, aligned_edge=LEFT)
        omega_defn = MathTex(r"= ", r"2\pi 60\text{Hz}").next_to(omega, RIGHT)
        omega_approx = MathTex(r"\approx ", r"377").next_to(omega_defn)

        v_phi = MathTex(r"\phi_v")
        i_phi = MathTex(r"\phi_i")
        v_phi_defn = MathTex(r"= 0")
        i_phi_defn = MathTex(r"=\; ?")
        v_eqn_no_phi = MathTex(r"v(t)", r"=", r"V_{max}\cos(\omega t)")

        self.play(Write(power_eqn))
        self.wait()
        self.play(Indicate(power_eqn.get_part_by_tex(r'V')))
        self.play(Indicate(power_eqn.get_part_by_tex(r'I')))
        self.wait()
        self.play(ReplacementTransform(power_eqn.copy(), power_eqn_t))
        self.play(power_eqn_t.animate.move_to(ORIGIN), FadeOut(power_eqn, shift=UP))
        self.remove(power_eqn)
        self.wait()
        self.play(power_eqn_t.animate.to_corner(UL))
        self.wait()
        self.play(Indicate(power_eqn_t.get_part_by_tex(r'v(t)')))
        self.play(ReplacementTransform(power_eqn_t.get_part_by_tex(r'v(t)').copy(), v_eqn.get_part_by_tex(r'v(t)'), path_arc=-120 * DEGREES))
        self.play(ReplacementTransform(v_eqn.get_part_by_tex(r'v(t)'), v_eqn))
        self.play(Indicate(power_eqn_t.get_part_by_tex(r'i(t)')))
        self.play(ReplacementTransform(power_eqn_t.get_part_by_tex(r'i(t)').copy(), i_eqn.get_part_by_tex(r'i(t)'), path_arc=-120 * DEGREES))
        self.play(ReplacementTransform(i_eqn.get_part_by_tex(r'i(t)'), i_eqn))

        self.play(MoveToTarget(v_max), MoveToTarget(i_max))
        self.play(FadeIn(v_max_defn, shift=RIGHT))
        self.play(FadeIn(i_max_defn, shift=RIGHT))
        self.play(FadeOut(v_max, shift=UP), FadeOut(v_max_defn, shift=UP), FadeOut(i_max, shift=DOWN), FadeOut(i_max_defn, shift=DOWN))
        self.remove(v_max, v_max_defn, i_max, i_max_defn)

        self.play(
            ReplacementTransform(v_eqn.get_part_by_tex(r'\omega').copy(), omega, path_arc=120 * DEGREES),
            ReplacementTransform(i_eqn.get_part_by_tex(r'\omega').copy(), omega, path_arc=120 * DEGREES)
        )
        self.play(FadeIn(omega_defn, shift=RIGHT))
        self.play(
            omega.animate.shift(LEFT),
            omega_defn.animate.shift(LEFT),
            FadeIn(omega_approx.shift(LEFT), shift=RIGHT)
        )
        self.play(FadeOut(omega, shift=UP), FadeOut(omega_defn, shift=UP), FadeOut(omega_approx, shift=UP))
        self.remove(omega, omega_defn, omega_approx)

        self.play(eqn_group.animate.to_edge(LEFT).next_to(power_eqn_t, DOWN, aligned_edge=LEFT))

        v_phi.align_to(v_eqn, UP)
        i_phi.align_to(i_eqn, UP)
        v_phi_defn.next_to(v_phi, RIGHT)
        i_phi_defn.next_to(i_phi, RIGHT)

        self.play(TransformMatchingShapes(v_eqn.get_part_by_tex(r'\phi_v'), v_phi))
        self.play(FadeIn(v_phi_defn, shift=RIGHT))

        v_eqn_no_phi.move_to(v_eqn, aligned_edge=LEFT)

        # # don't fucking ask :sob: i know... i know...
        # # no more of that cursed bullshit...

        self.play(
            FadeOut(v_phi, shift=RIGHT),
            FadeOut(v_phi_defn, shift=RIGHT),
        )

        self.play(TransformMatchingShapes(i_eqn.get_part_by_tex(r'\phi_i').copy(), i_phi))
        self.play(FadeIn(i_phi_defn, shift=RIGHT))
        self.wait(1.0)
        self.play(FadeOut(i_phi, shift=UP), FadeOut(i_phi_defn, shift=UP))
        self.wait(2.0)

        i_eqn_new = MathTex(r"i(t)", r"=", r"I_{max} \cos(\omega t + \phi_i)").move_to(i_eqn, aligned_edge=LEFT)
        eqn_group_new = VGroup(v_eqn_no_phi, i_eqn_new)

        self.play(Unwrite(eqn_group))
        self.play(Write(eqn_group_new))

        self.play(power_eqn_t.animate.move_to(ORIGIN))

        power_eqn_p1 = MathTex(r"p(t) =", r"V_{max}\cos(\omega t)", r"i(t)", font_size=60)
        power_eqn_p2 = MathTex(r"p(t) =", r"V_{max}\cos(\omega t)", r"I_{max} \cos(\omega t + \phi_i)", font_size=60)

        self.play(Indicate(v_eqn_no_phi.get_part_by_tex(r"V_{max}\cos(\omega t)")))
        self.play(TransformMatchingTex(power_eqn_t, power_eqn_p1))
        self.play(Indicate(i_eqn_new.get_part_by_tex(r"I_{max} \cos(\omega t + \phi_i)")))
        self.play(TransformMatchingTex(power_eqn_p1, power_eqn_p2))
        self.play(power_eqn_p2.animate.to_corner(UL))
        
        self.wait(1.0)

        ohms_law = MathTex(r"V = IR")
        ohms_law_r = MathTex(r"R = \frac{V}{I}")
        o_law_eqns = VGroup(ohms_law, ohms_law_r).arrange(buff=0.25, direction=DOWN)
        self.play(Write(o_law_eqns))

        ohms_law_rt = MathTex(r"R(t) = \frac{v(t)}{i(t)}").move_to(ohms_law_r, aligned_edge=DOWN).shift(DOWN * 0.25)
        self.play(TransformMatchingTex(ohms_law_r, ohms_law_rt))
        wondering = MathTex(r"???").next_to(ohms_law_rt, DOWN)
        self.play(FadeIn(wondering, shift=DOWN))
        self.play(FadeOut(wondering, shift=DOWN))

        self.wait(1.0)


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
