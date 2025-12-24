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
            "○ KCL and KVL",
            "○ Pre-Calculus (Trigonometric Functions and Identities)",
            alignment='left',
            font_size=36
        ).to_corner(UL, buff=0.5)
        
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

        with self.voiceover("This video assumes basic knowledge of the following concepts from DC Circuit Analysis and Pre-Calculus.."):
            self.play(Write(assumed_topics), run_time=1.5)
            self.wait(tracker.duration)

        self.play(Unwrite(assumed_topics))

class PowerLawScene(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(transcription_model=None))

        power_eqn = MathTex(r"P =", r"V", r"I", font_size=60)
        power_eqn_t = MathTex(r"p(t)", r"=", r"v(t)", r"i(t)", font_size=60).next_to(power_eqn, DOWN)

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


        with self.voiceover("You may know that the power of a particular device in a DC Circuit is computed as P = V times I.") as tracker:
            self.play(Write(power_eqn))
            self.wait()

        with self.voiceover("However, unlike in AC Circuits,") as tracker:
            pass

        with self.voiceover("V and I are just static values and don't change over time.") as tracker:
            self.play(Indicate(power_eqn.get_part_by_tex(r'V')))
            self.play(Indicate(power_eqn.get_part_by_tex(r'I')))
            self.wait()

        with self.voiceover("Well, in AC, we can just turn these variables, V and I, into their functional counterparts,") as tracker:
            self.play(ReplacementTransform(power_eqn.copy(), power_eqn_t))
            self.play(power_eqn_t.animate.move_to(ORIGIN), FadeOut(power_eqn, shift=UP))
            self.remove(power_eqn)
            self.wait()

        self.play(power_eqn_t.animate.to_corner(UL))

        with self.voiceover("v of t and "):
            self.play(Indicate(power_eqn_t.get_part_by_tex(r'v(t)')))
            self.play(ReplacementTransform(power_eqn_t.get_part_by_tex(r'v(t)').copy(), v_eqn.get_part_by_tex(r'v(t)'), path_arc=-120 * DEGREES))
            self.play(ReplacementTransform(v_eqn.get_part_by_tex(r'v(t)'), v_eqn))

        with self.voiceover("i of t"):
            self.play(Indicate(power_eqn_t.get_part_by_tex(r'i(t)')))
            self.play(ReplacementTransform(power_eqn_t.get_part_by_tex(r'i(t)').copy(), i_eqn.get_part_by_tex(r'i(t)'), path_arc=-120 * DEGREES))
            self.play(ReplacementTransform(i_eqn.get_part_by_tex(r'i(t)'), i_eqn))

        with self.voiceover("Of course, this also has the effect of making P turn into a function of time as well, p of t!"):
            self.play(Indicate(power_eqn_t.get_part_by_tex(r'p(t)')))

        with self.voiceover("In our case, we are only interested in AC circuits that power our appliances. In particular, the Philippine power grid is set to have a sinusoid voltage with a V RMS of 220 Volts.") as tracker:
            pass

        self.play(MoveToTarget(v_max), MoveToTarget(i_max))
        self.play(FadeIn(v_max_defn, shift=RIGHT))
        self.play(FadeIn(i_max_defn, shift=RIGHT))

        with self.voiceover("Thus v of t and i of t have the following mathematical forms, where V max is V RMS times square root of 2 and I max is I RMS times square root of 2.") as tracker:
            pass

        self.play(FadeOut(v_max, shift=UP), FadeOut(v_max_defn, shift=UP), FadeOut(i_max, shift=DOWN), FadeOut(i_max_defn, shift=DOWN))
        self.remove(v_max, v_max_defn, i_max, i_max_defn)

        
        with self.voiceover("Both of these functions have omega in the argument and since our electricity in the Philippines runs at a frequency of 60 Hertz, this would actually be equal to ") as tracker:
            self.play(
                ReplacementTransform(v_eqn.get_part_by_tex(r'\omega').copy(), omega, path_arc=120 * DEGREES),
                ReplacementTransform(i_eqn.get_part_by_tex(r'\omega').copy(), omega, path_arc=120 * DEGREES)
            )

        with self.voiceover("2 pi 60 or approximately 377. Conventionally, this is the number engineers use to approximate calculations.") as tracker: 
            self.play(FadeIn(omega_defn, shift=RIGHT))
            self.play(
                omega.animate.shift(LEFT),
                omega_defn.animate.shift(LEFT),
                FadeIn(omega_approx.shift(LEFT), shift=RIGHT)
            )

        with self.voiceover("However, to stay mathematically precise, let's just keep it to be omega.") as tracker:
            pass

        self.play(FadeOut(omega, shift=UP), FadeOut(omega_defn, shift=UP), FadeOut(omega_approx, shift=UP))
        self.remove(omega, omega_defn, omega_approx)

        self.play(eqn_group.animate.to_edge(LEFT).next_to(power_eqn_t, DOWN, aligned_edge=LEFT))

        v_phi.align_to(v_eqn, UP)
        i_phi.align_to(i_eqn, UP)
        v_phi_defn.next_to(v_phi, RIGHT)
        i_phi_defn.next_to(i_phi, RIGHT)

        with self.voiceover("As you'll see later, phi v is actually zero, since it would be our *reference* waveform.") as tracker: 
            self.play(TransformMatchingShapes(v_eqn.get_part_by_tex(r'\phi_v'), v_phi))
            self.play(FadeIn(v_phi_defn, shift=RIGHT))

            v_eqn_no_phi.move_to(v_eqn, aligned_edge=LEFT)

        with self.voiceover("What this means would be more apparent in the next slide. But if you've used an oscilloscope before, this is the same as setting a particular channel to be what triggers the oscilloscope to take a snapshot of a waveform.") as tracker:
            pass

        self.play(
            FadeOut(v_phi, shift=RIGHT),
            FadeOut(v_phi_defn, shift=RIGHT),
        )

        with self.voiceover("And it follows that whatever phi i is would just be relative to the phase of the voltage since that was what we chose to be our reference waveform.") as tracker:
            self.play(TransformMatchingShapes(i_eqn.get_part_by_tex(r'\phi_i').copy(), i_phi))
            self.play(FadeIn(i_phi_defn, shift=RIGHT))

        self.wait(1.0)

        with self.voiceover("But let's cover that later, as what I mean by 'relative to the phase of voltage' would be a lot more obvious in a visualization.") as tracker:
            self.play(FadeOut(i_phi, shift=UP), FadeOut(i_phi_defn, shift=UP))
            self.wait(2.0)

        with self.voiceover("Our voltage and current functions would then have the following form:") as tracker:
            pass
            i_eqn_new = MathTex(r"i(t)", r"=", r"I_{max} \cos(\omega t + \phi_i)").move_to(i_eqn, aligned_edge=LEFT)
            eqn_group_new = VGroup(v_eqn_no_phi, i_eqn_new)

        self.play(Unwrite(eqn_group))
        self.play(Write(eqn_group_new))

        self.play(power_eqn_t.animate.move_to(ORIGIN))
        with self.voiceover("Which has this effect on the power function:") as tracker:
            power_eqn_p1 = MathTex(r"p(t) =", r"V_{max}\cos(\omega t)", r"i(t)", font_size=60)
            power_eqn_p2 = MathTex(r"p(t) =", r"V_{max}\cos(\omega t)", r"I_{max} \cos(\omega t + \phi_i)", font_size=60)

            self.play(Indicate(v_eqn_no_phi.get_part_by_tex(r"V_{max}\cos(\omega t)")))
            self.play(TransformMatchingTex(power_eqn_t, power_eqn_p1))
            self.play(Indicate(i_eqn_new.get_part_by_tex(r"I_{max} \cos(\omega t + \phi_i)")))
            self.play(TransformMatchingTex(power_eqn_p1, power_eqn_p2))
            self.play(power_eqn_p2.animate.to_corner(UL))
            self.wait(1.0)

        with self.voiceover("Now you may recall that these two functions are related to one another by the AC counterpart of resistance, impedance.") as tracker:
            pass

        ohms_law = MathTex(r"V = IR")
        ohms_law_r = MathTex(r"R = \frac{V}{I}")
        o_law_eqns = VGroup(ohms_law, ohms_law_r).arrange(buff=0.25, direction=DOWN)
        ohms_law_rt = MathTex(r"R(t) = \frac{v(t)}{i(t)}").move_to(ohms_law_r, aligned_edge=DOWN).shift(DOWN * 0.25)
        with self.voiceover("This follows from the Ohm's Law of DC Circuits where V is equal to I times R, or if rearranged, R is equal to V over I.") as tracker:

            self.play(Write(o_law_eqns))
            self.wait(tracker.duration)

            self.play(TransformMatchingTex(ohms_law_r, ohms_law_rt))


        with self.voiceover("But here we see two problems,"):
            pass

        with self.voiceover("Number 1."):
            pass

        with self.voiceover("P of t is a multiplication of sinusoids which is difficult to calculate."):
            self.play(Indicate(power_eqn_p2))

        with self.voiceover("Number 2."):
            pass

        with self.voiceover("It seems our impedance is a function of time, but we know that the impedance in a circuit is constant!"):
            wondering = MathTex(r"???").next_to(ohms_law_rt, DOWN)
            self.wait(0.65)
            self.play(FadeIn(wondering, shift=DOWN))
            self.wait(0.5)
            self.play(FadeOut(wondering, shift=DOWN))

        with self.voiceover("Okay, how about we approach this from a visual perspective. Let's try graphing v of t and i of t!"):
            pass

        self.wait(2.0)

