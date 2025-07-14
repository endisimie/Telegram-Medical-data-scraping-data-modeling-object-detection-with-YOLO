-- models/staging/stg_telegram_messages.sql
with raw_data as (
  select * from {{ source('raw_data', 'telegram_messages') }}
)
select
  id::int as message_id,
  channel_id::int,
  date::timestamp as sent_at,
  message::text as message_text,
  media,
  length(message) as message_length,
  case when media like '%photo%' then true else false end as has_image
from raw_data
