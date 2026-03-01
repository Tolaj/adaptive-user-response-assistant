"""
Real-Time Voice Chat Client
Press SPACE to talk, release to get AI response
"""
import requests
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
import time
import threading
import sys
import pygame
from pathlib import Path
from io import BytesIO

SERVER_URL = "http://localhost:5001"
SAMPLE_RATE = 16000
CHANNELS = 1

# ═══════════════════════════════════════════════════════════════
# AUDIO RECORDING
# ═══════════════════════════════════════════════════════════════

recording = False
audio_frames = []

def audio_callback(indata, frames, time_info, status):
    if recording:
        audio_frames.append(indata.copy())

def start_recording():
    global recording, audio_frames
    audio_frames = []
    recording = True

def stop_recording():
    global recording
    recording = False
    if not audio_frames:
        return None
    audio_data = np.concatenate(audio_frames, axis=0)
    return audio_data

# ═══════════════════════════════════════════════════════════════
# SERVER COMMUNICATION
# ═══════════════════════════════════════════════════════════════

def send_voice(audio_data):
    """Save audio and send to server"""
    # Save as WAV to temp file
    tmp_path = os.path.join(tempfile.gettempdir(), f"voice_{int(time.time())}.wav")
    sf.write(tmp_path, audio_data, SAMPLE_RATE)

    try:
        with open(tmp_path, 'rb') as f:
            response = requests.post(
                f"{SERVER_URL}/v1/voice/chat",
                files={'file': ('audio.wav', f, 'audio/wav')},
                data={'voice': 'en'},
                timeout=60
            )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"\n❌ Server error: {response.text}")
            return None
    except Exception as e:
        print(f"\n❌ Request failed: {e}")
        return None
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass

def play_response(audio_url):
    """Download and play the audio response"""
    try:
        response = requests.get(f"{SERVER_URL}{audio_url}", timeout=10)
        if response.status_code == 200:
            tmp_path = os.path.join(tempfile.gettempdir(), f"response_{int(time.time())}.mp3")

            with open(tmp_path, 'wb') as f:
                f.write(response.content)
            
            pygame.mixer.music.load(tmp_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
    except Exception as e:
        print(f"\n❌ Playback failed: {e}")

# ═══════════════════════════════════════════════════════════════
# KEYBOARD DETECTION (cross-platform)
# ═══════════════════════════════════════════════════════════════

def get_key_press():
    """Detect key press - works on Windows"""
    try:
        import msvcrt
        return msvcrt.kbhit(), msvcrt.getch() if msvcrt.kbhit() else None
    except ImportError:
        return False, None

# ═══════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════

def check_server():
    try:
        r = requests.get(f"{SERVER_URL}/health", timeout=3)
        data = r.json()
        return data.get('llm_loaded', False)
    except:
        return False

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║            🎙️  REAL-TIME VOICE CHAT                         ║
║            Talk to your Local AI                            ║
╚══════════════════════════════════════════════════════════════╝

  Controls:
    ENTER  → Start / Stop recording
    Q      → Quit

""")

def main():
    print_banner()

    # Check server
    print("🔌 Connecting to server...", end=" ")
    if not check_server():
        print("❌ FAILED")
        print(f"   Make sure server is running: python voice_server.py")
        return
    print("✅ Connected!\n")

    # Init pygame audio
    pygame.mixer.init()

    # Start audio stream (always open, only records when flag is set)
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype='float32',
        callback=audio_callback
    )
    stream.start()

    print("─" * 60)
    print("  Press ENTER to start talking, ENTER again to stop")
    print("─" * 60 + "\n")

    conversation = []
    is_recording = False

    try:
        import msvcrt

        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()

                # Q to quit
                if key in (b'q', b'Q'):
                    print("\n👋 Goodbye!")
                    break

                # ENTER to toggle recording
                elif key == b'\r':
                    if not is_recording:
                        # Start recording
                        is_recording = True
                        start_recording()
                        print("🔴 Recording... (press ENTER to stop)", end="\r")
                    else:
                        # Stop and process
                        is_recording = False
                        audio_data = stop_recording()

                        if audio_data is None or len(audio_data) < SAMPLE_RATE * 0.5:
                            print("⚠️  Too short, try again                    ")
                            continue

                        duration = len(audio_data) / SAMPLE_RATE
                        print(f"⏹️  Recorded {duration:.1f}s — Processing...       ")

                        # Send to server
                        print("🤖 Thinking...", end="\r")
                        result = send_voice(audio_data)

                        if result:
                            user_text = result.get('user_text', '(unclear)')
                            response_text = result.get('response_text', '')
                            audio_url = result.get('audio_url', '')

                            print(f"\n{'─'*60}")
                            print(f"  👤 You: {user_text}")
                            print(f"  🤖 AI:  {response_text}")
                            print(f"{'─'*60}\n")

                            # Play audio response
                            if audio_url:
                                print("🔊 Playing response...")
                                play_response(audio_url)

                            print("  Press ENTER to talk again, Q to quit\n")

            time.sleep(0.05)

    except KeyboardInterrupt:
        print("\n👋 Interrupted. Goodbye!")
    finally:
        stream.stop()
        stream.close()
        pygame.mixer.quit()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()       