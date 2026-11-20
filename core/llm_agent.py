import json
import urllib.request
from pathlib import Path
import yaml

class OllamaAgent:
    def __init__(self, model_name: str = None, config_path: str = None):
        if config_path is None:
            root = Path(__file__).resolve().parent.parent
            config_path = root / "config" / "app_config.yaml"
        else:
            config_path = Path(config_path)

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)

        self.base_url = cfg["models"]["ollama"]["base_url"]
        default_pref = cfg["models"]["ollama"].get(
            "default_model", "gemma4:e4b"
        )
        target = model_name or default_pref

        # Dynamically discover installed models
        self.model = self._resolve_model(target)

    def get_available_models(self) -> list[str]:
        """Queries Ollama for currently installed local models."""
        try:
            url = f"{self.base_url}/api/tags"
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return [m["name"] for m in data.get("models", [])]
        except Exception as e:
            print(f"[Ollama] Failed to query installed models: {e}")
            return []

    def _resolve_model(self, target: str) -> str:
        installed = self.get_available_models()
        if not installed:
            print(f"[Ollama] No models detected. Falling back to: {target}")
            return target

        # 1. Exact match
        if target in installed:
            return target

        # 2. Match without tag (e.g. 'gemma4' matching 'gemma4:e4b')
        base_name = target.split(":")[0]
        for m in installed:
            if m.startswith(base_name):
                print(f"[Ollama] Matched '{target}' to installed '{m}'")
                return m

        # 3. Fallback to first available model
        selected = installed[0]
        print(f"[Ollama] '{target}' not found. Auto-selected '{selected}'")
        return selected

    def _post(self, endpoint: str, payload: dict) -> dict:
        url = f"{self.base_url}{endpoint}"
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def generate_cue_sheet(self, topic: str, context: str) -> dict:
        prompt = f"""
You are an expert online instructor. Convert the context below into a single
lecture cue sheet. Output MUST be raw valid JSON matching this structure:
{{
  "lecture_title": "string",
  "scenes": [
    {{
      "scene_id": 1,
      "scene_type": "kinetic_text",
      "narration": "Conversational speech text...",
      "visual_cue": {{
        "headline": "Main Concept",
        "key_phrases": ["term1", "term2"]
      }}
    }}
  ]
}}
Allowed scene_types: kinetic_text, concept_morph, split_comparison, diagram_flow.

Topic: {topic}
Context:
{context}
"""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        res = self._post("/api/generate", payload)
        return json.loads(res["response"])

    def unload_model(self):
        """Forces Ollama to release VRAM immediately."""
        payload = {"model": self.model, "keep_alive": 0}
        try:
            self._post("/api/generate", payload)
            print(f"[Ollama] Model '{self.model}' evicted from VRAM.")
        except Exception as e:
            print(f"[Ollama] Warning on unload: {e}")
