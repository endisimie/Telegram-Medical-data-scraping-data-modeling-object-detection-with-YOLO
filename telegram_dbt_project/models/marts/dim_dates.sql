-- models/marts/dim_dates.sql

{{ config(materialized='table') }}

WITH calendar AS (
    SELECT
        d::DATE AS date_day
    FROM generate_series(
        (SELECT MIN(date)::DATE FROM raw_data.telegram_messages),
        (SELECT MAX(date)::DATE FROM raw_data.telegram_messages),
        '1 day'
    ) AS d
)

SELECT
    date_day,
    EXTRACT(DAY FROM date_day) AS day,
    EXTRACT(MONTH FROM date_day) AS month,
    EXTRACT(YEAR FROM date_day) AS year,
    TO_CHAR(date_day, 'Day') AS day_name,
    TO_CHAR(date_day, 'Month') AS month_name,
    TO_CHAR(date_day, 'YYYY-MM') AS year_month
FROM calendar
