from .database import fetch_all

# Top mentioned messages (as product mentions)
def get_top_products(limit: int = 10):
    return fetch_all("""
        SELECT text AS product, COUNT(*) AS mentions
        FROM raw_data.telegram_messages
        WHERE text IS NOT NULL
        GROUP BY text
        ORDER BY mentions DESC
        LIMIT %s
    """, (limit,))

# Channel-specific activity
def get_channel_activity(channel_name: str):
    return fetch_all("""
        SELECT dc.channel_name, COUNT(*) AS total_messages
        FROM raw_data_raw_data.fct_messages fm
        JOIN raw_data_raw_data.dim_channels dc ON fm.channel_id = dc.channel_id
        WHERE dc.channel_name = %s
        GROUP BY dc.channel_name
        ORDER BY total_messages DESC;
    """, (channel_name,))

# Search messages by keyword
def search_messages(query: str):
    return fetch_all("""
        SELECT id AS message_id, text, date, media
        FROM raw_data.telegram_messages
        WHERE text ILIKE %s
        ORDER BY date DESC
        LIMIT 50
    """, (f"%{query}%",))
