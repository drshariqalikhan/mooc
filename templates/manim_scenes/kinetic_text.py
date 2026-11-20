import json
import os
from manim import *

class KineticTextScene(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        params_raw = os.environ.get("MANIM_SCENE_PARAMS", "{}")
        params = json.loads(params_raw)

        headline_text = params.get("headline", "Key Concept")
        phrases = params.get(
            "key_phrases", ["Core Idea", "Essential Takeaway"]
        )
        target_duration = float(params.get("duration", 3.0))

        # 1. Headline reveal
        headline = Text(
            headline_text,
            font_size=52,
            weight=BOLD,
            color="#38bdf8"
        ).to_edge(UP, buff=1.2)

        line = Line(LEFT * 4, RIGHT * 4, color="#38bdf8", stroke_width=2)
        line.next_to(headline, DOWN, buff=0.3)

        t_head = min(0.8, target_duration * 0.25)
        self.play(Write(headline), Create(line), run_time=t_head)

        # 2. Key phrases kinetic cascade
        phrase_group = VGroup()
        colors = ["#f8fafc", "#cbd5e1", "#94a3b8"]
        for i, p in enumerate(phrases[:3]):
            t = Text(f"• {p}", font_size=36, color=colors[i % len(colors)])
            phrase_group.add(t)

        phrase_group.arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        phrase_group.next_to(line, DOWN, buff=0.8)

        rem_time = max(0.5, target_duration - t_head)
        t_each = rem_time / max(1, len(phrase_group))

        for item in phrase_group:
            self.play(
                FadeIn(item, shift=UP * 0.3),
                item.animate.set_color("#34d399"),
                run_time=t_each * 0.6
            )
            self.wait(t_each * 0.4)
