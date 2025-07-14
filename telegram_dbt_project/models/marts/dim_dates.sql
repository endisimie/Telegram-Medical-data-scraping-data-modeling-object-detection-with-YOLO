select distinct
  sent_at::date as date_day,
  extract(dow from sent_at) as day_of_week,
  extract(week from sent_at) as week_number
from {{ ref('stg_telegram_messages') }}
