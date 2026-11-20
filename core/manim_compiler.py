import json
import os
import subprocess
from pathlib import Path

class ManimCompiler:
    SCENE_MAP = {
        "kinetic_text": ("kinetic_text.py", "KineticTextScene"),
        "concept_morph": ("concept_morph.py", "ConceptMorphScene"),
        "split_comparison": ("split_comparison.py", "SplitComparisonScene"),
        "diagram_flow": ("diagram_flow.py", "DiagramFlowScene"),
    }

    def __init__(self, root_dir: str = None):
        self.root = Path(root_dir) if root_dir else Path(__file__).resolve().parent.parent
        self.templates_dir = self.root / "templates" / "manim_scenes"

    def compile_all(self, cue_sheet: dict, timing_data: dict, output_dir: str) -> list[str]:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        rendered_clips = []

        timing_map = {s["scene_id"]: s for s in timing_data.get("scenes", [])}

        for scene in cue_sheet.get("scenes", []):
            s_id = scene["scene_id"]
            s_type = scene.get("scene_type", "kinetic_text")
            timing = timing_map.get(s_id, {"duration": 3.0})

            script_file, class_name = self.SCENE_MAP.get(
                s_type, self.SCENE_MAP["kinetic_text"]
            )
            template_path = self.templates_dir / script_file

            # Merge visual cues with timing duration
            params = dict(scene.get("visual_cue", {}))
            params["duration"] = timing["duration"]

            env = os.environ.copy()
            env["MANIM_SCENE_PARAMS"] = json.dumps(params)

            cmd = [
                "manim", "-ql",
                "--media_dir", str(out_path),
                str(template_path), class_name
            ]
            print(f"[ManimCompiler] Rendering Scene {s_id} ({s_type})...")
            subprocess.run(cmd, env=env, check=True)

            # Discover rendered partial mp4
            pattern = f"**/{class_name}.mp4"
            matches = list(out_path.glob(pattern))
            if matches:
                # Rename/relocate to canonical scene file
                canonical = out_path / f"scene_{s_id}.mp4"
                if canonical.exists():
                    canonical.unlink()
                matches[-1].rename(canonical)
                rendered_clips.append(str(canonical.resolve()))

        return rendered_clips
