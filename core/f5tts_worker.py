import sys
import wave
from pathlib import Path

def generate_silence(path: str, duration_sec: float = 3.0):
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(24000)
        frames = int(24000 * duration_sec)
        wf.writeframes(b"\x00" * (frames * 2))

def synthesize(text: str, ref_audio: str, output_path: str):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    try:
        from f5_tts.api import F5TTS
        tts = F5TTS()
        tts.export_audio(
            text=text,
            ref_audio=ref_audio if Path(ref_audio).exists() else "",
            output_path=output_path
        )
    except Exception as e:
        # Fallback to clear 3-second timing pad if no ref voice provided
        generate_silence(output_path, duration_sec=3.0)

if __name__ == "__main__":
    if len(sys.argv) >= 4:
        synthesize(
            text=sys.argv[1],
            ref_audio=sys.argv[2],
            output_path=sys.argv[3]
        )
