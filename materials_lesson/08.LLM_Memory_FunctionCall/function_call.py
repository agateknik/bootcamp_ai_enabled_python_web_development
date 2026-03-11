import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client_oa = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)


# buat function tool
def get_weather(city: str):
    # function untuk mendapatkan data cuaca
    return f"Cuaca di {city} hari ini cerah dengan suhu 30 derajat Celcius."


# function tool harus didefinisikan
get_weather_fd = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather in a given location",  # ini bagian penting agar di kenali model LLM
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get the weather for",
                }
            },
            "required": ["city"],
        },
    },
}

messages_state = [
    {"role": "system", "content": "You are elpful assistant"},
    {"role": "user", "content": "Bagaimana cuaca di Jakarta , Indonesia hari ini?"},
]

completion = client_oa.chat.completions.create(
    model="google/gemini-2.0-flash-lite-001",
    messages=messages_state,  # type:ignore
    # register tool
    tools=[get_weather_fd],  # type:ignore
)

result = completion.choices[0].message

tool_call = result.tool_calls[0]  # tampilkan dengan method tool_calls
if tool_call:
    tool_call_id = tool_call.id
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)
    city = tool_args.get("city")

    messages_state.append(result)

    if tool_name == "get_weather":
        result = get_weather(city)

        messages_state.append(
            {"role": "tool", "tool_call_id": tool_call_id, "content": result}
        )

        final_completion = client_oa.chat.completions.create(
            model="qwen/qwen3.5-plus-02-15",
            messages=messages_state,  # type :ignore
        )

        final_result = final_completion.choices[0].message.content
        print("Assistant:", final_result)
else:
    print(result.content)
