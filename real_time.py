import requests
from stt import speech_to_text_from_mic
from tts import speak

OLLAMA_URL = "http://localhost:11434/api/generate"

print("🎯 Real-time Voice AI started (Ctrl+C to stop)")

while True:
    try:
        user_text = speech_to_text_from_mic(duration=4)
        print("You:", user_text)

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "phi",
                "prompt": user_text,
                "stream": False
            },
            timeout=60
        )

        ai_reply = response.json()["response"]
        print("AI:", ai_reply)

        speak(ai_reply)

    except KeyboardInterrupt:
        print("\n🛑 Stopped")
        break
