{{ config(materialized='ephemeral') }}

-- Read and stage raw JSON data
SELECT
    -- If there's no change to the court status,
    -- often the last_updated_timestamp will be the same.
    -- In other cases, the case will be tagged as "No Information To Display."
    DISTINCT
        court_region,
        strptime(last_updated_timestamp, '%Y-%m-%dT%H:%M:%S') as last_updated_timestamp,
        court_name,
        court_number,
        case_number,
        defendant_name,
        trial_status
FROM read_json_auto('{{ var("daily_court_json_feed") }}/**/*.jsonl')
