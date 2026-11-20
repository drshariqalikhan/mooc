from pathlib import Path
from pypdf import PdfReader

class DocumentLoader:
    @staticmethod
    def load(file_path: str) -> str:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")

        suffix = path.suffix.lower()
        if suffix in [".txt", ".md"]:
            with open(path, "r", encoding="utf-8") as f:
                return f.read().strip()
        elif suffix == ".pdf":
            reader = PdfReader(path)
            extracted = [
                page.extract_text() or ""
                for page in reader.pages
            ]
            return "\n".join(extracted).strip()
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    @staticmethod
    def chunk_by_words(text: str, max_words: int = 1200) -> list[str]:
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_words):
            chunks.append(" ".join(words[i:i + max_words]))
        return chunks
