
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE user_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    level INTEGER NOT NULL,
    score FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT 
    u.username,
    s.level,
    s.score,
    s.created_at
FROM user_scores s
JOIN users u ON s.user_id = u.id
ORDER BY s.created_at DESC;
