import json
import os
from manim import *

class SplitComparisonScene(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        params = json.loads(os.environ.get("MANIM_SCENE_PARAMS", "{}"))
        headline_text = params.get("headline", "Comparison")
        left_items = params.get("items_left", ["Traditional", "Static", "Manual"])
        right_items = params.get("items_right", ["Automated", "Dynamic", "Scalable"])
        duration = float(params.get("duration", 3.0))

        headline = Text(headline_text, font_size=46, color="#38bdf8").to_edge(UP, buff=0.8)
        divider = DashedLine(UP * 2.2, DOWN * 2.8, color="#475569")
        self.play(FadeIn(headline), Create(divider), run_time=0.6)

        # Left Group (Red-tinted)
        g_left = VGroup(*[Text(f"- {t}", font_size=28, color="#fca5a5") for t in left_items[:3]])
        g_left.arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(LEFT * 3.5)

        # Right Group (Emerald-tinted)
        g_right = VGroup(*[Text(f"+ {t}", font_size=28, color="#6ee7b7") for t in right_items[:3]])
        g_right.arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT * 1.5)

        sub_time = max(0.6, (duration - 1.0) / 2)
        self.play(FadeIn(g_left, shift=RIGHT * 0.2), run_time=sub_time)
        self.play(FadeIn(g_right, shift=LEFT * 0.2), run_time=sub_time)
        self.wait(max(0.3, duration - 0.6 - (sub_time * 2)))
