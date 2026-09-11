CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY,
    game TEXT,
    time TEXT,
    grade TEXT
    score INTEGER
    big_mode INTEGER,
    20G_mode INTEGER,
    description TEXT,
    submitted_at TEXT,
    user_id INTEGER REFERENCES users
)