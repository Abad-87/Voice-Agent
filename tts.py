from piper import PiperVoice

voice = PiperVoice.load("en_US-lessac-medium.onnx")

def text_to_speech(text: str):
    try:
        import sounddevice as sd
        audio, sample_rate = voice.synthesize(text)

        sd.play(audio, sample_rate)
        sd.wait()

    except Exception as e:
        print("❌ TTS Error:", e)
