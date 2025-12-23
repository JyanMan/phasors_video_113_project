import numpy as np
import math

from numpy import pi

from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService
from helper import play_replace_trans_full

class PlottingScene(Scene):
    def construct(self):
        V_MAX = 1.0
        I_MAX = 1.0
        V_COL = YELLOW
        I_COL = ManimColor("#41FF17")
        P_COL = BLUE
        
        # ax = Axes(
        #     x_range=[-pi/6, 2*(2*pi), pi/3],
        #     y_range=[-1.5, 1.5, 0.5],
        #     x_length=8,
        #     axis_config={'color': BLUE, 'tip_width': 0.1, 'tip_height': 0.1},
        #     # tips=False
        # ).to_edge(LEFT)

        ax_x_min = ValueTracker(-pi/6)
        ax_x_max = ValueTracker(2*(2*pi))
        ax = always_redraw(
            lambda: Axes(
                x_range=[ax_x_min.get_value(), ax_x_max.get_value(), pi/3],
                y_range=[-1.5, 1.5, 0.5],
                x_length=8,
                axis_config={'color': BLUE, 'tip_width': 0.1, 'tip_height': 0.1},
                # tips=False
            ).to_corner(UL)
        )

        eqns = MathTex(r"v(t) &= V_{max}\cos(\omega t) \\",
                       r"i(t) &= I_{max}\cos(\omega t + \phi_i) \\",
                       r"p(t) &= v(t)i(t)").to_corner(UR).shift(RIGHT * 0.25)
        eqns.set_color_by_tex(r"v(t) &= V_{max}\cos(\omega t) \\", V_COL)
        eqns.set_color_by_tex(r"i(t) &= I_{max}\cos(\omega t + \phi_i)", I_COL)
        eqns.set_color_by_tex(r"p(t) &= v(t)i(t)", P_COL)
        v_eqn = eqns.get_part_by_tex(r"v(t) &= V_{max}\cos(\omega t) \\")
        i_eqn = eqns.get_part_by_tex(r"i(t) &= I_{max}\cos(\omega t + \phi_i)")
        p_eqn = eqns.get_part_by_tex(r"p(t) &= v(t)i(t)")

        # p_eqn_p1 = MathTex(r"p(t) = (V_{max}\cos(\omega t))(I_{max}\cos(\omega t + \phi_i))")
        # p_eqn_p2 = MathTex(r"p(t) = I_{max}V_{max}\cos(\omega t)\cos(\omega t + \phi_i)")
        # p_eqn_p3 = MathTex(r"p(t) = \frac{V_{max}I_{max}}{2}[\cos((\omega t) - (\omega t + \phi_i)) + \cos((\omega t) + (\omega t + \phi_i))]")
        # p_eqn_p4 = MathTex(r"p(t) = \frac{V_{max}I_{max}}{2}[\cos(\phi_i) + \cos(2\omega t + \phi_i))]")
        p_eqn_p1 = MathTex(
            r"p(t)", r"=", 
            r"V_{max}", r"\cos(\omega t)", 
            r"I_{max}", r"\cos(\omega t + \phi_i)",
            color=P_COL
        )

        p_eqn_p2 = MathTex(
            r"p(t)", r"=", 
            r"I_{max}", r"V_{max}",
            r"\cos(\omega t)",
            r"\cos(\omega t + \phi_i)",
            color=P_COL
        )

        p_eqn_p3 = MathTex(
            r"p(t)", r"=", 
            r"\frac{V_{max}I_{max}}{2}", r"\bigg[",
            r"\cos\Big((\omega t) - (\omega t + \phi_i)\Big)", r"+",
            r"\cos\Big((\omega t) + (\omega t + \phi_i)\Big)",
            r"\bigg]",
            font_size=38,
            color=P_COL
        )

        p_eqn_p4 = MathTex(
            r"p(t)", r"=", 
            r"\frac{V_{max}I_{max}}{2}", r"\left[",
            r"\cos(-\phi_i)", r"+",
            r"\cos(2\omega t + \phi_i)",
            r"\right]",
            color=P_COL
        )

        trig_iden = MathTex(r"\cos(A)\cos(B) = \frac{1}{2}\bigg[\cos(A - B) + \cos(A + B)\bigg]", font_size=42).set_color(GRAY)
        p_eqn_p5 = MathTex(
            r"p(t)", r"=",
            r"v(t)", r"\sum_{i=1}^{n}", r"i_{n}(t)",
            color=P_COL
        ).move_to(p_eqn, aligned_edge=LEFT).shift(DOWN * 0.5)

        v_phase = ValueTracker(0)
        v_wave = always_redraw(
            lambda: ax.plot(lambda t: V_MAX * np.cos(t + v_phase.get_value()), x_range=[ax_x_min.get_value(), ax_x_max.get_value()], color=V_COL)
        )

        i_phase = ValueTracker(90 * DEGREES)
        i_phase_text = VGroup(
            MathTex(r"\phi_i =").set_color(I_COL),
            DecimalNumber(
                i_phase.get_value(),
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            ).add_updater(lambda x: x.set_value(i_phase.get_value()))
        ).arrange().to_corner(DR, buff=1.5)

        i_phase_vals_degr = [
            MathTex(r"+360^{\circ}").set_color(GRAY),
            MathTex(r"-360^{\circ}").set_color(GRAY),
            MathTex(r"+180^{\circ}").set_color(GRAY),
            MathTex(r"-180^{\circ}").set_color(GRAY),
        ]

        i_wave = always_redraw(
            lambda: ax.plot(lambda t: I_MAX * np.cos(t + i_phase.get_value()), x_range=[ax_x_min.get_value(), ax_x_max.get_value()], color=I_COL)
        )

        p_wave = always_redraw(
            lambda: ax.plot(lambda t: V_MAX * I_MAX * np.cos(t + v_phase.get_value()) * np.cos(t + i_phase.get_value()), x_range=[ax_x_min.get_value(), ax_x_max.get_value()], color=P_COL)
        )

        v_wave_start = Dot((0, 0, 0), color=V_COL)

        i_wave_start = Dot(
            point=ax.c2p(-i_phase.get_value(), I_MAX),
            color=I_COL
        ).add_updater(
            lambda x: x.move_to(ax.c2p(-i_phase.get_value(), I_MAX))
        )

        phase_angle_circ = Circle(radius=1, color=WHITE).next_to(i_phase_text, UP).shift(UP * 0.5)
        phase_angle_ref = Line(phase_angle_circ.get_center(), phase_angle_circ.point_at_angle(0), color=WHITE)
        phase_angle_ray = Line(
            phase_angle_circ.get_center(), phase_angle_circ.point_at_angle(i_phase.get_value()),
            color=WHITE
        ).add_updater(
            lambda x: x.become(phase_angle_ref.copy()).rotate(
                i_phase.get_value(), about_point=phase_angle_circ.get_center()
            )
        )
        phase_angle_angle = always_redraw(
            lambda: Arc(
                radius=phase_angle_circ.radius / 5.0,
                start_angle=0,
                angle=i_phase.get_value(),
                arc_center=phase_angle_circ.get_center(),
            ) if abs(i_phase.get_value()) > 0.01 else VMobject()
        )

        phase_angle_var = MathTex(r'\phi_i').move_to(phase_angle_circ.get_center()).shift(DOWN * 0.25).scale(0.75).shift(RIGHT * 0.125)

        self.add(ax)

        self.wait(1.0)
        self.add(v_wave)
        self.play(v_phase.animate(rate_func=linear).set_value(50), run_time=1.0)
        self.play(v_phase.animate(rate_func=linear).set_value(100), run_time=1.0)
        self.play(v_phase.animate(rate_func=linear).set_value(150), run_time=1.0)
        self.play(v_phase.animate(rate_func=smooth).set_value(0), run_time=0.25)
        self.play(Indicate(v_wave, scale_factor=1.05, color=V_COL), Write(v_eqn))

        self.add(i_wave)
        self.play(Indicate(i_wave, scale_factor=1.05, color=I_COL), Write(i_eqn))

        self.play(Create(p_wave))
        self.play(Indicate(p_wave, scale_factor=1.05), Write(p_eqn))

        self.play(p_eqn.animate.center().to_edge(DOWN).shift(UP * 1.0))

        p_eqn_p1.move_to(p_eqn)

        self.play(ReplacementTransform(p_eqn, p_eqn_p1))
        p_eqn_p2.move_to(p_eqn_p1)
        self.play(TransformMatchingTex(p_eqn_p1, p_eqn_p2))
        trig_iden.next_to(p_eqn_p1, DOWN)
        self.play(FadeIn(trig_iden, shift=UP))
        self.play(FadeOut(trig_iden, shift=UP))
        p_eqn_p3.move_to(p_eqn_p2)
        self.play(TransformMatchingTex(p_eqn_p2, p_eqn_p3))
        p_eqn_p4.move_to(p_eqn_p2)
        self.play(TransformMatchingTex(p_eqn_p3, p_eqn_p4))
        self.remove(p_eqn_p3)

        self.play(p_eqn_p4.animate.to_edge(DOWN))

        self.play(Write(i_phase_text))
        for tex in i_phase_vals_degr:
            tex.next_to(i_phase_text, UP).shift(RIGHT * 0.25)

        self.play(
            ax_x_min.animate.set_value(-pi/6 - i_phase.get_value()),
            ax_x_max.animate.set_value(2*(2*pi) - i_phase.get_value())
        )

        self.play(Create(i_wave_start))
        self.play(FocusOn(i_wave_start))

        # 360 degrees to the left and to the right
        self.play(
            LaggedStart(
                AnimationGroup(
                    ax_x_min.animate.set_value(-pi/6 - 12*(30*DEGREES)),
                    ax_x_max.animate.set_value(2*(2*pi) - 12*(30*DEGREES)),
                ),
                i_phase.animate.set_value(12 * (30 * DEGREES)), lag_ratio=0.25
            ), run_time=3.5
        )
        self.play(FadeIn(i_phase_vals_degr[0], shift=UP))
        self.play(FadeOut(i_phase_vals_degr[0], shift=UP))
        
        self.play(
            LaggedStart(
                i_phase.animate.set_value(-12 * (30 * DEGREES)),
                AnimationGroup(
                    ax_x_min.animate.set_value(-pi/6),
                    ax_x_max.animate.set_value(2*(2*pi)),
                ), lag_ratio=0.25
            ), run_time=3.5
        )
        self.play(FadeIn(i_phase_vals_degr[1], shift=UP))
        self.play(FadeOut(i_phase_vals_degr[1], shift=UP))

        # # 180 degrees to the left and to the right
        self.play(
            LaggedStart(
                AnimationGroup(
                    ax_x_min.animate.set_value(-pi/6 - 12*(30*DEGREES)),
                    ax_x_max.animate.set_value(2*(2*pi) - 12*(30*DEGREES)),
                ),
                i_phase.animate.set_value(6 * (30 * DEGREES)), lag_ratio=0.25
            ), run_time=3.5
        )
        self.play(FadeIn(i_phase_vals_degr[2], shift=UP))
        self.play(FadeOut(i_phase_vals_degr[2], shift=UP))
        
        self.play(
            LaggedStart(
                i_phase.animate.set_value(-6 * (30 * DEGREES)),
                AnimationGroup(
                    ax_x_min.animate.set_value(-pi/6),
                    ax_x_max.animate.set_value(2*(2*pi)),
                ), lag_ratio=0.25
            ), run_time=3.5
        )
        self.play(FadeIn(i_phase_vals_degr[3], shift=UP))
        self.play(FadeOut(i_phase_vals_degr[3], shift=UP))


        ########################################################################
        # demo the circularity of the phase shift
        
        self.play(i_phase.animate.set_value(90 * DEGREES))
        phase_angle_ray.update()
        self.play(GrowFromCenter(phase_angle_circ))
        self.play(GrowFromEdge(phase_angle_ray, LEFT), GrowFromEdge(phase_angle_ref, LEFT))
        self.play(Create(phase_angle_angle), Create(phase_angle_var))
        self.play(
            LaggedStart(
                AnimationGroup(
                    ax_x_min.animate.set_value(-pi/6 - 12*(30*DEGREES)),
                    ax_x_max.animate.set_value(2*(2*pi) - 12*(30*DEGREES)),
                ),
                i_phase.animate.set_value(6 * (30 * DEGREES)), lag_ratio=0.25
            ), run_time=2.5
        )
        self.play(
            LaggedStart(
                i_phase.animate.set_value(-6 * (30 * DEGREES)),
                AnimationGroup(
                    ax_x_min.animate.set_value(-pi/6),
                    ax_x_max.animate.set_value(2*(2*pi)),
                ), lag_ratio=0.25
            ), run_time=2.5
        )

        self.play(
            FadeOut(phase_angle_circ, shift=DOWN), FadeOut(phase_angle_ray, shift=DOWN),
            FadeOut(phase_angle_ref, shift=DOWN), FadeOut(phase_angle_angle, shift=DOWN),
            FadeOut(phase_angle_var, shift=DOWN)
        )

        # demo the circularity of the phase shift
        ########################################################################


        self.play(Write(i_phase_text))
        for tex in i_phase_vals_degr:
            tex.next_to(i_phase_text, UP).shift(RIGHT * 0.25)

        self.play(Create(i_wave_start))
        self.play(FocusOn(i_wave_start))

        circuits = [SVGMobject('circ1.svg'), SVGMobject('circ2.svg'), SVGMobject('circ3.svg')]
        for c in circuits:
            c.set_color(WHITE)
            c.to_edge(RIGHT).shift(LEFT)

        # inductor negative phi, current lags voltage
        # negative phi = later in time
        self.play(
            LaggedStart(
                FadeIn(circuits[0], shift=DOWN),
                i_phase.animate.set_value(-75 * DEGREES),
                lag_ratio=0.75
            ), run_time=3.5
        )
        self.wait(1.0)

        # resistive 0 phi, current in phase voltage
        # 0 phi = same time
        self.play(
            LaggedStart(
                TransformMatchingShapes(circuits[0], circuits[1]),
                i_phase.animate.set_value(0 * DEGREES),
                lag_ratio=0.75
            ), run_time=3.5
        )
        self.wait(1.0)

        # capacitive positive phi, current leads voltage
        # positive phi = earlier in time
        self.play(
            LaggedStart(
                TransformMatchingShapes(circuits[1], circuits[2]),
                i_phase.animate.set_value(75 * DEGREES),
                lag_ratio=0.75
            ), run_time=3.5
        )
        self.wait(1.0)
        self.play(FadeOut(circuits[2], shift=DOWN))

        self.play(Uncreate(i_wave_start))
        self.play(i_phase.animate.set_value(90 * DEGREES))

        i_waves_more = [
            ax.plot(lambda t: 0.25 * np.cos(t + 30 * DEGREES), color=GREEN_A),
            ax.plot(lambda t: 0.35 * np.cos(t + 60 * DEGREES), color=GREEN_C),
            ax.plot(lambda t: 0.80 * np.cos(t + 90 * DEGREES), color=GREEN_E)
        ]
        p_waves_more = [
            p_wave.copy(),
            ax.plot(
                lambda t: V_MAX * I_MAX * np.cos(t + v_phase.get_value()) * np.cos(t + i_phase.get_value()) * 0.25 * np.cos(t + 30 * DEGREES),
                x_range=[ax_x_min.get_value(), ax_x_max.get_value()], color=P_COL
            ),
            ax.plot(
                lambda t: V_MAX * I_MAX * np.cos(t + v_phase.get_value()) * np.cos(t + i_phase.get_value()) * 0.35 * np.cos(t + 60 * DEGREES),
                x_range=[ax_x_min.get_value(), ax_x_max.get_value()], color=P_COL
            ),
            ax.plot(
                lambda t: V_MAX * I_MAX * np.cos(t + v_phase.get_value()) * np.cos(t + i_phase.get_value()) * 0.80 * np.cos(t + 90 * DEGREES),
                    x_range=[ax_x_min.get_value(), ax_x_max.get_value()], color=P_COL
            ),
        ]

        i_eqn_new = MathTex(r"i_{n}(t)", r" &= I_{max}\cos(\omega t + \phi_i)", color=I_COL).move_to(i_eqn, aligned_edge=LEFT).shift(LEFT * 0.25)
        self.play(ReplacementTransform(i_eqn, i_eqn_new))
        self.play(ReplacementTransform(p_eqn_p4, p_eqn_p5))

        for i, wave in enumerate(i_waves_more):
            self.play(Create(wave))
            self.remove(p_wave)
            self.play(ReplacementTransform(p_waves_more[i], p_waves_more[i + 1]))
            self.wait(1.0)

        vt_distr = p_eqn_p5.get_part_by_tex(r'v(t)').copy()
        vt_distr_rot_pt = p_eqn_p5.get_part_by_tex(r"\sum_{i=1}^{n}").get_center()
        vt_distr.generate_target()
        vt_distr.target.move_to(p_eqn_p5.get_part_by_tex(r"i_{n}(t)").get_center()).scale(0.0)
        self.play(Rotate(vt_distr, angle=-120 * DEGREES, about_point=vt_distr_rot_pt))
        self.play(MoveToTarget(vt_distr))

        self.wait(5.0)


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
            self.play(v_text.animate().center().to_edge(UP).to_edge(LEFT).shift(RIGHT))
            self.play(Create(curr_wave_end), Uncreate(volt_wave_end))

        # init current wave
        with self.voiceover("and current waveforms that come out of your outlet") as tracker:
            curr_wave_end.add_updater(lambda f: f.move_to(curr_wave.get_end()))
            self.play(Create(curr_wave), run_time=1)
            self.play(Write(i_text_end_curr_wave()), run_time=0.5)
            self.play(i_text.animate().next_to(v_text, DOWN, aligned_edge=LEFT))
            self.play(Uncreate(curr_wave_end))


        with self.voiceover(
            "and as we learned from school, these waveforms are\
            mathematically defined as a sinusoid with amplitude\
            V max and I max respectively of voltage and current"
        ) as tracker:
            # voltage formula
            self.wait(6)
            v_text = play_replace_trans_full(self, v_text, v_text_formula(), run_time=1)
            # current formula
            i_text = play_replace_trans_full(self, i_text, i_text_formula())


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
        p_of_t = MathTex(
            "p(t)", font_size=50, color=MAROON_C
        ).move_to(power_wave.get_end()).shift(RIGHT*0.5)
        def p_of_t_formula():
            return MathTex(
                r"p(t) = v(t)i(t)",
                color=MAROON_C,
                font_size=50
            ).to_edge(UP).shift(DOWN*0.5)

        phase_group = self.create_phase_indicator(axes)
        start_line = phase_group[0]
        end_line = phase_group[1]
        i_phase = phase_group[4]
        def i_phase_with_placeholder():
            return MathTex(
                r"\phi =", r"\phantom{+0.00}",
                font_size=50,
                color=GREEN
            ).move_to(i_phase.get_left()).shift(RIGHT*0.5)
        i_phase_val = DecimalNumber(0)
        def i_phase_value():
            i_phase_val = DecimalNumber(
                number=curr_phase.get_value(),
                num_decimal_places=2,
                color=BLUE_C,
            ).move_to(i_phase.get_right()).shift(RIGHT*0.5)
            return i_phase_val
        def i_phase_updater(mob):
            value = curr_phase.get_value()
            mob.set_value(value)

        def i_formula_with_placeholder():
            return  MathTex(
                r"i(t) = I_{max} \cos(", r"2\pi 60t", r"\phantom{+}", r"\phantom{0.00}", r")",
                substrings_to_isolate=[r"\phi"],
                font_size=50,
                color=GREEN
            ).move_to(i_formula.get_center()).shift(RIGHT*0.2)

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

        phase_number = MathTex(
            r"+0.00",
            color=BLUE_C,
            font_size=50,
        # ).move_to(i_formula.get_right()).shift(LEFT*2)
        )
        def phase_number_init():
            return phase_number.move_to(i_formula.get_right()).shift(LEFT*0.8)            

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

        purely_res_load = Text(
            "Purely Resistive Load", color=BLUE_C, font_size=40
        ).to_edge(RIGHT).shift(DOWN*2)

        def phase_in_pi_terms():
            return MathTex(
                r"\approx 2\pi",
                color=PINK
            ).move_to(i_phase.get_right()).shift([0.2, -0.5, 0])

        #### ANIMATION START ####

        self.play(Create(power_wave), run_time=2)
        self.play(Create(p_of_t), run_time=0.5)
        self.play(
            FadeOut(v_formula),
            i_formula.animate().to_edge(DOWN)
        )
        play_replace_trans_full(self, p_of_t, p_of_t_formula())
        self.play(
            self.phase_to_zero_animation(phase_group),
            curr_phase.animate().set_value(0),
            pow_phase.animate().set_value(0),
            pow_offset.animate().set_value(0),
            run_time=3
        )

        i_phase = play_replace_trans_full(self, i_phase, i_phase_with_placeholder())
        self.play(
            FadeOut(end_line), FadeOut(start_line),
            # Create(i_phase_with_placeholder()),
            Create(i_phase_value())
        )

        # focus on phi / i_phase
        self.play(
            FadeToColor(i_phase, color=BLUE_C),
            FadeToColor(i_formula[3], color=BLUE_C)
        )
        i_formula = play_replace_trans_full(self, i_formula, i_formula_with_placeholder())
        i_phase_val.add_updater(i_phase_updater)

        self.play(Create(phase_number_init()))
        phase_number.add_updater(phase_number_updater)

        # shift the current left and right
        pow_offset.add_updater(pow_offset_follow_current)

        # purely resistive load
        self.play(Create(purely_res_load))

        self.wait(2)
        
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
            run_time=8
        )

        # add approximation of phase in terms of pi
        self.play(Create(phase_in_pi_terms()), run_time=0.5)

        # PRE FADE OUT WITH EDITOR NALANG


