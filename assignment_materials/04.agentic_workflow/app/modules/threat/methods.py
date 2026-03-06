# 1. user topic
# 2. generate set queries
# 3. a Search to the web based queries (tavily)
# 4. summarize_address_range
# 5. generate report

import json

from app.utils.openai import oa_client
from app.utils.tavily import tavily_client
from app.modules.threat.schema import QueriesSchema
from app.modules.threat.prompt import REPORT_SYSTEM_PROMPT


def generate_queries(topic: str) -> QueriesSchema:
    # keywords: list = ["exploit", "0day", "vulnerability", "privilege escalation", "cve"]
    keywords: list = ["exploit", "vulnerability", "cve"]
    query_list = [f"{topic} {keyword}" for keyword in keywords]
    queries: QueriesSchema = QueriesSchema(queries=query_list)

    return queries


def search_threat(query: str) -> str:

    result = tavily_client.search(
        query=query, search_depth="advanced", include_raw_content="markdown"
    )

    # lakukan summarize dengan model AI
    response = oa_client.chat.completions.create(
        model="deepseek/deepseek-v3.2",
        messages=[
            {
                "role": "system",
                "content": "Summarize this into informative content, please include data, numbers, and url/source",
            },
            {"role": "user", "content": f"Search result: {json.dumps(result)}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
    )

    return response.choices[0].message.content  # type: ignore


def generate_report(topic: str, research_context: str):

    # lakukan generate report dengan bantuan AI
    response = oa_client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[
            {
                "role": "system",
                "content": REPORT_SYSTEM_PROMPT.format(
                    research_context=research_context
                ),
            },
            {"role": "user", "content": f"Topic: {topic}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
    )

    return response.choices[0].message.content
