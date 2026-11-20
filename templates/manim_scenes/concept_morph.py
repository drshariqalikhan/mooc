import json
import os
from manim import *

class ConceptMorphScene(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        params = json.loads(os.environ.get("MANIM_SCENE_PARAMS", "{}"))
        headline_text = params.get("headline", "Transformation")
        phrases = params.get("key_phrases", ["Input", "Output"])
        duration = float(params.get("duration", 3.0))

        # 1. Headline
        headline = Text(headline_text, font_size=48, color="#38bdf8").to_edge(UP, buff=1.0)
        self.play(FadeIn(headline, shift=DOWN * 0.2), run_time=0.6)

        # 2. Initial Object (Box + Text)
        box1 = RoundedRectangle(corner_radius=0.2, height=2.2, width=3.8, color="#f43f5e")
        txt1 = Text(phrases[0], font_size=32, color=WHITE).move_to(box1.get_center())
        grp1 = VGroup(box1, txt1)

        # 3. Target Object (Circle + Text)
        box2 = Circle(radius=1.6, color="#34d399")
        txt2 = Text(phrases[-1], font_size=32, color=WHITE).move_to(box2.get_center())
        grp2 = VGroup(box2, txt2)

        self.play(Create(grp1), run_time=0.8)
        
        # Morph duration scaled to remaining time
        morph_time = max(0.8, duration - 2.0)
        self.play(ReplacementTransform(grp1, grp2), run_time=morph_time)
        self.wait(max(0.4, duration - 1.4 - morph_time))
