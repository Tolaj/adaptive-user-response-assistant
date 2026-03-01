"""
Quick Test Script - Verify Voice Features
Tests all voice endpoints without requiring audio recording
"""
import requests
import json
import os
from pathlib import Path
import time

SERVER_URL = "http://localhost:5001"

def test_health():
    """Test server health"""
    print("\n" + "="*60)
    print("🏥 HEALTH CHECK")
    print("="*60)
    
    try:
        response = requests.get(f"{SERVER_URL}/health", timeout=5)
        data = response.json()
        
        print(f"✅ Server Status: {data['status']}")
        print(f"✅ LLM Model: {data['llm_model']}")          # was 'model'
        print(f"✅ LLM Loaded: {data['llm_loaded']}")        # was 'loaded'
        print(f"✅ Whisper Loaded: {data.get('whisper_loaded', 'Not loaded')}")
        print(f"✅ Context Window: {data['context_size']}")   # was 'ctx'
        print(f"✅ GPU Layers: {data['gpu_layers']}")
        # removed 'threads' — not in health response
        
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def test_text_to_speech():
    """Test TTS endpoint"""
    print("\n" + "="*60)
    print("🔊 TEXT-TO-SPEECH TEST")
    print("="*60)
    
    test_text = "Hello! This is a test of the text to speech system."
    print(f"Input: {test_text}")
    
    try:
        response = requests.post(
            f"{SERVER_URL}/v1/audio/speech",
            json={
                "input": test_text,
                "voice": "en",
                "speed": 1.0
            },
            timeout=30
        )
        
        if response.status_code == 200:
            output_file = "test_speech.mp3"
            with open(output_file, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(output_file)
            print(f"✅ TTS Success!")
            print(f"   File: {output_file}")
            print(f"   Size: {file_size} bytes")
            return True
        else:
            print(f"❌ TTS failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ TTS error: {e}")
        return False


def test_chat_completion():
    """Test basic chat (text only)"""
    print("\n" + "="*60)
    print("💬 CHAT COMPLETION TEST")
    print("="*60)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Keep responses brief."},
        {"role": "user", "content": "Say hello in one sentence."}
    ]
    
    try:
        response = requests.post(
            f"{SERVER_URL}/v1/chat/completions",
            json={
                "messages": messages,
                "max_tokens": 50,
                "temperature": 0.7
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            text = data['choices'][0]['message']['content']
            print(f"✅ Chat Success!")
            print(f"   Response: {text}")
            return True
        else:
            print(f"❌ Chat failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return False


def create_test_audio():
    """Create a simple test audio file using synthesis"""
    print("\n" + "="*60)
    print("🎵 CREATING TEST AUDIO")
    print("="*60)
    
    try:
        # Generate a test audio file using TTS
        test_text = "Hello, this is a test message for voice recognition."
        
        response = requests.post(
            f"{SERVER_URL}/v1/audio/speech",
            json={
                "input": test_text,
                "voice": "en"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            test_audio = "test_audio.mp3"
            with open(test_audio, 'wb') as f:
                f.write(response.content)
            print(f"✅ Test audio created: {test_audio}")
            return test_audio
        else:
            print(f"❌ Failed to create test audio")
            return None
            
    except Exception as e:
        print(f"❌ Error creating test audio: {e}")
        return None


def test_transcription(audio_file=None):
    """Test STT endpoint"""
    print("\n" + "="*60)
    print("🎤 SPEECH-TO-TEXT TEST")
    print("="*60)
    
    if not audio_file:
        print("⚠️  No audio file provided, skipping STT test")
        print("   To test: provide a .wav or .mp3 file")
        return False
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    try:
        with open(audio_file, 'rb') as f:
            response = requests.post(
                f"{SERVER_URL}/v1/audio/transcriptions",
                files={'file': (audio_file, f)},
                timeout=60
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ STT Success!")
            print(f"   Transcription: {data['text']}")
            print(f"   Language: {data.get('language', 'unknown')}")
            return True
        else:
            print(f"❌ STT failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ STT error: {e}")
        return False


def test_voice_chat(audio_file=None):
    """Test complete voice pipeline"""
    print("\n" + "="*60)
    print("🎙️ VOICE CHAT PIPELINE TEST")
    print("="*60)
    
    if not audio_file:
        # Try to create test audio first
        audio_file = create_test_audio()
        if not audio_file:
            print("⚠️  Cannot test voice chat without audio file")
            return False
    
    if not os.path.exists(audio_file):
        print(f"❌ Audio file not found: {audio_file}")
        return False
    
    try:
        with open(audio_file, 'rb') as f:
            response = requests.post(
                f"{SERVER_URL}/v1/voice/chat",
                files={'file': (audio_file, f)},
                data={'voice': 'en'},
                timeout=120
            )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Voice Chat Success!")
            print(f"\n   👤 User: {data['user_text']}")
            print(f"   🤖 Assistant: {data['response_text']}")
            print(f"\n   Audio URL: {data['audio_url']}")
            
            # Try to download response audio
            audio_url = f"{SERVER_URL}{data['audio_url']}"
            audio_response = requests.get(audio_url)
            if audio_response.status_code == 200:
                response_file = "test_response.mp3"
                with open(response_file, 'wb') as f:
                    f.write(audio_response.content)
                print(f"   📥 Response audio saved: {response_file}")
            
            return True
        else:
            print(f"❌ Voice chat failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Voice chat error: {e}")
        return False


def main():
    print("""
╔═══════════════════════════════════════════════════════════╗
║              🧪 VOICE SERVER TEST SUITE                   ║
║          Verify all voice features are working            ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    results = {
        "health": False,
        "chat": False,
        "tts": False,
        "stt": False,
        "voice_chat": False
    }
    
    # Run tests
    results["health"] = test_health()
    
    if not results["health"]:
        print("\n❌ Server not responding. Make sure server is running:")
        print("   python voice_server.py")
        return
    
    time.sleep(1)
    results["chat"] = test_chat_completion()
    
    time.sleep(1)
    results["tts"] = test_text_to_speech()
    
    # Only test STT and voice chat if you have audio files
    audio_file = "test_audio.mp3" if os.path.exists("test_audio.mp3") else None
    
    if audio_file:
        time.sleep(1)
        results["stt"] = test_transcription(audio_file)
        
        time.sleep(1)
        results["voice_chat"] = test_voice_chat(audio_file)
    else:
        print("\n⚠️  Skipping STT/Voice Chat tests (no audio file)")
        print("   To test these, provide a .wav or .mp3 file")
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:12} {test.upper()}")
    
    total = sum(results.values())
    print(f"\n{total}/{len(results)} tests passed")
    
    if total == len(results):
        print("\n🎉 All tests passed! Voice features are working!")
    elif results["health"] and results["chat"] and results["tts"]:
        print("\n✅ Core features working. STT/Voice requires audio file.")
    else:
        print("\n⚠️  Some tests failed. Check server logs.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()