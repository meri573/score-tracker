CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY,
    game TEXT,
    big_mode INTEGER,
    20G_mode INTEGER,
    submitted_at TEXT,
    user_id INTEGER REFERENCES users
)