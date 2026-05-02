CREATE TABLE Users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password_hash TEXT
);

CREATE TABLE Projects (
    id INTEGER PRIMARY KEY,
    title TEXT, 
    type INTEGER REFERENCES Classes ON DELETE SET NULL,
    description TEXT,
    owner INTEGER REFERENCES Users ON DELETE SET NULL
);

CREATE TABLE Items (
    id INTEGER PRIMARY KEY,
    title TEXT,
    type INTEGER REFERENCES Classes,
    description TEXT,
    image BLOB,
    project INTEGER REFERENCES Projects ON DELETE CASCADE
);

CREATE TABLE Classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);
