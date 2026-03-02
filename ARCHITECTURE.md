

# Adaptive Assistant Architecture Guide

## CRITICAL FILE: config/vad.py

This is THE most important file for fixing STT (speech-to-text) problems.

### Quick Parameter Reference

| Parameter | Default | Problem | Solution |
|-----------|---------|---------|----------|
| ENERGY_THRESHOLD | 0.045 | Hallucinating | Increase to 0.06-0.10 |
| NO_SPEECH_THRESHOLD | 0.92 | "I'm sorry" on silence | Increase to 0.94-0.98 |
| LOGPROB_THRESHOLD | -0.4 | Low confidence outputs | Make less negative: -0.2 to 0.0 |
| PREROLL_SECONDS | 0.15 | First word clipped | Increase to 0.20-0.30 |
| MIN_SPEECH_SEC | 0.48 | Missing words | Decrease to 0.25-0.35 |
| MIN_AUDIO_SEC | 0.65 | Short hallucinations | Increase to 0.80-1.0 |
| COMPRESSION_RATIO_THRESHOLD | 1.5 | Music transcribing | Decrease to 0.8-1.2 |
| TRANSCRIBE_EVERY | 0.6 | Slow feedback | Decrease to 0.3-0.4 |

---

## Key Configuration Files (In Priority Order)

### 1. config/vad.py (CRITICAL - STT Quality)
File: `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config/vad.py`

**What it controls:**
- VAD (Voice Activity Detection) sensitivity → when to start/stop transcription
- Whisper confidence thresholds → accept/reject transcriptions
- Preroll buffer → capture audio before speech detected

**To fix:**

