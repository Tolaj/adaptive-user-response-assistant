# Use the TTS audio as input for voice chat
import requests

with open('test_speech.mp3', 'rb') as f:
    response = requests.post(
        'http://localhost:5001/v1/voice/chat',
        files={'file': ('test.mp3', f, 'audio/mpeg')},
        data={'voice': 'en'}
    )
    print(response.json())
