from manim import *
import numpy as np
import math
from numpy import pi
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

class PhasorTime(VoiceoverScene):
    def construct(self):
        self.set_speech_service(GTTSService(transcription_model=None))
        V_COL = YELLOW
        I_COL = ManimColor("#41FF17")
        P_COL = BLUE

        ax = Axes(
            x_range=[-pi/6, 2*(2*pi), pi/3],
            y_range=[-3.0, 3.0, 0.5],
            x_length=7,
            y_length=4,
            axis_config={'color': BLUE, 'tip_width': 0.1, 'tip_height': 0.1},
        ).to_edge(LEFT, buff=0.75)
        plane = NumberPlane(
            x_range=(-3.125, 3.125, 0.5),
            y_range=(-2.5, 2.5, 0.5),
            x_length=5,
            y_length=4
        ).to_edge(RIGHT, buff=0.75)
        
        v_phasor_eqn = MathTex(
            r"\vec{V}", r"=", r"V_{max}", r"\angle{0^{\circ}}",
            font_size=28
        )
        i_phasor_eqn = MathTex(
            r"\vec{I}", r"=", r"I_{max}", r"\angle{\phi_i}",
            font_size=28
        )
        s_phasor_eqn = MathTex(
            r"\vec{S}", r"=", r"\vec{V}", r"\vec{I}^*", r"=", r"V_{max}\angle{0^{\circ}}", r"\cdot", r"I_{max}", r"\angle{-\phi_i}",
            font_size=28
        )
        eqns = MathTex(r"v(t) &= V_{max}\cos(\omega t) \\",
                       r"i(t) &= I_{max}\cos(\omega t + \phi_i) \\",
                       r"p(t) &= v(t)i(t)", font_size=28).next_to(ax, UP, aligned_edge=LEFT, buff=0.1)

        v_max = ValueTracker(1.0)
        i_max = ValueTracker(1.0)
        v_max_text = VGroup(
            MathTex(r"|\vec{V}| = V_{max} =", font_size=42),
            DecimalNumber(
                v_max.get_value(),
                font_size=42
            ).add_updater(lambda x: x.set_value(v_max.get_value()))
        ).arrange(RIGHT, buff=0.125)
        i_max_text = VGroup(
            MathTex(r"|\vec{I}| = I_{max} =", font_size=42),
            DecimalNumber(
                i_max.get_value(),
                font_size=42
            ).add_updater(lambda x: x.set_value(i_max.get_value()))
        ).arrange(RIGHT, buff=0.125)

        v_phase = ValueTracker(0)
        v_wave = always_redraw(
            lambda: ax.plot(lambda t: v_max.get_value() * np.cos(t + v_phase.get_value()), color=V_COL)
        )
        v_phasor = always_redraw(
            lambda: Arrow(
                start=plane.c2p(0, 0, 0),
                end=plane.c2p(
                    v_max.get_value() * np.cos(v_phase.get_value()),
                    v_max.get_value() * np.sin(v_phase.get_value()),
                    0
                ),
                buff=0,
                tip_length=0.25,  # Always 0.25 units
                stroke_width=4.5,
                color=V_COL
            )
        )

        i_phase = ValueTracker(0.0)
        i_wave = always_redraw(
            lambda: ax.plot(lambda t: i_max.get_value() * np.cos(t + i_phase.get_value()), color=I_COL)
        )
        i_phasor = always_redraw(
            lambda: Arrow(
                start=plane.c2p(0, 0, 0),
                end=plane.c2p(
                    i_max.get_value() * np.cos(i_phase.get_value()),
                    i_max.get_value() * np.sin(i_phase.get_value()),
                    0
                ),
                buff=0,
                tip_length=0.25,
                stroke_width=4.5,
                color=I_COL
            )
        )

        i_phase_text = VGroup(
            MathTex(r"\phi_i =").set_color(I_COL),
            DecimalNumber(
                i_phase.get_value(),
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            ).add_updater(lambda x: x.set_value(i_phase.get_value()))
        ).arrange()
        i_phasor_angle = always_redraw(
            lambda: Arc(
                radius=0.20,
                start_angle=0,
                angle=i_phase.get_value(),
                arc_center=plane.c2p(0, 0, 0),
                color=I_COL,
            ) if abs(i_phase.get_value()) > 0.01 else VMobject()
        )

        # def point_proportion(angle, arc):
        #     if abs(angle) > 0.01:
        #         return (0, 0, 0)
        #     else:
        #         return plane.c2p(1, 1, 0)
                # return i_phasor_angle.point_from_proportion(0.5)
        
        # i_phase_symbol = always_redraw(
        #     lambda: MathTex(
        #         r"\phi_i", color=I_COL).move_to(
        #             point_proportion(i_phase.get_value(), i_phasor_angle)
        #         ) if abs(i_phase.get_value()) > 0.01 else VMobject()
        # )
        s_phase_text = VGroup(
            MathTex(r"-\phi_i =").set_color(P_COL),
            DecimalNumber(
                i_phase.get_value(),
                show_ellipsis=True,
                num_decimal_places=2,
                include_sign=True,
            ).add_updater(lambda x: x.set_value(-i_phase.get_value()))
        ).arrange().set_opacity(0.0)
        s_phasor_angle = always_redraw(
            lambda: Arc(
                radius=0.20,
                start_angle=0,
                angle=-i_phase.get_value(),
                arc_center=plane.c2p(0, 0, 0),
                color=P_COL,
            ) if abs(i_phase.get_value()) > 0.01 else VMobject()
        )
        # s_phase_symbol = always_redraw(
        #     lambda: MathTex(
        #         r"-\phi_i", color=P_COL).move_to(
        #             point_proportion(i_phase.get_value(), s_phasor_angle)
        #         ) if abs(i_phase.get_value()) > 0.01 else VMobject()
        # )
        p_wave = always_redraw(
            lambda: ax.plot(
                lambda t: v_max.get_value() * i_max.get_value() *
                np.cos(t + v_phase.get_value()) *
                np.cos(t + i_phase.get_value()),
                color=P_COL
            )
        )
        s_phasor = always_redraw(
            lambda: Arrow(
                start=plane.c2p(0, 0, 0),
                end=plane.c2p(
                    v_max.get_value() * i_max.get_value() * np.cos(i_phase.get_value()) * np.cos(v_phase.get_value()),
                    v_max.get_value() * i_max.get_value() * np.sin(-i_phase.get_value()),
                    0
                ),
                buff=0,
                tip_length=0.25,
                stroke_width=4.5,
                color=P_COL
            )
        )

        phasor_eqns = VGroup(v_phasor_eqn, i_phasor_eqn, s_phasor_eqn).arrange(DOWN, aligned_edge=LEFT, buff=0.125).next_to(plane, UP, aligned_edge=LEFT, buff=0.1)
        max_values = VGroup(v_max_text, i_max_text).arrange(DOWN, buff=0.05)
        phase_values = VGroup(i_phase_text, s_phase_text).arrange(DOWN, buff=0.05)
        moving_values = VGroup(max_values, phase_values).arrange(RIGHT, buff=1.0).to_edge(DOWN)

        with self.voiceover(
        """Now let us take a look at the phasor representation of our functions!
        """
        ):
            self.play(Create(ax), Create(plane))
            self.play(Write(eqns), Write(phasor_eqns))
            pass

        with self.voiceover(
        """Let's put the time domain representation of the functions on the axes on the left.
        """
        ):
            self.play(Circumscribe(ax))
            self.play(Create(v_wave), Create(i_wave))

        with self.voiceover(
        """Similarly, let's also put the phasor domain representation of the functions on the
        plane on the right.
        """
        ):
            self.play(Circumscribe(plane))
            self.play(Create(v_phasor), Create(i_phasor))

        with self.voiceover(
        """On the bottom right, i'll display and change the values that affect the power output. These
        are V max, I max, and the phase shift of current phi i.
        """
        ):
            self.play(Write(i_phasor_angle), Write(moving_values))

        with self.voiceover(
        """Watch closely how changes in the waveform map to the phasor in the plane.
        """
        ):
            self.play(v_max.animate.set_value(0.5), run_time=1.5)
            self.play(v_max.animate.set_value(2.2), run_time=1.5)
            self.play(i_max.animate.set_value(0.8), run_time=1.5)
            self.play(i_max.animate.set_value(1.2), run_time=1.5)
            self.play(i_phase.animate.set_value(pi / 3), run_time=1.0)
            self.play(i_phase.animate.set_value(-pi / 3), run_time=1.0)
            self.play(i_phase.animate.set_value(-pi / 6), run_time=1.0)
            self.play(i_phase.animate.set_value(pi / 4), run_time=1.0)

        
        s_phasor.update()
        p_wave.update()
        with self.voiceover(
        """And since the complex power S is defined as the product of these two, with one being the conjugate
        the resulting power phasor would look like this.
        """
        ):
            self.play(Create(p_wave), s_phase_text.animate.set_opacity(1.0),
                      Create(s_phasor), Create(s_phasor_angle))

        with self.voiceover(
        """Focus closely on how this angle is just a reflection of the angle between the voltage and current phasors.
        """
        ):
            self.play(FocusOn(s_phasor_angle))
            self.play(Indicate(s_phase_text))
            self.play(Indicate(s_phasor_angle, scale_factor=2.0))

        with self.voiceover(
        """It is inverted precisely because of the definition of the complex power phasor.
        """
        ):
            self.play(Indicate(VGroup(s_phasor_eqn[3], s_phasor_eqn[7], s_phasor_eqn[8])))

        with self.voiceover(
        """Now let us try changing the constants within the voltage and current functions to see
        how this actually affects the power phasor.
        """
        ):
            self.play(v_max.animate.set_value(0.5), run_time=1.7)
            self.play(v_max.animate.set_value(2.2), run_time=1.3)
            self.play(i_max.animate.set_value(0.8), run_time=1.0)
            self.play(i_max.animate.set_value(1.2), run_time=1.8)
            self.play(i_phase.animate.set_value(pi / 3), run_time=1.2)
            self.play(i_phase.animate.set_value(-pi / 3), run_time=1.4)
            self.play(i_phase.animate.set_value(-pi / 6), run_time=0.8)
            self.play(i_phase.animate.set_value(pi / 4), run_time=1.0)

        pass

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