**Hallucinating on silence:**
\`\`\`python
NO_SPEECH_THRESHOLD = 0.96        # was 0.92
LOGPROB_THRESHOLD = -0.2          # was -0.4  
COMPRESSION_RATIO_THRESHOLD = 1.0 # was 1.5
\`\`\`

**Missing words from real speech:**
\`\`\`python
ENERGY_THRESHOLD = 0.03        # was 0.045
MIN_SPEECH_SEC = 0.35          # was 0.48
PREROLL_SECONDS = 0.25         # was 0.15
\`\`\`

**Background music transcribing:**
\`\`\`python
COMPRESSION_RATIO_THRESHOLD = 0.8  # was 1.5
NO_SPEECH_THRESHOLD = 0.95         # was 0.92
ENERGY_THRESHOLD = 0.07            # was 0.045
\`\`\`

---

### 2. config/features.py (Mode Selection)
File: `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config/features.py`

**What it controls:**
- Which mode to run: stt_only, tts_only, text_to_text_chat, voice_to_text_chat, full, server

**To change mode:**
\`\`\`python
MODE = "voice_to_text_chat"  # Change to: "stt_only", "tts_only", "full", etc.
\`\`\`

---

### 3. config/llm.py (LLM Quality)
File: `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config/llm.py`

**What it controls:**
- TEMPERATURE: 0.0=boring, 1.0+=creative
- n_ctx: context size (2048=default, reduce to 1024 for speed)
- MODEL_PATH: which LLM to use

**To make responses more creative:**
\`\`\`python
TEMPERATURE = 1.2  # was 0.7
\`\`\`

**To speed up LLM:**
\`\`\`python
N_CTX = 1024  # was 2048
\`\`\`

---

### 4. config/tts.py (TTS Voice)
File: `/Users/swapnil/Documents/Projects/adaptive-user-response-assistant/config/tts.py`

**What it controls:**
- SUPERTONIC_SPEED: 0.5=slow, 1.0=normal, 1.5=fast
- SUPERTONIC_STEPS: 50=fast/lower quality, 150=slow/best quality
- SUPERTONIC_VOICE: which voice to use

**To make TTS slower & clearer:**
\`\`\`python
SUPERTONIC_SPEED = 0.7    # was 1.0
SUPERTONIC_STEPS = 120    # was 100
\`\`\`

**To make TTS faster:**
\`\`\`python
SUPERTONIC_SPEED = 1.3    # was 1.0
SUPERTONIC_STEPS = 50     # was 100
\`\`\`

---

## All Files & What They Do

### Entry Point
- **main.py** — Determines which mode to run
  - Imports MODE from config/features.py
  - Calls _run_stt_only(), _run_voice_chat(), _run_full(), etc.

### Configuration (Edit These To Tune)
- **config/features.py** — MODE selection
- **config/vad.py** — Speech detection tuning (CRITICAL!)
- **config/llm.py** — LLM settings (temperature, context size)
- **config/tts.py** — TTS settings (speed, quality, voice)
- **config/whisper.py** — Whisper STT settings
- **config/server.py** — Server settings

### Microphone & Audio (Understand These)
- **audio/io/mic.py** — Opens mic at 44.1kHz
- **audio/transform/resample.py** — Converts 44.1kHz → 16kHz (MUST NOT REMOVE!)
- **transcription/vad/session.py** — Mic loop with VAD & preroll
- **transcription/vad/processor.py** — Detects speech vs silence
- **transcription/vad/energy.py** — RMS + ZCR algorithm

### Whisper (Speech-to-Text)
- **transcription/stream/buffer.py** — Buffers 16kHz audio
- **transcription/stream/worker.py** — Thread that transcribes periodically
- **transcription/stream/partial.py** — Real-time streaming text
- **transcription/stream/final.py** — Final transcription (when speech ends)
- **transcription/hallucination/confidence.py** — Filters by Whisper confidence
- **transcription/hallucination/repetition.py** — Filters repetitive/music audio

### LLM (Language Model)
- **llm/model/singleton.py** — Load Qwen once
- **llm/inference/stream.py** — Stream tokens
- **llm/history/state.py** — Keep conversation context

### TTS (Text-to-Speech)
- **tts/model/singleton.py** — Load Supertonic once
- **tts/engine/worker.py** — Generate audio from tokens
- **tts/engine/control.py** — interrupt, resume, speak_filler

### Utilities
- **ui/console.py** — Colored terminal output
- **server/logger.py** — Log to file with latency metrics

---

## 6 Operating Modes

Change MODE in config/features.py to switch:

- **stt_only** — Speak → Whisper → Text (test STT)
- **tts_only** — Type → TTS → Speaker (test TTS)
- **text_to_text_chat** — Type → LLM → Type (test LLM)
- **voice_to_text_chat** — Speak → Whisper → LLM → Type
- **full** — Speak → Whisper → LLM → TTS → Speaker (complete voice loop)
- **server** — WebSocket API server

---

## Common Fixes

### Fix 1: Stop Hallucinating "I'm sorry", "Thank you", "Okay"
**File:** config/vad.py
**Changes:**
\`\`\`python
NO_SPEECH_THRESHOLD = 0.98        # Increase from 0.92
LOGPROB_THRESHOLD = 0.0           # Increase from -0.4
COMPRESSION_RATIO_THRESHOLD = 0.8 # Decrease from 1.5
\`\`\`

### Fix 2: Capture First Word (Not Clipped)
**File:** config/vad.py
**Changes:**
\`\`\`python
PREROLL_SECONDS = 0.25  # Increase from 0.15
\`\`\`

### Fix 3: Don't Miss Words from Real Speech
**File:** config/vad.py
**Changes:**
\`\`\`python
ENERGY_THRESHOLD = 0.03   # Decrease from 0.045
MIN_SPEECH_SEC = 0.35     # Decrease from 0.48
\`\`\`

### Fix 4: Stop Music Being Transcribed
**File:** config/vad.py
**Changes:**
\`\`\`python
COMPRESSION_RATIO_THRESHOLD = 0.8  # Decrease from 1.5
NO_SPEECH_THRESHOLD = 0.95         # Increase from 0.92
\`\`\`

### Fix 5: More Creative LLM
**File:** config/llm.py
**Changes:**
\`\`\`python
TEMPERATURE = 1.2  # Increase from 0.7
\`\`\`

### Fix 6: Faster LLM Response
**File:** config/llm.py
**Changes:**
\`\`\`python
N_CTX = 1024  # Decrease from 2048
\`\`\`

### Fix 7: Better TTS Quality
**File:** config/tts.py
**Changes:**
\`\`\`python
SUPERTONIC_STEPS = 120  # Increase from 100
SUPERTONIC_SPEED = 0.7  # Decrease from 1.0
\`\`\`

---

## Logging & Metrics

Each interaction is logged to: `logs/conversation_YYYY-MM-DD_HH-MM-SS.log`

**Format:**
\`\`\`
[HH:MM:SS] #02  YOU:what user said  AI:what AI responded  whisper:1.206s  ft:0.348s  llm:2.514s  e2e:3.742s
\`\`\`

**Metrics:**
- **whisper:X.XXs** — Time for speech-to-text
- **ft:X.XXs** — Time until LLM gives first token
- **llm:X.XXs** — Time for full LLM response
- **e2e:X.XXs** — Total time from speech input to final response

---

## When to Use Each Mode

- **stt_only** — Testing mic quality and Whisper accuracy
- **tts_only** — Testing voice output quality
- **text_to_text_chat** — Testing LLM reasoning without audio
- **voice_to_text_chat** — Voice input, text output (quiet environments)
- **full** — Production mode (full voice assistant)
- **server** — Running as API server

---

## Quick Checklist for Problems

- [ ] Hallucinating on silence? → Increase NO_SPEECH_THRESHOLD in config/vad.py
- [ ] First word clipped? → Increase PREROLL_SECONDS in config/vad.py
- [ ] Missing words? → Decrease ENERGY_THRESHOLD in config/vad.py
- [ ] Music transcribing? → Decrease COMPRESSION_RATIO_THRESHOLD in config/vad.py
- [ ] Boring LLM? → Increase TEMPERATURE in config/llm.py
- [ ] Slow LLM? → Decrease N_CTX in config/llm.py
- [ ] Poor TTS? → Increase SUPERTONIC_STEPS in config/tts.py
- [ ] Slow TTS? → Decrease SUPERTONIC_STEPS in config/tts.py
