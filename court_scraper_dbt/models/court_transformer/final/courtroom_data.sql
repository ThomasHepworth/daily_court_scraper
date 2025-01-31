{{ config(materialized='table') }}

WITH courtroom_data AS (
    SELECT
        -- Generate a surrogate key for uniquely identifying each court case record
        md5(
            court_region || court_name || court_number || case_number || last_updated_timestamp
        ) AS sk_court_case,

        -- Core court details
        court_region,
        court_name,
        court_number,
        case_number,

        -- Standardise and split defendant names if multiple exist
        CASE
            WHEN defendant_name IS NULL OR defendant_name = ''
            THEN NULL
            ELSE string_split(upper(defendant_name), ';')
        END AS defendant_names,

        -- Standardise timestamp format and extract the weekday
        last_updated_timestamp,
        dayname(last_updated_timestamp) AS week_day,

        -- Free-text trial status (raw form)
        trial_status AS free_text_trial_status
    FROM {{ ref('stg_courtroom_data') }}
)

SELECT
    *,

    -- Identify whether a courtroom is in use based on the trial status.
    -- Some records contain "No Information To Display", indicating an inactive courtroom.
    CASE
        WHEN contains(free_text_trial_status, 'No Information To Display')
        THEN 0
        ELSE 1
    END AS court_room_in_use,

    -- Extract structured trial status if the courtroom is in use.
    -- Assumes the format "Some text - Trial Status".
    CASE
        WHEN contains(free_text_trial_status, 'No Information To Display')
        THEN NULL
        ELSE split_part(free_text_trial_status, ' -', 1)
    END AS trial_status

FROM courtroom_data
