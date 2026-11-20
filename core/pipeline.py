import sys
from pathlib import Path

# Ensure project root is always first in sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.ingestion import DocumentLoader
from core.llm_agent import OllamaAgent
from core.audio_engine import AudioEngine
from core.manim_compiler import ManimCompiler
from core.video_assembler import VideoAssembler
from core.udemy_packer import UdemyPacker

def run_pipeline(doc_path: str):
    inter_dir = ROOT / "workspace" / "intermediate"
    out_dir = ROOT / "workspace" / "output"

    print("\n==========================================")
    print("   MOOC STUDIO: AUTONOMOUS PRODUCTION     ")
    print("==========================================\n")

    # Step 1: Document Ingestion
    print(f"[1/5] Ingesting document: {doc_path}")
    raw_text = DocumentLoader.load(doc_path)
    topic = Path(doc_path).stem.replace("_", " ").title()

    # Step 2: Ollama Script Generation + VRAM Eviction
    print("[2/5] Synthesizing script & visual cue sheet via Ollama...")
    llm = OllamaAgent()
    cue_sheet = llm.generate_cue_sheet(topic, raw_text[:2500])
    print(f"      Title: {cue_sheet.get('lecture_title')}")
    print(f"      Scenes: {len(cue_sheet.get('scenes', []))}")
    llm.unload_model()

    # Step 3: F5-TTS Audio & Timing Sheet
    print("[3/5] Synthesizing narration audio via F5-TTS...")
    audio_eng = AudioEngine()
    timing_data = audio_eng.process_cue_sheet(cue_sheet, str(inter_dir))

    # Step 4: Manim Programmatic Vector Rendering
    print("[4/5] Rendering animated visual scenes via Manim...")
    compiler = ManimCompiler()
    clips = compiler.compile_all(cue_sheet, timing_data, str(inter_dir))

    # Step 5: Assembly & Course Packaging
    print("[5/5] Assembling video, subtitles, and Udemy kit...")
    assembler = VideoAssembler()
    final_video = assembler.assemble_lecture(
        cue_sheet, timing_data, clips, str(out_dir), "Lecture_01"
    )
    UdemyPacker.generate_pack(cue_sheet, timing_data, str(out_dir), "Lecture_01")

    print("\n==========================================")
    print("[✓] PRODUCTION COMPLETE!")
    print(f"    Video:     {final_video}")
    print(f"    Subtitles: {out_dir / 'Lecture_01.srt'}")
    print(f"    Udemy Kit: {out_dir / 'Lecture_01_Udemy_Kit.md'}")
    print("==========================================\n")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "workspace/input/sample.txt"
    run_pipeline(target)
