from flask import Flask, render_template, request, jsonify, send_from_directory
from speech_to_text import speech_to_text
from text_to_speech import text_to_speech
from assistant import *
from config import TTS_URL, OUTPUT_PATH
import os

app = Flask(__name__)

assistant_client = None
assistant_id = None
thread = None
initialized = False


@app.before_request
def initialize_assistant():
    global assistant_client, assistant_id, thread, initialized
    if not initialized:
        print("Initializing assistant...")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        assistant_client = openai
        assistant_id = create_assistant(assistant_client)

        # Create a single thread during initialization
        thread = assistant_client.beta.threads.create()
        print(f"Thread created: {thread.id}")
        initialized = True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/process_audio", methods=["POST"])
def process_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    audio_file = request.files["file"]
    audio_file.save("uploaded_audio.wav")

    text = speech_to_text("uploaded_audio.wav")
    return jsonify({"text": text})


@app.route("/send_message", methods=["POST"])
def send_message():
    global thread
    data = request.json
    if not data or "text" not in data or "emotion" not in data:
        return jsonify({"error": "Invalid request"}), 400

    text = data["text"]
    emotion = data["emotion"]
    user_input = f"{text} emotion = {emotion}"

    try:
        # Run the assistant with the existing thread
        run, thread_obj = create_message_and_run(
            assistant_client, assistant_id=assistant_id, query=user_input, thread=thread
        )

        while True:
            run = assistant_client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )
            if run.status == "completed":
                messages = assistant_client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                latest_message = messages.data[0]
                assistant_response = latest_message.content[0].text.value

                # Convert response to speech
                audio_path = text_to_speech(assistant_response, TTS_URL)

                if audio_path:
                    return jsonify(
                        {
                            "response": assistant_response,
                            "audio_path": os.path.basename(audio_path),
                        }
                    )
                else:
                    return jsonify(
                        {"error": "Failed to generate audio from assistant response."}
                    )
            elif run.status == "failed":
                print_error_details(run)
                return jsonify({"error": "Assistant failed to process the request."})
            elif run.status == "requires_action":
                function_name, arguments, function_id = get_function_details(run)
                function_response = execute_function_call(function_name, arguments)
                run = submit_tool_outputs(
                    assistant_client, run, thread_obj, function_id, function_response
                )
                continue
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/audio/<filename>")
def serve_audio(filename):
    file_path = os.path.join(os.path.dirname(OUTPUT_PATH), filename)

    try:
        # Serve the file
        response = send_from_directory(os.path.dirname(OUTPUT_PATH), filename)

        # Add a callback to delete the file after the response is sent
        @response.call_on_close
        def cleanup():
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted audio file: {file_path}")

        return response
    except Exception as e:
        print(f"Error serving audio file: {e}")
        return jsonify({"error": "Failed to serve audio file."}), 500


if __name__ == "__main__":
    app.run(debug=True)
