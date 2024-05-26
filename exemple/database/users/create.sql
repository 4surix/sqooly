INSERT OR IGNORE INTO users (
    name,
    created_at
)
VALUES (
    ?,
    strftime('%Y-%m-%d %H:%M:%S', 'now')
)
