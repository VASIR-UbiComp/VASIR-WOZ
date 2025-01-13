import whisper
import pyaudio
import wave


def record_audio(filename, duration, rate=44100, chunk=1024, channels=2):
    # Create an interface to PortAudio
    p = pyaudio.PyAudio()

    # Open a stream with the necessary parameters
    stream = p.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )

    print(f"Recording for {duration} seconds...")

    frames = []

    # Record the audio in chunks
    for _ in range(0, int(rate / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    print(f"Recording finished. Saving to {filename}...")

    # Save the recorded data as a WAV file
    wf = wave.open(filename, "wb")
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b"".join(frames))
    wf.close()

    print(f"File saved as {filename}.")


def speech_to_text(filename):
    model = whisper.load_model("base")
    result = model.transcribe(filename, fp16=False, language="Polish")
    return result["text"]


if __name__ == "__main__":
    record_audio("output.wav", duration=10, channels=1)
    text = speech_to_text("output.wav")
    print(text)
