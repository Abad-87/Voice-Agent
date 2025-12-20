from faster_whisper import WhisperModel

SAMPLE_RATE = 16000

# CPU + low RAM optimized
model = WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8"
)

def record_audio(duration=5, filename="temp.wav"):
    import sounddevice as sd
    import numpy as np
    import wavio
    print("🎤 Recording...")
    audio = sd.rec(
        int(duration * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype="int16"
    )
    sd.wait()
    wavio.write(filename, audio, SAMPLE_RATE, sampwidth=2)
    print("✅ Recording finished")
    return filename

# Used by FastAPI (audio file upload)
def speech_to_text(audio_path: str) -> str:
    segments, _ = model.transcribe(audio_path)
    return " ".join(segment.text for segment in segments)

# Used by real-time mic mode
def speech_to_text_from_mic(duration=10) -> str:
    audio_path = record_audio(duration)
    return speech_to_text(audio_path)
