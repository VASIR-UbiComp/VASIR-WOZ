from tools_constants import available_functions
import os
from dotenv import find_dotenv, load_dotenv
import json
import openai
from config import *
from tools_constants import tools

# Load environment variables
load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Ensure API keys are set
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is not set")


def create_message_and_run(client, assistant_id, query, thread=None):
    try:
        if not thread:
            thread = client.beta.threads.create()
            print("Thread created:", thread)

        message = client.beta.threads.messages.create(
            thread_id=thread.id, role="user", content=query
        )
        print("Message created:", message)

        run = client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=assistant_id
        )
        print("Run created:", run)
        return run, thread
    except Exception as e:
        raise Exception(f"Error creating message and run: {e}")


# Function to execute function call
def execute_function_call(function_name, arguments):
    try:
        function = available_functions.get(function_name, None)
        if function:
            arguments = json.loads(arguments)
            print(f"Executing function '{function_name}' with arguments: {arguments}")
            results = function(**arguments)
        else:
            results = f"Error: function {function_name} does not exist"
        return results
    except Exception as e:
        raise Exception(f"Error executing function {function_name}: {e}")


# Function to submit tool outputs
def submit_tool_outputs(client, run, thread, function_id, function_response):
    try:
        print(
            f"Submitting tool outputs for function_id '{function_id}' with response: {function_response}"
        )
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": function_id,
                    "output": str(function_response),
                }
            ],
        )
        return run
    except Exception as e:
        raise Exception(f"Error submitting tool outputs: {e}")


# Function to retrieve function details
def get_function_details(run):
    try:
        print("\nrun.required_action\n", run.required_action)
        function_name = run.required_action.submit_tool_outputs.tool_calls[
            0
        ].function.name
        arguments = run.required_action.submit_tool_outputs.tool_calls[
            0
        ].function.arguments
        function_id = run.required_action.submit_tool_outputs.tool_calls[0].id

        print(f"function_name: {function_name} and arguments: {arguments}")
        return function_name, arguments, function_id
    except Exception as e:
        print(f"Error retrieving function details: {e}")
        return None, None, None


def print_error_details(run):
    print("Run failed.")
    # Print relevant details of the run object instead of the whole object
    print("Run error details:")
    print(f"Run ID: {run.id}")
    print(f"Status: {run.status}")
    if hasattr(run, "error"):
        print(f"Error: {run.error}")
    if hasattr(run, "required_action") and run.required_action:
        print(f"Required action: {run.required_action}")
    # print(f"Assistant: {assistant}")
    print(f"Run Last Error: {run.last_error}")
    # print(f"Thread: {thread}")


def create_assistant(client):
    # Function to create an assistant
    try:
        assistant = client.beta.assistants.create(
            name=ASSISTANT_NAME,
            instructions=ASSISTANT_INSTRUCTIONS,
            model=ASSISTANT_MODEL,
            tools=tools,
        )
        print(f"Assistant created: {assistant}")
        assistant_id = assistant.id
        if not assistant_id:
            raise Exception("Failed to create or retrieve assistant")
        return assistant_id
    except Exception as e:
        raise Exception(f"Error creating assistant: {e}")
