# mooc# MOOC Studio: Autonomous Course Production Pipeline

> **Repository:** [drshariqalikhan/mooc](https://github.com/drshariqalikhan/mooc.git)  
> **Target Output:** High-production, kinetic video lecture series formatted for platforms like Udemy/Coursera from raw documents.  
> **Execution Profile:** 100% Local, zero external API dependencies, single-click desktop launch.

---

## 🤖 LLM Handover Protocol & Operational Rules

> **MANDATORY INSTRUCTION FOR ANY AI ASSISTANT WORKING ON THIS REPOSITORY:**
> 1. **Read-Before-Writing:** Before generating any configuration, code, or documentation, inspect this `README.md` to identify the current active phase, completed milestones, and strict hardware constraints.
> 2. **Rule of Continuous Update:** Whenever you complete, modify, or advance a step, you **must update this README** immediately. Adjust the task checkboxes (`[ ]` → `[x]`), update the `Current Active Phase` indicator, and append brief notes to the `Changelog & Session Notes` section at the bottom.
> 3. **Hardware Invariance:** Do **not** suggest or implement solutions that require cloud APIs (OpenAI, ElevenLabs, Runway) or violate the memory constraints below. All components must run within the specified local hardware bounds.
> 4. **No Code Sprawl:** Maintain the directory tree defined in this document. Do not invent divergent frameworks unless explicitly directed.

---

## 🖥️ Target System Specs & Constraints

All pipeline components must respect the following local machine parameters:

| Component | Specification | Operational Constraint |
| :--- | :--- | :--- |
| **CPU** | Intel Core i9-9900K (8C/16T @ 3.60 GHz) | Cairo / OpenGL software rendering & pipeline orchestration |
| **System RAM**| 16.0 GB DDR4 | Max active system RAM ceiling: ~12 GB (safe margin) |
| **GPU** | NVIDIA GeForce RTX 2080 Ti (**11.0 GB VRAM**) | **Strict single-tenant VRAM policy** (No concurrent LLM + TTS) |
| **Storage** | ~1.0 TB Free NVMe/SSD | High-bitrate intermediate video frame cache |
| **OS** | Windows 10/11 64-bit | PowerShell / Conda environment execution |

### ⚠️ Non-Negotiable Architecture Constraints
1. **The Sequential Baton Pass (VRAM Management):**
   * Ollama and F5-TTS **must never run concurrently in GPU memory**.
   * The pipeline must load Ollama, run inference, generate structured outputs, and trigger an explicit memory release (`unload`) before F5-TTS initializes.
   * After F5-TTS synthesizes audio and extracts timing offsets, its VRAM must be freed before video rendering begins.
2. **Templated Manim Architecture (No Dynamic Hallucinated Code):**
   * The LLM **must not** generate arbitrary, raw Python Manim scripts from scratch.
   * The visual engine must rely on **pre-built, rock-solid Manim scene templates** (Kinetic Typography, Split Comparison, Node Flowcharts, Diagram Morphs).
   * The LLM only populates a validated, strict **JSON Cue Sheet** that parameterizes these pre-tested templates.

---

## 🏗️ Core Pipeline Architecture
[Raw Input Document] (.pdf / .txt / .md)
│
▼
┌────────────────────────────────────────────────────────┐
│ Phase 2: Curriculum & Script Engine (Ollama) │
│ - Chunk into 4-8 min micro-lectures │
│ - Generate spoken script + JSON visual cue sheets │
│ - Release Ollama VRAM │
└────────────────────────┬───────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│ Phase 3: Speech Synthesis Engine (F5-TTS) │
│ - Generate high-fidelity narration audio │
│ - Extract millisecond word/phrase timestamps │
│ - Release F5-TTS VRAM │
└────────────────────────┬───────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│ Phase 4: Kinetic Visual Engine (Manim Community) │
│ - Inject JSON cues + durations into Manim templates │
│ - Render vector-crisp 1080p motion scenes │
└────────────────────────┬───────────────────────────────┘
│
▼
┌────────────────────────────────────────────────────────┐
│ Phase 5: Audio-Visual Assembly (FFmpeg + NVENC) │
│ - Mux Manim scene segments with F5-TTS master track │
│ - Export 1080p MP4 + Synchronized .SRT Subtitles │
│ - Output course metadata & student assessment sheet │
└────────────────────────────────────────────────────────┘

---

## 📁 Repository Directory Structure

```text
mooc/
├── README.md                      <-- Source of truth & progress ledger
├── launch.bat                     <-- One-click desktop execution script
├── requirements.txt               <-- Python dependency manifest
├── config/
│   ├── app_config.yaml            <-- System, paths, and model configurations
│   └── course_profile.yaml        <-- Default pedagogical style & slide themes
├── core/
│   ├── __init__.py
│   ├── ingestion.py               <-- Document parsing & chunking
│   ├── llm_agent.py               <-- Ollama client & prompt orchestration
│   ├── audio_engine.py            <-- F5-TTS wrapper & timestamp alignment
│   ├── manim_compiler.py          <-- Maps JSON cue sheets to Manim scenes
│   └── video_assembler.py         <-- FFmpeg stitching, subtitle & NVENC export
├── templates/
│   ├── schemas/                   <-- JSON schemas for visual cue sheets
│   └── manim_scenes/              <-- Parameterized Manim templates
│       ├── kinetic_text.py
│       ├── concept_morph.py
│       ├── split_comparison.py
│       └── diagram_flow.py
├── ui/                            <-- Minimal local web interface
│   ├── index.html
│   └── app.py
└── workspace/                     <-- Working directory for project runs (gitignored)
    ├── input/
    ├── intermediate/              <-- Temporary audio wavs, cue JSONs, and video clips
    └── output/                    <-- Final courses (MP4, SRT, Quizzes)
🚦 Implementation Roadmap & Live Status
Current Active Phase: Phase 1: Environment Baseline & Project Scaffold
Phase 1: Environment Baseline & Project Scaffold

Document verified working versions of Conda, Python, Ollama, F5-TTS, and FFmpeg.

Create base directory layout and .gitignore (ignore intermediate video/audio caches).

Create config/app_config.yaml to specify default paths, model names, and resolution targets.

Verify GPU NVENC availability via FFmpeg CLI.
Phase 2: Ingestion & Pedagogical Cue Generation (Ollama)

Implement document loader (PDF, Markdown, plain text) with token-aware chunking.

Design robust prompt chains for:
Curriculum Architect (Splits source text into a structured syllabus).
Lecture Scriptwriter (Writes spoken script in conversational lecturer tone).

Formalize the cue_sheet.schema.json definition (links spoken sentences to animation actions).

Implement VRAM release trigger to shut down / evict the Ollama model after generation.
Phase 3: Speech Synthesis & Timing Extraction (F5-TTS)

Implement local F5-TTS wrapper taking script text segments and reference voice audio.

Implement sentence/clause duration and word-level timestamp extraction.

Save master narrative audio (.wav) alongside aligned timing metadata (timing.json).

Ensure full VRAM deallocation upon audio synthesis completion.
Phase 4: Parameterized Manim Template Library

Build KineticTextScene (Word-by-word reveal, focus glow, dynamic scale-up).

Build ConceptMorphScene (Smooth shape/icon/text vector interpolation).

Build SplitComparisonScene (Two-sided comparative matrix with check/cross animations).

Build DiagramFlowScene (Programmatic node/arrow sequence).

Build manim_compiler.py to ingest cue_sheet.json + timing.json and programmatically render each scene.
Phase 5: Assembly & Course Packaging (FFmpeg)

Automate seamless stitching of generated Manim video chunks.

Multiplex final video with high-bitrate F5-TTS master audio track using NVIDIA NVENC.

Auto-generate synchronized .srt and .vtt subtitle tracks from timing metadata.

Auto-generate Udemy-ready artifacts: course summary markdown, bulleted outcomes, and end-of-module multiple-choice quiz questions.
Phase 6: One-Click Desktop Launcher & UI

Build lightweight local dashboard (clean UI to drop documents, pick voices, and preview scripts).

Create launch.bat to launch the environment silently and open Chrome/Edge in --app standalone mode.

Add end-to-end integration test (1-page test document to finished 2-minute MP4).
📝 Changelog & Session Handover Notes
Use this section to record progress at the end of each session so the next LLM or engineer can resume instantly.
Initial Setup: Documented project architecture, system hardware limits (RTX 2080 Ti 11GB / 16GB RAM), and sequential execution strategy. Defined strict handover protocol and directory scaffold. Ready to commence Phase 1.