class PhasorAnalysisAssumptions(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(transcription_model=None))

        euler_iden = MathTex(r"Ae^{jx}", r"=", r"A\cos(x)", r"+ Aj\sin(x)")
        euler_iden_rp = MathTex(r"\operatorname{Re}(", r"Ae^{jx}", r")", r"=", r"A\cos(x)")
        euler_iden_rp_t1 = VGroup(
            MathTex(r"\operatorname{Re}(", r"Ae^{jx}", r")", r"=", r"A\cos(x)", ","),
            Tex(r"Let $x = \omega t$")
        ).arrange(RIGHT)
        euler_iden_wt1 = MathTex(r"\operatorname{Re}(", r"Ae^{j(\omega t)}", r")", r"=", r"A\cos(\omega t)")
        euler_iden_wt2 = MathTex(r"A\cos(\omega t)",  r"=", r"\operatorname{Re}(", r"Ae^{j(\omega t)}", r")",)

        euler_iden_factored1 = MathTex(
            r"Ae^{jx}", r"=",
            r"\operatorname{Re}(" r"Ae^{jx}", r")", r"+",
            r"\operatorname{Im}(" r"Ae^{jx}", r")"
        )
        euler_iden_factored2 = MathTex(
            r"Ae^{jx}", r"=",
            r"\operatorname{Re}(" r"Ae^{jx}", r")", r"+",
            r"\operatorname{Im}(" r"Ae^{jx}", r")"
        )
        
        v_func_iden1 = MathTex(
            r"v(t)", r" = V_{max}", r"\cos(\omega t)"
        )
        v_func_iden2 = MathTex(
            r"v(t)", r"=", "\operatorname{Re}(", r"V_{max}", r"e^{j(\omega t)}", r")"
        )
        v_func_iden3 = MathTex(
            r"v(t)", r"=", "\operatorname{Re}(", r"V_{max}", r"e^{j\omega t}", r")"
        )
        v_func_iden4 = MathTex(
            r"v(t)", r"=",
            "\operatorname{Re}(", r"e^{j\omega t}", r")",
            r"\big[", r"V_{max}", r"\big]"
        )

        i_func_iden1 = MathTex(
            r"i(t)", r"=", "\operatorname{Re}(", r"I_{max}", r"e^{j(\omega t + \phi_i)}", r")"
        )
        i_func_iden2 = MathTex(
            r"i(t)", r"=", "\operatorname{Re}(", r"I_{max}", r"e^{j\omega t}", r"\cdot", r"e^{j\phi_i}", r")"
        )
        i_func_iden3 = MathTex(
            r"i(t)",  r"=",
            "\operatorname{Re}(", r"e^{j\omega t}", r")",
            r"\big[",
            r"I_{max}", r"\cdot", "\operatorname{Re}(", r"e^{j\phi_i}", r")",
            r"\big]"
        )

        p_func1 = MathTex(
            r"p(t)", r"=", r"v(t)", r"\cdot", r"i(t)"
        )
        p_func2 = MathTex(
            r"p(t)", r"=", r"\big[",
            r"\operatorname{Re}(", r"V_{max}", "e^{j\omega t}", r")", r"\big]", r"\cdot", r"\big[",
            r"\operatorname{Re}(", r"I_{max}", r"e^{j\omega t}", r"\cdot", r"e^{j\phi_i}", r")"
            r"\big]",
        )
        p_func3 = MathTex(
            r"p(t)", r"=", r"\big[",
            r"V_{max}", r"\operatorname{Re}(", "e^{j\omega t}", r")", r"\big]", r"\cdot",
            r"\big[",
            r"I_{max}", r"\operatorname{Re}(", r"e^{j\omega t}", r")", r"\cdot",
            r"\operatorname{Re}(", r"e^{j\phi_i}", r")", r"\big]",
        )
        p_func4 = MathTex(
            r"p(t)", r"=", r"\operatorname{Re}(", "e^{j\omega t}", r")",
            r"\big[", r"V_{max}", r"\big]", r"\cdot",
            r"\big[", r"I_{max}", r"\operatorname{Re}(", r"e^{j\phi_i}", r")", r"\big]",
        )

        v_phasor = MathTex(
            r"\vec{V}", r"=", r"V_{max}", r"\angle{0^{\circ}}"
        )

        i_phasor = MathTex(
            r"\vec{I}", r"=", r"I_{max}", r"\angle{\phi_i}"
        )

        s_phasor_p1 = MathTex(
            r"\vec{S}", r"=", r"\vec{V}", r"\cdot", r"\vec{I}^*"
        )

        s_phasor_p2 = MathTex(
            r"\vec{S}", r"=", r"V_{max}\angle{0^{\circ}}", r"\cdot", r"I_{max}", r"\angle{-\phi_i}"
        )

        with self.voiceover(
        """I will assume the viewer already has an idea about the engineering
        counterpart of the euler's formula."""
        ) as tracker:
            self.play(Write(euler_iden))

        with self.voiceover(
        """as you can see, this is a complex number with the cosine as the real part and the sine as the
        imaginary part."""
        ):
            pass

        with self.voiceover(
        """Taking the real part of this complex number just leaves us with cosine."""
        ) as tracker:
            self.play(
                AnimationGroup(
                    FadeOut(euler_iden, shift=UP),
                    FadeIn(euler_iden_rp, shift=UP),
                    lag_ratio=-0.25                      
                )
            )

        with self.voiceover(
        """And if we let x be equal to omega t. We get a cosine wave that's similar to our voltage and current sinusoids."""
        ) as tracker:
            self.play(TransformMatchingTex(euler_iden_rp, euler_iden_rp_t1))
            self.wait(1.0)
            self.play(TransformMatchingTex(euler_iden_rp_t1, euler_iden_wt1))

        ###############################################################
        with self.voiceover(
        """We can then apply this identity on the voltage function.
        """
        ):
            self.play(
                AnimationGroup(
                    euler_iden_wt1.animate.shift(UP * 0.75),
                    FadeIn(v_func_iden1, shift=UP),
                    lag_ratio=-0.25                      
                )
            )
            self.wait(1.5)
            euler_iden_wt2.move_to(euler_iden_wt1)
            self.play(TransformMatchingTex(v_func_iden1, v_func_iden2), TransformMatchingTex(euler_iden_wt1, euler_iden_wt2))

        self.play(
            AnimationGroup(
                FadeOut(euler_iden_wt2, shift=UP),
                v_func_iden2.animate.to_corner(UL),
                lag_ratio=0.80
            )
        )
        v_func_iden3.move_to(v_func_iden2, aligned_edge=LEFT)
        self.play(TransformMatchingTex(v_func_iden2, v_func_iden3))

        ###############################################################

        with self.voiceover(
        """Similarly, apply the same identity on the current function.
        """
        ):
            self.play(FadeIn(i_func_iden1, shift=UP))


        with self.voiceover(
        """And apply the exponential rule for addition. The reason for this will be obvious in a moment.
        """
        ):
            self.play(TransformMatchingTex(i_func_iden1, i_func_iden2))
            self.wait(1.25)
            self.play(i_func_iden2.animate.next_to(v_func_iden3, aligned_edge=LEFT, direction=DOWN))

        v_func_iden4.move_to(v_func_iden3, aligned_edge=LEFT)
        i_func_iden3.move_to(i_func_iden2, aligned_edge=LEFT)

        ###############################################################

        with self.voiceover(
        """Now let's bring in the power function.
        """
        ):
            self.play(FadeIn(p_func1, shift=UP))

        with self.voiceover(
        """Substituting in the functions on the top left.
        """
        ):
            self.play(TransformMatchingTex(p_func1, p_func2))
            self.play(Indicate(VGroup(*p_func2[3:7]), scale_factor=1.05))
            self.play(Indicate(VGroup(*v_func_iden3[2:]), scale_factor=1.05))
            self.play(Indicate(VGroup(*p_func2[10:15]), scale_factor=1.05))
            self.play(Indicate(VGroup(*i_func_iden2[2:]), scale_factor=1.05))

        with self.voiceover(
        """Notice how they have a common factor? Specifically the real part of the complex exponential e raised to j omega t? Let's factor that out.
        """
        ):
            self.play(TransformMatchingTex(p_func2, p_func3))

        self.play(TransformMatchingTex(p_func3, p_func4))

        with self.voiceover(
        """Let's make the functions on the top left have a similar form as well.
        """
        ):
            self.play(TransformMatchingTex(v_func_iden3, v_func_iden4))
            self.play(TransformMatchingTex(i_func_iden2, i_func_iden3))

        v_phasor.move_to(v_func_iden4, aligned_edge=LEFT)
        i_phasor.move_to(i_func_iden3, aligned_edge=LEFT)

        with self.voiceover(
        """Notice how they all have a factor of e raised to j omega t? You can interpret this as the factor that
        makes them related to one another! Since they're all multiplied to one another, we can *temporarily forget*
        this complex exponential just to leave out what really matters: V max, I max, and the phase shift phi i.
        """
        ):
            self.play(TransformMatchingTex(v_func_iden4, v_phasor), TransformMatchingTex(i_func_iden3, i_phasor))
            self.play(
                AnimationGroup(
                    FadeOut(p_func4, shift=UP),
                    FadeIn(s_phasor_p1, shift=UP),
                    lag_ratio=-0.25                      
                )
            )

        self.play(TransformMatchingTex(s_phasor_p1, s_phasor_p2))
        self.play(s_phasor_p2.animate.next_to(i_phasor, aligned_edge=LEFT, direction=DOWN))

        phasors = VGroup(v_phasor, i_phasor, s_phasor_p2)

        with self.voiceover(
            """These are called Phasors which are numbers in the complex plane and this makes analyzing ac circuits much easier as you'll see
            later. """
        ):
            self.play(Circumscribe(phasors))

        with self.voiceover(
            """Do note that the key assumption that enabled us to represent it in this way is the fact that both the voltage and current
            waveforms share the same frequency, you wouldn't be able to do this otherwise."""
        ):
            self.play(Indicate(v_phasor), Indicate(i_phasor))
            pass
        

        self.play(Unwrite(phasors))

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
