import sounddevice as sd
import numpy as np
import wave
import requests
from faster_whisper import WhisperModel
from tts import text_to_speech as speak

# ---------------- CONFIG ----------------
SAMPLE_RATE = 16000
CHANNELS = 1
SILENCE_THRESHOLD = 500
SILENCE_DURATION = 5
MAX_RECORD_TIME = 10
OLLAMA_URL = "http://localhost:11434/api/generate"

model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

def record_until_silence(filename="input.wav"):
    print("\n🎤 Listening... Speak now")

    frames = []
    silence_time = 0
    block_duration = 0.1

    with sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=CHANNELS,
        dtype="int16"
    ) as stream:
        elapsed = 0

        while True:
            block, _ = stream.read(int(SAMPLE_RATE * block_duration))
            frames.append(block)

            rms = np.sqrt(np.mean(block.astype(np.float32) ** 2))

            if rms < SILENCE_THRESHOLD:
                silence_time += block_duration
            else:
                silence_time = 0

            elapsed += block_duration

            if silence_time >= SILENCE_DURATION or elapsed >= MAX_RECORD_TIME:
                break

    audio = np.concatenate(frames)

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio.tobytes())

    print("🛑 Speech ended")
    return filename

def transcribe(audio):
    segments, _ = model.transcribe(audio)
    text = " ".join(s.text.strip() for s in segments)
    return text.strip()

def ask_phi(text):
    r = requests.post(
        OLLAMA_URL,
        json={
            "model": "phi",
            "prompt": text,
            "stream": False
        },
        timeout=180
    )
    return r.json().get("response", "").strip()

# ---------------- MAIN LOOP ----------------
print("🤖 Voice AI READY (Ctrl+C to stop)")

while True:
    try:
        audio = record_until_silence()
        user_text = transcribe(audio)

        if not user_text:
            print("⚠️ Didn't catch that. Speak again.")
            continue

        print(f"🧑 You: {user_text}")

        ai_reply = ask_phi(user_text)

        if not ai_reply:
            ai_reply = "Sorry, I didn't understand that."

        print(f"🤖 AI: {ai_reply}")

        # 🔊 GUARANTEED SPEAK
        speak(ai_reply)

    except KeyboardInterrupt:
        print("\n👋 Stopped")
        break
    except Exception as e:
        print("❌ Error:", e)
