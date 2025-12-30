import os
from typing import Optional
import sounddevice as sd
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
USE_ELEVENLABS = bool(ELEVENLABS_API_KEY)

# Check availability of TTS libraries
try:
    from elevenlabs import generate, play, set_api_key
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False
    print("ElevenLabs not available - using Piper fallback")
    generate = None
    play = None
    set_api_key = None

try:
    from piper import PiperVoice
    PIPER_AVAILABLE = True
except ImportError:
    PIPER_AVAILABLE = False
    print("Piper TTS not available - TTS will be limited")
    PiperVoice = None

if USE_ELEVENLABS and ELEVENLABS_AVAILABLE:
    set_api_key(ELEVENLABS_API_KEY)

# Fallback Piper voice
piper_voice = None

def init_piper():
    global piper_voice
    if piper_voice is None:
        piper_voice = PiperVoice.load("en_US-lessac-medium.onnx")

async def text_to_speech_elevenlabs(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", language: str = "en") -> Optional[bytes]:
    """Use ElevenLabs for high-quality, empathetic TTS"""
    if not ELEVENLABS_AVAILABLE:
        return None

    try:
        audio = generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )
        return audio
    except Exception as e:
        print(f"ElevenLabs error: {e}")
        return None

def text_to_speech_piper(text: str) -> tuple:
    """Fallback to Piper TTS"""
    if not PIPER_AVAILABLE:
        return None, None

    try:
        init_piper()
        audio, sample_rate = piper_voice.synthesize(text)
        return audio, sample_rate
    except Exception as e:
        print(f"Piper TTS error: {e}")
        return None, None

async def text_to_speech(text: str, voice_id: str = "21m00Tcm4TlvDq8ikWAM", language: str = "en", play_audio: bool = True) -> Optional[bytes]:
    """Main TTS function with ElevenLabs priority"""
    if USE_ELEVENLABS and ELEVENLABS_AVAILABLE:
        audio = await text_to_speech_elevenlabs(text, voice_id, language)
        if audio and play_audio and ELEVENLABS_AVAILABLE:
            play(audio)
        return audio

    # Fallback to Piper
    audio, sample_rate = text_to_speech_piper(text)
    if audio and play_audio and PIPER_AVAILABLE:
        sd.play(audio, sample_rate)
        sd.wait()
    return audio

# Synchronous version for backward compatibility
def speak(text: str):
    """Synchronous TTS function"""
    try:
        import asyncio
        asyncio.run(text_to_speech(text, play_audio=False))
    except Exception as e:
        print(f"TTS Error: {e}")
        # Mock response for testing
        return f"[TTS: {text}]"
