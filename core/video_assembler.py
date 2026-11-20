import json
import subprocess
from pathlib import Path
import yaml

class VideoAssembler:
    def __init__(self, config_path: str = None):
        if config_path is None:
            root = Path(__file__).resolve().parent.parent
            config_path = root / "config" / "app_config.yaml"
        else:
            config_path = Path(config_path)

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        self.codec = cfg["video"].get("ffmpeg_codec", "h264_nvenc")

    @staticmethod
    def _sec_to_srt(seconds: float) -> str:
        hrs = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        ms = int(round((seconds - int(seconds)) * 1000))
        return f"{hrs:02d}:{mins:02d}:{secs:02d},{ms:03d}"

    def build_subtitles(self, cue_sheet: dict, timing_data: dict, out_srt: Path):
        timing_map = {s["scene_id"]: s for s in timing_data.get("scenes", [])}
        entries = []
        for idx, scene in enumerate(cue_sheet.get("scenes", []), 1):
            s_id = scene["scene_id"]
            timing = timing_map.get(s_id, {})
            start = self._sec_to_srt(timing.get("start_time", 0.0))
            end = self._sec_to_srt(timing.get("end_time", 3.0))
            text = scene.get("narration", "")
            entries.append(f"{idx}\n{start} --> {end}\n{text}\n")
        out_srt.write_text("\n".join(entries), encoding="utf-8")

    def assemble_lecture(
        self,
        cue_sheet: dict,
        timing_data: dict,
        video_clips: list[str],
        output_dir: str,
        lecture_slug: str = "Lecture_01"
    ) -> Path:
        out = Path(output_dir).resolve()
        out.mkdir(parents=True, exist_ok=True)
        timing_map = {s["scene_id"]: s for s in timing_data.get("scenes", [])}
        muxed_clips = []

        for v_path in video_clips:
            vp = Path(v_path).resolve()
            if not vp.exists():
                raise FileNotFoundError(f"Video segment not found: {vp}")

            s_id = 1
            for part in vp.stem.split("_"):
                if part.isdigit():
                    s_id = int(part)
                    break

            timing = timing_map.get(s_id, {})
            a_path = timing.get("audio_path")
            if not a_path or not Path(a_path).exists():
                raise FileNotFoundError(f"Audio file missing for scene {s_id}: {a_path}")

            muxed_part = out / f"muxed_{s_id}.mp4"
            
            # Fast stream copy: video stream is copied directly, audio encoded to AAC
            cmd = [
                "ffmpeg", "-y",
                "-i", str(vp),
                "-i", str(a_path),
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                str(muxed_part)
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"[FFmpeg Error]\n{res.stderr}")
                res.check_returncode()
            muxed_clips.append(muxed_part)

        concat_txt = out / "concat_list.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for p in muxed_clips:
                clean_path = str(p.resolve()).replace("\\", "/")
                f.write(f"file '{clean_path}'\n")

        final_mp4 = out / f"{lecture_slug}.mp4"
        cmd_concat = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            str(final_mp4)
        ]
        res_cat = subprocess.run(cmd_concat, capture_output=True, text=True)
        if res_cat.returncode != 0:
            print(f"[FFmpeg Concat Error]\n{res_cat.stderr}")
            res_cat.check_returncode()

        srt_file = out / f"{lecture_slug}.srt"
        self.build_subtitles(cue_sheet, timing_data, srt_file)
        return final_mp4
