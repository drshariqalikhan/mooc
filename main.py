import sys
from pathlib import Path
from core.pipeline import run_pipeline

if __name__ == "__main__":
    doc = sys.argv[1] if len(sys.argv) > 1 else "workspace/input/microservices_guide.txt"
    run_pipeline(doc)
