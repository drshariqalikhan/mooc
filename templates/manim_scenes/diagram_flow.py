import json
import os
from manim import *

class DiagramFlowScene(Scene):
    def construct(self):
        self.camera.background_color = "#0f172a"

        params = json.loads(os.environ.get("MANIM_SCENE_PARAMS", "{}"))
        headline_text = params.get("headline", "Process Architecture")
        nodes = params.get("nodes", ["Ingest", "Synthesize", "Render", "Publish"])
        duration = float(params.get("duration", 3.0))

        headline = Text(headline_text, font_size=46, color="#38bdf8").to_edge(UP, buff=1.0)
        self.play(FadeIn(headline), run_time=0.5)

        # Create sequential flowchart nodes
        node_objs = []
        for name in nodes[:4]:
            box = RoundedRectangle(corner_radius=0.15, height=1.0, width=2.2, color="#38bdf8")
            txt = Text(name, font_size=24, color=WHITE).move_to(box.get_center())
            node_objs.append(VGroup(box, txt))

        chain = VGroup(*node_objs).arrange(RIGHT, buff=0.6).shift(DOWN * 0.3)
        arrows = [
            Arrow(node_objs[i].get_right(), node_objs[i+1].get_left(), buff=0.1, color="#94a3b8")
            for i in range(len(node_objs) - 1)
        ]

        t_elem = max(0.4, (duration - 1.0) / len(node_objs))
        for i, node in enumerate(node_objs):
            self.play(GrowFromCenter(node), run_time=t_elem * 0.7)
            if i < len(arrows):
                self.play(Create(arrows[i]), run_time=t_elem * 0.3)
        self.wait(max(0.3, duration - 0.5 - (t_elem * len(node_objs))))
