def text_to_speech(text: str):
    try:
        from piper import PiperVoice
        import sounddevice as sd
        voice = PiperVoice.load("en_US-lessac-medium.onnx")
        audio, sample_rate = voice.synthesize(text)

        sd.play(audio, sample_rate)
        sd.wait()

    except Exception as e:
        print("❌ TTS Error:", e)
