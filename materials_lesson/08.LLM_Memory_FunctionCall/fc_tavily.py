import json
from openai import OpenAI
import os
from dotenv import load_dotenv
from tavily import TavilyClient


load_dotenv()

client_oa = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


# buat function tool search ke internet
def search(query: str):
    # function memanggil tavily untuk search ke internet
    result = tavily_client.search(
        query, include_answer="basic", search_depth="advanced"
    )
    print(result)
    return json.dumps(result)


# function tool harus didefinisikan
search_fd = {
    "type": "function",
    "function": {
        "name": "search",
        "description": "Search information in the internet based on query input",  # ini bagian penting agar di kenali model LLM
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query to search in the internet",
                }
            },
            "required": ["query"],
        },
    },
}

messages_state = [
    {"role": "system", "content": "You are elpful assistant"},
    {
        "role": "user",
        "content": "Cari informasi tren golang dan javascript sebagai backend pemograman?",
    },
]

completion = client_oa.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=messages_state,  # type:ignore
    # register tool
    tools=[search_fd],  # type:ignore
)

result = completion.choices[0].message

tool_call = result.tool_calls  # tampilkan dengan method tool_calls
if tool_call is not None:
    tool_call_id = tool_call[0].id
    tool_name = tool_call[0].function.name
    tool_args = json.loads(tool_call[0].function.arguments)
    query = tool_args.get("query")

    messages_state.append(result)

    if tool_name == "search":
        result = search(query=query)

        messages_state.append(
            {"role": "tool", "tool_call_id": tool_call_id, "content": result}
        )

        final_completion = client_oa.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages_state,  # type :ignore
        )

        final_result = final_completion.choices[0].message.content
        print("Assistant:", final_result)
else:
    print(result.content)
