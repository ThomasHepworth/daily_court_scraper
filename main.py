from __future__ import annotations

import dlt

from src.dlt_resources import court_room_details
from src.pipeline_logging import log_pipeline_execution_times, log_pipeline_state

pipeline = dlt.pipeline(
    pipeline_name="extract_daily_courts",
    pipelines_dir=".dlt/pipelines",
    destination="filesystem",
)

log_pipeline_state(pipeline)

load_info = pipeline.run(
    data=court_room_details(),
    table_name="daily_courts_feed",
    loader_file_format="jsonl",
)

log_pipeline_execution_times(pipeline)
