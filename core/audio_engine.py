import json
import subprocess
import wave
from pathlib import Path
import yaml

class AudioEngine:
    def __init__(self, config_path: str = None):
        if config_path is None:
            root = Path(__file__).resolve().parent.parent
            config_path = root / "config" / "app_config.yaml"
        else:
            config_path = Path(config_path)

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        self.root = Path(__file__).resolve().parent.parent
        self.conda_env = cfg["models"]["tts"].get("conda_env", "f5tts")
        self.ref_audio = cfg["models"]["tts"].get(
            "reference_voice_path", ""
        )

    @staticmethod
    def get_wav_duration(file_path: str) -> float:
        with wave.open(str(file_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return round(frames / float(rate), 3)

    def process_cue_sheet(self, cue_sheet: dict, output_dir: str) -> dict:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        timing_data = {
            "lecture_title": cue_sheet.get("lecture_title", "Lecture"),
            "scenes": []
        }

        current_offset = 0.0
        worker_script = str(self.root / "core" / "f5tts_worker.py")

        for scene in cue_sheet.get("scenes", []):
            scene_id = scene["scene_id"]
            narration = scene["narration"]
            scene_wav = out_path / f"scene_{scene_id}.wav"

            cmd = [
                "conda", "run", "--no-capture-output",
                "-n", self.conda_env,
                "python", worker_script,
                narration, self.ref_audio, str(scene_wav)
            ]
            subprocess.run(cmd, check=True)

            duration = self.get_wav_duration(str(scene_wav))
            timing_data["scenes"].append({
                "scene_id": scene_id,
                "audio_path": str(scene_wav.resolve()),
                "start_time": current_offset,
                "end_time": round(current_offset + duration, 3),
                "duration": duration
            })
            current_offset = round(current_offset + duration, 3)

        timing_file = out_path / "timing.json"
        with open(timing_file, "w", encoding="utf-8") as f:
            json.dump(timing_data, f, indent=2)

        print(f"[AudioEngine] Timing sheet written: {timing_file}")
        return timing_data
