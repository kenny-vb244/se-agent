import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

MODEL = "openai/gpt-oss-120b"


# --- The tool our agent can call ---
def calculate_average(scores):
    """Return the average of a list of numeric scores, rounded to one decimal."""
    return round(sum(scores) / len(scores), 1)


# --- Describe that tool to the model, in the format it expects ---
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_average",
            "description": "Calculate the average of a list of numeric scores.",
            "parameters": {
                "type": "object",
                "properties": {
                    "scores": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "The list of numeric scores to average.",
                    }
                },
                "required": ["scores"],
            },
        },
    }
]

# So we can map a tool name back to the real Python function that runs it
available_functions = {
    "calculate_average": calculate_average,
}

def run_agent(user_prompt):
    messages = [
        {"role": "system", "content": "You are a helpful assistant. Use tools when they help you answer accurately."},
        {"role": "user", "content": user_prompt},
    ]

    # Step 1: send the prompt, telling the model which tools are available
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # Step 2: did the model decide it needs a tool?
    if not tool_calls:
        # No tool needed -- just return its direct answer
        return response_message.content

    # Step 3: the model wants to call a tool. Add its request to the
    # conversation as a plain dict (not the raw SDK object), then actually
    # run the corresponding Python function.
    messages.append({
        "role": "assistant",
        "content": response_message.content,
        "tool_calls": [
            {
                "id": tc.id,
                "type": "function",
                "function": {"name": tc.function.name, "arguments": tc.function.arguments},
            }
            for tc in tool_calls
        ],
    })

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        function_to_call = available_functions[function_name]

        result = function_to_call(**function_args)

        # Feed the tool's result back into the conversation
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": json.dumps(result),
        })

    # Step 4: send the conversation (now including the tool's result) back
    # to the model so it can produce a final, natural-language answer.
    second_response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return second_response.choices[0].message.content


if __name__ == "__main__":
    print("--- Prompt that should NOT need the tool ---")
    print(run_agent("What is the capital of France?"))

    print("\n--- Prompt that SHOULD trigger the tool ---")
    print(run_agent("What's the average of these exam scores: 80, 90, 70, 100?"))