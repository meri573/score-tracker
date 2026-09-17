CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY,
    game TEXT,
    result_time TEXT,
    grade TEXT,
    score INTEGER,
    big_mode INTEGER,
    twentyg_mode INTEGER,
    result_description TEXT,
    submitted_at TEXT,
    user_id INTEGER REFERENCES users
);