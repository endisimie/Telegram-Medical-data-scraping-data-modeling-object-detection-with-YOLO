select
  message_id,
  channel_id,
  sent_at,
  message_length,
  has_image
from {{ ref('stg_telegram_messages') }}
