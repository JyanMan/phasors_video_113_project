from manim import *
from manim_voiceover import VoiceoverScene
from manim_voiceover.services.recorder import RecorderService
from manim_voiceover.services.gtts import GTTSService

class VoiceoverTest(VoiceoverScene):
    def construct(self):
        self.set_speech_service(RecorderService(transcription_model=None))
        # self.set_speech_service(GTTSService())
        
        hello_text = Text("Hello World!")
        box = Square()
        circle = Circle()
        
        with self.voiceover("This is a text writing hello world!"):
            self.play(Write(hello_text))
            self.wait(2.0)

        with self.voiceover("Now I'm going to turn it into a box!"):
            self.wait(1.0)
            self.play(ReplacementTransform(hello_text, box))
            self.wait(2.5)

        with self.voiceover("...and into a circle!"):
            self.play(ReplacementTransform(box, circle))
