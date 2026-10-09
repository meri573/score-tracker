CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE results (
    id INTEGER PRIMARY KEY,
    game TEXT,
    time TEXT,
    grade TEXT,
    score INTEGER,
    big_mode INTEGER,
    twentyg_mode INTEGER,
    description TEXT,
    submitted_at TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users,
    result_id INTEGER REFERENCES results ON DELETE CASCADE
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE result_classes (
    id INTEGER PRIMARY KEY,
    result_id INTEGER REFERENCES results ON DELETE CASCADE,
    title TEXT,
    value TEXT
);