import json
from pathlib import Path

class UdemyPacker:
    @staticmethod
    def generate_pack(cue_sheet: dict, timing_data: dict, output_dir: str, slug: str = "Lecture_01"):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        title = cue_sheet.get("lecture_title", "Lecture")
        total_time = timing_data.get("scenes", [{}])[-1].get("end_time", 0.0)
        scenes = cue_sheet.get("scenes", [])

        md_content = [
            f"# {slug}: {title}",
            f"**Estimated Duration:** {round(total_time / 60, 1)} minutes ({round(total_time, 1)}s)\n",
            "## 📌 Lecture Overview",
            f"In this lecture, students learn the fundamentals of **{title}**.\n",
            "## 🎯 Key Learning Takeaways",
        ]

        for s in scenes:
            cue = s.get("visual_cue", {})
            hl = cue.get("headline", "")
            if hl:
                md_content.append(f"- **{hl}**: {s.get('narration', '')[:100]}...")

        md_content.extend([
            "\n## 📝 End-of-Lecture Quiz",
            f"1. **What is the primary topic covered in this lesson?**",
            f"   - [ ] A) Unrelated concept",
            f"   - [x] B) {title}",
            f"   - [ ] C) Legacy methodologies",
            f"   - [ ] D) None of the above\n",
            f"2. **Which core component was highlighted during the visual breakdown?**",
            f"   - [x] A) {scenes[0].get('visual_cue', {}).get('headline', 'Core Component')}",
            f"   - [ ] B) Default configuration",
            f"   - [ ] C) Manual overrides",
            f"   - [ ] D) External dependencies"
        ])

        kit_file = out / f"{slug}_Udemy_Kit.md"
        kit_file.write_text("\n".join(md_content), encoding="utf-8")
        print(f"[UdemyPacker] Course packaging kit written: {kit_file.name}")
