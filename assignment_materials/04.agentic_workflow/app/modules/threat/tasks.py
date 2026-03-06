from weasyprint import HTML
import markdown
from app.modules.threat.methods import generate_queries, search_threat, generate_report
from app.celery_app import celery_app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_threat(topic: str):
    logger.info("Starting agentic workflow ...")

    research_context = ""
    queries = generate_queries(topic)

    for query in queries.queries:
        logger.info(f"Processing query: {query}")

        result = search_threat(query)
        research_context += f"Query {query} \n\n Result: {result} \n\n\n"
        logger.info(f"Search completed for: {query}")

    report_result = generate_report(topic=topic, research_context=research_context)

    if not report_result:
        raise ValueError("Not report generated")

    logger.info("Starting generated report...")
    # generated report
    result: str = markdown.markdown(text=report_result, output_format="html")
    HTML(string=result).write_pdf("ThreatReport.pdf")


@celery_app.task
def find_threat_task(topic: str):
    find_threat(topic)
