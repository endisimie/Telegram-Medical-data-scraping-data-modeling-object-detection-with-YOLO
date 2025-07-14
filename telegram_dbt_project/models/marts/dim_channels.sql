select distinct
  channel_id,
  'Channel ' || channel_id as channel_name
from {{ ref('stg_telegram_messages') }}
