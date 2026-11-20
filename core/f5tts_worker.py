import sys
import traceback
from pathlib import Path

def resolve_ref_audio(user_ref: str) -> tuple[str, str]:
    # 1. Use user-specified reference if it exists
    if user_ref and Path(user_ref).exists():
        return str(Path(user_ref).resolve()), ""

    # 2. Check F5-TTS package bundled sample
    try:
        from importlib.resources import files
        bundled = files("f5_tts").joinpath("infer/examples/basic/basic_ref_en.wav")
        if Path(str(bundled)).exists():
            return str(bundled), "Some call me nature, others call me mother nature."
    except Exception:
        pass

    # 3. Check local directory discovered on your machine
    known_path = Path(r"D:\AI\F5-TTS\src\f5_tts\infer\examples\basic\basic_ref_en.wav")
    if known_path.exists():
        return str(known_path), "Some call me nature, others call me mother nature."

    return "", ""

def synthesize(text: str, ref_audio: str, output_path: str):
    out = Path(output_path).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    ref_file, ref_text = resolve_ref_audio(ref_audio)

    try:
        from f5_tts.api import F5TTS
        tts = F5TTS()
        print(f"[Worker] Synthesizing: '{text[:40]}...' using ref: '{ref_file}'")
        
        tts.infer(
            ref_file=ref_file,
            ref_text=ref_text,
            gen_text=text,
            file_wave=str(out),
            remove_silence=False
        )
        print(f"[Worker] Audio generated successfully at: {out}")
    except Exception as e:
        print(f"[Worker Error] Synthesis failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        synthesize(
            text=sys.argv[1],
            ref_audio=sys.argv[2],
            output_path=sys.argv[3]
        )
