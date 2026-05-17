import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from call_function import available_functions, call_function
from prompts import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise Exception("LLM API KEY NOT FOUND")

client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
function_results = []

message = types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=message,
    config=types.GenerateContentConfig(
        tools=[available_functions], system_instruction=system_prompt, temperature=0
    ),
)

if not response.usage_metadata:
    raise Exception("Request Failed!")

function_call_results = [
    call_function(call, args.verbose) for call in response.function_calls
]

for function_call_result in function_call_results:
    if (
        not function_call_result.parts
        or not function_call_result.parts[0].function_response
        or not function_call_result.parts[0].function_response.response
    ):
        raise Exception("Function response is empty!")

    if args.verbose:
        print(f"-> {function_call_result.parts[0].function_response.response}")
    function_results.append(function_call_result.parts[0])


if args.verbose:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


# print each iterable in response.function_call list if it exists
if response.function_calls:
    for item in response.function_calls:
        print(f"Calling function: {item.name}({item.args})")
else:
    print(f"Response:\n{response.text}")
