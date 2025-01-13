import pyaudio
import numpy as np
import wave
import speech_recognition as sr
import whisper

# options = {'language': 'pl'} jakby sie chcialo whispera w wykrywaniu keyword


def is_keyword_detected(keyword):
    is_keyword = False
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    options = {"language": "pl"}
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for the keyword...")
        while True:
            audio = recognizer.listen(source)
            try:
                transcript = recognizer.recognize_google(
                    audio
                )  # recognize_whisper(audio, **options) #recognizer_google(audio)
                print("You said:", transcript)
                if keyword.lower() in transcript.lower():
                    print("Keyword detected!")
                    is_keyword = True
                    return is_keyword
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")


def record_audio_with_silence_detection(
    output_filename="output.wav", silence_threshold=150, silence_duration=3
):
    # Audio recording parameters
    FORMAT = pyaudio.paInt16  # 16-bit resolution
    CHANNELS = 1  # Mono channel
    RATE = 44100  # 44.1kHz sampling rate
    CHUNK = 1024  # 1024 samples per frame

    # Initialize pyaudio
    audio = pyaudio.PyAudio()

    # Start recording
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    print("Recording...")

    frames = []
    silence_buffer = []  # Buffer to hold recent volume values
    max_silent_chunks = int(silence_duration * RATE / CHUNK)

    def calculate_rms(audio_data):
        """Calculate the root mean square (RMS) of the audio data."""
        return np.sqrt(np.mean(np.square(audio_data.astype(np.float64))))

    try:
        while True:
            data = stream.read(CHUNK)
            frames.append(data)

            # Convert the audio data to numpy array
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Compute the volume (root mean square)
            volume = calculate_rms(audio_data)

            # Debug print for volume levels
            print(f"Volume: {volume}")

            # Add the current volume to the silence buffer
            silence_buffer.append(volume)

            # Maintain the buffer size to max_silent_chunks
            if len(silence_buffer) > max_silent_chunks:
                silence_buffer.pop(0)

            # Check if all recent volumes in the buffer are below the silence threshold
            if len(silence_buffer) == max_silent_chunks and all(
                vol < silence_threshold for vol in silence_buffer
            ):
                print("Silence detected. Stopping recording.")
                break
    except Exception as e:
        print(f"An error occurred: {e}")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(output_filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    print(f"Recording saved as {output_filename}")


def speech_to_text(filename):
    # options = {'language': 'pl'}
    model = whisper.load_model("base")
    result = model.transcribe(filename, fp16=False, language="Polish")  # **options)
    return result["text"]


if __name__ == "__main__":
    # Example usage:
    # keyword = 'start'
    # if (is_keyword_detected(keyword)):
    record_audio_with_silence_detection("output.wav", 150, 3)
    text = speech_to_text("output.wav")
    print(text)
