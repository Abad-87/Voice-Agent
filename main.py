from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import shutil
import requests

from stt import speech_to_text
from tts import text_to_speech
from auth import verify_key

app = FastAPI(title="Local Voice AI")

OLLAMA_URL = "http://localhost:11434/api/generate"


@app.post("/voice-chat")
def voice_chat(
    x_api_key: str = Header(...),
    audio_file: UploadFile = File(...)
):
    # 🔐 API key check
    if not verify_key(x_api_key):
        raise HTTPException(status_code=403, detail="Invalid API key")

    # 💾 Save uploaded audio
    audio_path = f"temp_{audio_file.filename}"
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(audio_file.file, f)

    # 🎤 Speech → Text
    user_text = speech_to_text(audio_path)

    # 🤖 Text → LLM
    response = requests.post(
    OLLAMA_URL,
    json={
        "model": "phi",
        "prompt": f"""
You are a helpful and responsible AI assistant.

Health rules:
- You may give general health information and precautions
- You may give home-care and lifestyle advice
- Do NOT diagnose diseases
- Always advise consulting a doctor if symptoms persist or worsen

User: {user_text}
""",
        "stream": False
    },
    timeout=120
)


    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="LLM failed")

    ai_reply = response.json()["response"]

    # 🔊 Text → Speech (THIS is where it belongs)
    text_to_speech(ai_reply)

    return {
        "you_said": user_text,
        "ai_reply": ai_reply
    }
