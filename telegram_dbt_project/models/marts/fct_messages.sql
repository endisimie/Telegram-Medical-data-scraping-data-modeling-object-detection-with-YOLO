-- models/marts/fct_messages.sql

{{ config(materialized='table')}}

WITH base AS (
    SELECT
        message_id,
        message_text,
        media,
        message_date,
        message_day,
        message_hour,
        message_length,
        has_text,
        channel_id
    FROM {{ ref('stg_telegram_messages') }}
)

SELECT
    b.message_id,
    b.message_text,
    b.media,
    b.message_date,
    b.message_day,
    b.message_hour,
    b.message_length,
    b.has_text,
    d.year_month,
    d.day_name,
    d.month_name
FROM base b
LEFT JOIN {{ ref('dim_dates') }} d
  ON b.message_day = d.date_day
