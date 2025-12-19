from manim import *
import numpy as np
import math

# class TrigIssues(Scene):
#     def construct(self):
#         axes = Axes(
#             x_range=[0, 10, 1],
#             y_range=[-1.5, 1.5, 0.5],
#             axis_config={"color": BLUE}
#         )
#         axes2 = Axes(
#             x_range=[0, 10, 1],
#             y_range=[-1.5, 1.5, 0.5],
#             axis_config={"color": BLUE}
#         )

#         first_wave = axes.plot(lambda x: 0.5*np.sin(x*2), color=GREEN).move_to(DOWN)
#         second_wave = axes2.plot(lambda x: 0.5*np.sin(x*2), color=BLUE).move_to(UP*2)

#         first_cos = MathTex(r"a = A_{1} \cos( \omega t - \phi)", font_size=40).move_to(DOWN*2.5)
#         second_cos= MathTex(r"b = A_{2} \cos(\omega t - \phi)", font_size=40).move_to(UP*0.5)

#         self.play(Create(first_wave), Create(second_wave), Create(first_cos), Create(second_cos))

#         self.wait(2)

#         sum_wave = axes.plot(lambda x: np.sin(x*2), color=YELLOW)        
#         init_waves = VGroup(*[first_wave, second_wave])
#         init_formulas = VGroup(*[first_cos, second_cos])
#         sum_formula = MathTex(r"c = A_{1} \cos(\omega t - \phi) +  A_{1} \cos(\omega t - \phi)", font_size=40).move_to(DOWN*2.5)
#         self.play(
#             Transform(init_waves, sum_wave),
#             Transform(init_formulas, sum_formula)
#         )
        









        

def main():
    print("Hello from v2-write-up!")


if __name__ == "__main__":
    main()
