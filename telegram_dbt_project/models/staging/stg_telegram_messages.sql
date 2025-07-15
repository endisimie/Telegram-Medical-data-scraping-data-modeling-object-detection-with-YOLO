-- models/staging/stg_telegram_messages.sql

{{ config(materialized='view') }}

SELECT
    id AS message_id,
    (text IS NOT NULL AND LENGTH(TRIM(text)) > 0) AS has_text,
    TRIM(text) AS message_text,
    media,
    CAST(date AS TIMESTAMP) AS message_date,
    DATE(date) AS message_day,
    EXTRACT(HOUR FROM date) AS message_hour,
    LENGTH(TRIM(text)) AS message_length,
    channel_id
FROM raw_data.telegram_messages
WHERE text IS NOT NULL
