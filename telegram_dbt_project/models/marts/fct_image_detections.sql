-- models/marts/fct_image_detections.sql

{{ config(materialized='table') }}

SELECT
    det.message_id,
    msg.message_text,
    det.object_class,
    det.confidence_score
FROM raw_data.image_detections det
LEFT JOIN {{ ref('fct_messages') }} msg
    ON det.message_id = msg.message_id
