from __future__ import annotations

from typing import TYPE_CHECKING
import logging


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    import dlt


def log_pipeline_state(pipeline: dlt.Pipeline) -> None:
    state = pipeline.state
    previous_extraction = state.get("_local", {})
    previous_extraction_date = previous_extraction.get("last_extraction_date")

    state_breakdown = (
        f"--- Pipeline State ---\n"
        f"\t- Pipeline Dataset Name: {state.get('dataset_name', 'N/A')}\n"
        f"\t- Pipeline Name: {state.get('pipeline_name', 'N/A')}\n"
        f"\t- Default Schema Name: {state.get('default_schema_name', 'N/A')}\n"
        f"\t- Destination Type: {state.get('destination_type', 'N/A')}\n"
        f"\t- Destination: {state.get('destination_name', 'N/A')}\n"
        f"\t- Version Hash: {state.get('_version_hash', 'N/A')}\n"
    )
    logger.info(state_breakdown)

    if previous_extraction_date:
        previous_extr = (
            f"--- Previous Extraction ---\n"
            f"\t- Extraction Date: {previous_extraction_date.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
            f"\t- Extraction Hash: {previous_extraction.get('last_extraction_hash', 'N/A')}\n"
        )
        logger.info(previous_extr)


def get_pipeline_job_metrics(pipeline: dlt.Pipeline) -> None:
    trace = pipeline.last_trace

    for load_id in trace.last_load_info.metrics:
        for table in trace.last_load_info.metrics[load_id][0]["job_metrics"]:
            logger.info(trace.last_load_info.metrics[load_id][0]["job_metrics"][table])


def log_pipeline_execution_times(pipeline: dlt.Pipeline) -> None:
    end_time, start_time = (
        pipeline.last_trace.finished_at,
        pipeline.last_trace.started_at,
    )
    total_time = end_time - start_time

    total_seconds = int(total_time.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    execution_details = (
        f"--- Pipeline Execution Details ---\n"
        f"\t- Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        f"\t- End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        f"\t- Total Execution Time: {hours}h {minutes}m {seconds}s\n"
    )
    logger.info(execution_details)
