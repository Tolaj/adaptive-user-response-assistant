"""
Pre-download Whisper models to avoid connection issues during runtime
Run this BEFORE starting the server
"""
import whisper
import os

print("="*60)
print("WHISPER MODEL DOWNLOADER")
print("="*60)

models = {
    "tiny": "~75MB - Fastest, lowest accuracy",
    "base": "~142MB - Good balance (RECOMMENDED)",
    "small": "~466MB - Better accuracy",
    "medium": "~1.5GB - High accuracy",
    "large": "~2.9GB - Best accuracy"
}

print("\nAvailable models:")
for name, desc in models.items():
    print(f"  - {name:8} {desc}")

print("\nWhich model do you want to download?")
print("Recommendation: Start with 'base' (press Enter for base)")
choice = input("Enter model name (tiny/base/small/medium/large) [base]: ").strip().lower()

if not choice:
    choice = "base"

if choice not in models:
    print(f"❌ Invalid choice. Using 'base'")
    choice = "base"

print(f"\n📥 Downloading {choice} model...")
print("This may take a few minutes depending on your connection...")

try:
    model = whisper.load_model(choice)
    print(f"\n✅ SUCCESS! {choice} model downloaded and loaded")
    print(f"Model location: {os.path.expanduser('~/.cache/whisper')}")
    print(f"\nYou can now start the server with:")
    print(f"  export WHISPER_MODEL={choice}  # Linux/Mac")
    print(f"  $env:WHISPER_MODEL='{choice}'  # PowerShell")
    print(f"  python voice_server.py")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    print("\nIf download fails, try:")
    print("1. Check your internet connection")
    print("2. Try a smaller model (tiny or base)")
    print("3. Download manually from: https://openaipublic.azureedge.net/main/whisper/models/")