-- models/marts/dim_channels.sql

{{ config(materialized='view') }}

SELECT
    NULL::INTEGER AS channel_id,
    NULL::TEXT AS channel_name
WHERE FALSE
