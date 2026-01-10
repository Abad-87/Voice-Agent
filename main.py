from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.responses import Response
import shutil
import requests
import os

from stt import speech_to_text
from tts import text_to_speech
from auth import verify_key

app = FastAPI(title="Voice AI")

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/voice-chat")
async def voice_chat(
    x_api_key: str = Header(...),
    audio_file: UploadFile = File(...)
):
    # 🔐 API key check
    if not verify_key(x_api_key):
        raise HTTPException(status_code=403, detail="Invalid API key")

    # 💾 Save uploaded audio
    audio_path = f"/tmp/{audio_file.filename}"
    with open(audio_path, "wb") as f:
        shutil.copyfileobj(audio_file.file, f)

    # 🎤 Speech → Text
    user_text = speech_to_text(audio_path)

    if not user_text:
        raise HTTPException(status_code=400, detail="Could not transcribe audio")

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

    # 🔊 Text → Speech (generate audio bytes)
    audio_bytes = await text_to_speech(ai_reply)

    if not audio_bytes:
        raise HTTPException(status_code=500, detail="TTS failed")

    # 🎧 Return AUDIO, not JSON
    return Response(
        content=audio_bytes,
        media_type="audio/wav"
    )
