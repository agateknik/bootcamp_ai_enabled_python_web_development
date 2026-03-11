import os
import datetime
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), base_url="https://openrouter.ai/api/v1"
)

today_date = datetime.datetime.now()

summarized_result = ""

SYSTEM_PROMPT = f"""
    You are a helpful assistant.
    as additional context:
    
    Today's date is {today_date} 
    
    <document_context>
        Restoran ayam kampung BOPOKUH adalah restoran dengan menu khas menu olahan ayam dari berbagai resep Nusantara.
        Restoran ini berlokasi di Matraman, Jakarta Timur.
        Menu favorit nya:
        - Ayam serundeng gacoannya pitung.
        - Opor ayam semar mesem.
        - Ayam bakar bali
    </document_context>
    
    <previous_conversation_summary>
    ....{summarized_result}
    </previous_conversation_summary>
"""

SUMMARIZE_THRESHOLD = 10
SLIDING_WINDOW_SIZE = 3

message_state = []


def summarize_conversation(messages: list[dict[str, Any]]) -> str:
    summarize_prompt = [
        {
            "role": "system",
            "content": "You are a helpful assistant that summarizes conversation history.",
        },
        {
            "role": "user",
            "content": f"Summarize the following conversation concisely, keeping only key information:\n\n{messages}",
        },
    ]

    chat = client.chat.completions.create(
        model="google/gemini-2.0-flash-lite-001",
        messages=summarize_prompt,  # type: ignore[arg-type]
    )

    return chat.choices[0].message.content or ""


def build_context_messages(summarized_history, recent_messages):
    context_messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if summarized_history:
        context_messages.append(
            {
                "role": "system",
                "content": f"Summary of previous conversation:\n{summarized_history}",
            }
        )

    context_messages.extend(recent_messages)

    return context_messages


message_state.append({"role": "system", "content": SYSTEM_PROMPT})

while True:
    user_input: str = input("You: (ketik 'exit' untuk keluar)\n")
    if user_input == "exit":
        break

    message_state.append({"role": "user", "content": user_input})

    conversation_only = [m for m in message_state if m["role"] in ["user", "assistant"]]

    if len(conversation_only) > SUMMARIZE_THRESHOLD:
        messages_to_summarize = conversation_only[:-SLIDING_WINDOW_SIZE]
        summarized_history = summarize_conversation(messages_to_summarize)

        recent_messages = conversation_only[-SLIDING_WINDOW_SIZE:]

        final_messages = build_context_messages(summarized_history, recent_messages)
    else:
        summarized_history = ""
        recent_messages = (
            message_state[-SUMMARIZE_THRESHOLD:]
            if len(message_state) > SUMMARIZE_THRESHOLD
            else message_state
        )
        final_messages = build_context_messages(summarized_history, recent_messages)

    chat = client.chat.completions.create(
        model="google/gemini-2.0-flash-lite-001",
        messages=final_messages,  # type: ignore
    )

    result = chat.choices[0].message.content or ""

    print(f"Assistant: {result}")
    message_state.append({"role": "assistant", "content": result})
