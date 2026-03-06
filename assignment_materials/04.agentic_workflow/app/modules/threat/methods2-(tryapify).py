# 1. user topic
# 2. generate set queries
# 3. a Search to the web based queries (tavily)
# 3. b Twitter scarepper agent (apify)
# 4. summarize_address_range
# 5. generate report

import json
import logging

from app.utils.openai import oa_client
from app.utils.tavily import tavily_client
from app.modules.threat.schema import QueriesSchema
from app.utils.apify import apify_client


logger = logging.getLogger(__name__)


def generate_queries(topic: str) -> QueriesSchema:
    # keywords: list = ["exploit", "0day", "vulnerability", "privilege escalation", "cve"]
    keywords: list = ["exploit", "vulnerability", "cve"]
    query_list = [f"{topic} {keyword}" for keyword in keywords]
    queries: QueriesSchema = QueriesSchema(queries=query_list)

    logger.info(f"Generate queries : {queries}")

    return queries


def search_threat(query: str) -> list:
    result = tavily_client.search(
        query=query, search_depth="advanced", include_raw_content="markdown"
    )
    articles = []

    for r in result["results"]:
        articles.append(r)

    return articles


def search_threat_twitter(query: str) -> list:
    try:
        run_input = {"searchTerms": [query], "maxTweets": 20}

        run = apify_client.actor(
            "kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest"
        ).call(run_input=run_input)

        tweets = []

        if run is not None:
            for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
                tweets.append(item["text"])

        return tweets
    except Exception as e:
        logger.warning(f"Twitter search failed for query '{query}': {e}")
        return []


def summarize_context(articles: list, tweets: list):
    # lakukan summarize dengan model AI
    response = oa_client.chat.completions.create(
        model="deepseek/deepseek-v3.2",
        messages=[
            {
                "role": "system",
                "content": "Summarize this into informative content, please include data, numbers, and url/source",
            },
            {"role": "user", "content": f"Context: {articles} {tweets}"},
        ],
        extra_body={"reasoning": {"enabled": True}},
    )

    logger.info("Thinking for generate summary ...")

    return response.choices[0].message.content
