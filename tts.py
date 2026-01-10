import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
USE_ELEVENLABS = bool(ELEVENLABS_API_KEY)

# ---------------- ELEVENLABS ----------------
try:
    from elevenlabs import generate, set_api_key
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    generate = None
    set_api_key = None

if USE_ELEVENLABS and ELEVENLABS_AVAILABLE:
    set_api_key(ELEVENLABS_API_KEY)

# ---------------- PIPER ----------------
try:
    from piper import PiperVoice
    PIPER_AVAILABLE = True
except ImportError:
    PIPER_AVAILABLE = False
    PiperVoice = None

piper_voice = None

def init_piper():
    global piper_voice
    if piper_voice is None:
        piper_voice = PiperVoice.load("en_US-lessac-medium.onnx")

# ---------------- ELEVENLABS TTS ----------------
async def text_to_speech_elevenlabs(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"
) -> Optional[bytes]:
    if not ELEVENLABS_AVAILABLE:
        return None

    try:
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        return audio  # bytes
    except Exception as e:
        print(f"ElevenLabs error: {e}")
        return None

# ---------------- PIPER TTS ----------------
def text_to_speech_piper(text: str) -> Optional[bytes]:
    if not PIPER_AVAILABLE:
        return None

    try:
        init_piper()
        audio, sample_rate = piper_voice.synthesize(text)

        # Convert to WAV bytes
        import io
        import soundfile as sf

        buffer = io.BytesIO()
        sf.write(buffer, audio, sample_rate, format="WAV")
        buffer.seek(0)
        return buffer.read()

    except Exception as e:
        print(f"Piper TTS error: {e}")
        return None

# ---------------- MAIN TTS ----------------
async def text_to_speech(
    text: str,
    voice_id: str = "21m00Tcm4TlvDq8ikWAM"
) -> Optional[bytes]:

    if USE_ELEVENLABS and ELEVENLABS_AVAILABLE:
        audio = await text_to_speech_elevenlabs(text, voice_id)
        if audio:
            return audio

    return text_to_speech_piper(text)

# ---------------- SYNC WRAPPER ----------------
def speak(text: str) -> Optional[bytes]:
    import asyncio
    return asyncio.run(text_to_speech(text))
